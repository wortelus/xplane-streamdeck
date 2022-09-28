import logging
from os.path import join
import sys

import numpy as np
import yaml
from yaml import safe_load
from PIL import ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

try:
    import dynamic
except ImportError:
    print("You don't seem to have dynamic.py near its main.py and preprocessing.py. correct your installation")
    sys.exit(1)
try:
    import sanity
except ImportError:
    print("You don't seem to have sanity.py near its main.py and preprocessing.py. correct your installation")
    sys.exit(1)
try:
    import assetio
except ImportError:
    print("You don't seem to have assetio.py near its main.py and preprocessing.py. correct your installation")
    sys.exit(1)

ACTION_CFG = "actions.yaml"
ACTION_CFG_NAME = "actions"

DEFAULT_FONT = None
DEFAULT_FONT_SIZE = 10

IMAGES_ALREADY_GENERATED = {}


#
# preset loading
#


def load_default_font(path, size):
    path = assetio.get_font_path(path)

    global DEFAULT_FONT_SIZE
    DEFAULT_FONT_SIZE = size
    global DEFAULT_FONT
    DEFAULT_FONT = ImageFont.truetype(path, size)


def get_filename_button_static_png(icon_name):
    return join(icon_name + ".png")


def get_filename_button_dataref_png(icon_name, state):
    return join(icon_name + "." + str(state) + ".png")


class Button(object):
    def __init__(self, index, name, icon, cmd_type, label=None, dataref=None, dataref_multiplier=None,
                 dataref_states=None, dataref_default=None, file_names=None, auto_switch=True,
                 cmd=None, cmd_mul=None, cmd_release=None, cmd_release_mul=None,
                 cmd_on=None, cmd_off=None, cmd_on_mul=None, cmd_off_mul=None,
                 gauge=None, display=None, special_labels=None):
        # Constants

        sanity.vital_check(index, name)

        self.index = index
        self.name = name
        self.icon = icon

        self.cmd_type = sanity.cmd_check(index, name, cmd_type)

        # verify string type
        self.label = sanity.label_check(index, name, label)

        self.dataref = dataref
        if dataref_multiplier is None:
            self.dataref_multiplier = 1.0
        else:
            self.dataref_multiplier = float(dataref_multiplier)

        self.switch_direction = 1  # up / cmd_on / cmd_on_mul
        if dataref_states is None:
            # if it dataref is None, then it is single-image key
            if dataref is not None:
                # set default values 0.0 and 1.0
                self.dataref_states = [0.0, 1.0]
                self.dataref_min = 0.0
                self.dataref_max = 1.0
            else:
                self.dataref_states = None
        else:
            self.dataref_states = dataref_states
            self.dataref_min = min(dataref_states)
            self.dataref_max = max(dataref_states)

        if auto_switch is None:
            self.auto_switch = True
        else:
            self.auto_switch = auto_switch

        # generate warnings for weird commands
        sanity.cmd2_check(index, name, cmd_type, cmd, cmd_mul, cmd_release, cmd_release_mul,
                          cmd_on, cmd_off, cmd_on_mul, cmd_off_mul)

        self.cmd = cmd
        self.cmd_mul = cmd_mul
        self.cmd_release = cmd_release
        self.cmd_release_mul = cmd_release_mul

        self.cmd_on = cmd_on
        self.cmd_off = cmd_off
        self.cmd_on_mul = cmd_on_mul
        self.cmd_off_mul = cmd_off_mul

        # Runtime Variables
        self.current = dataref_default

        # special labels do not need any type of preprocessing in this constructor
        self.special_labels = special_labels

        self.gauge = None
        self.display = None
        if file_names is not None:
            # sanity check file_names corresponding to dataref_states
            sanity.file_names_check(index, name, file_names, self.dataref_states)

            self.file_names = np.empty(len(file_names), dtype=object)
            for i, fn in enumerate(file_names):
                self.file_names[i] = get_filename_button_static_png(fn)
        elif gauge:
            # sanity check for gauge (if it contains everything)
            sanity.gauge_check(index, name, gauge)

            # overwrite default dataref_states
            self.dataref_states = dynamic.get_dataref_states(gauge, self)
            # special case - gauge with needles :)
            # here comes the dynamic.py into play
            self.gauge = gauge
            # preload full path for later image processing in dynamic.py
            self.gauge["background"] = get_filename_button_static_png(gauge["background"])
            self.gauge["needle"] = get_filename_button_static_png(gauge["needle"])
            # get own filenames, which really doesn't exist on disk and are created dynamically only for the runtime
            # so we pregenerate them artificial names for the use in main global images dict
            self.file_names = dynamic.create_dynamic_filenames(self.gauge["name"], self.dataref_states,
                                                               self.label, self.special_labels)
        elif display:
            # sanity check for display (if it contains everything)
            sanity.display_check(index, name, display)

            # overwrite default dataref_states
            self.dataref_states = dynamic.get_dataref_states(display, self)
            # special case - display of number values
            # here comes the dynamic.py into play
            self.display = display

            if "color" not in display:
                # set default color
                self.display["color"] = "white"

            self.display["background"] = get_filename_button_static_png(display["background"])
            self.file_names = dynamic.create_dynamic_filenames(self.display["name"], self.dataref_states,
                                                               self.label, self.special_labels)
        elif self.dataref_states is not None:
            if icon is None:
                logging.error("#{} {} is trying to set dataref_states without the 'icon' parameter, quitting..."
                              .format(index, name))
                sys.exit(1)

            self.file_names = np.empty(len(self.dataref_states), dtype=object)
            for i, state in enumerate(self.dataref_states):
                self.file_names[i] = get_filename_button_dataref_png(icon, state)
        else:
            if icon is None:
                logging.error("#{} {} is trying to set static icon without the 'icon' parameter, quitting..."
                              .format(index, name))
                sys.exit(1)

            self.file_names = np.empty(1, dtype=object)
            self.file_names[0] = get_filename_button_static_png(icon)


def load_preset(deck, target_dir, yaml_keyset, deck_key_count, preload_labels=False):
    with open(join(target_dir, yaml_keyset)) as stream:
        try:
            preset_cfg = safe_load(stream)
        except yaml.YAMLError as err:
            print("cannot load {}, ensure you have proper syntax config {}".format(yaml_keyset, err))
            sys.exit(1)

    keys = preset_cfg["actions"]
    # key_count = len(keys)

    preset = np.empty(deck_key_count, dtype=object)
    other_keysets = np.empty(shape=0, dtype=str)

    for _, key in enumerate(keys):
        index = key.get("index")
        name = key.get("name")
        # try to convert to int because it is used as array index
        try:
            index = int(index)
        except (ValueError, TypeError):
            logging.error("button with name {} has index non-convertable to integer, quitting...".format(name))
            sys.exit(1)
        cmd_type = key.get("type")
        preset[index] = Button(
            index,
            name,
            key.get("icon"),
            cmd_type,
            key.get("label"),
            key.get("dataref"),
            key.get("dataref-multiplier"),
            key.get("dataref-states"),
            key.get("dataref-default"),
            key.get("file-names"),
            key.get("auto-switch"),
            key.get("command"),
            key.get("commands"),
            key.get("command-release"),
            key.get("commands-release"),
            key.get("command-on"),
            key.get("command-off"),
            key.get("commands-on"),
            key.get("commands-off"),
            key.get("gauge"),
            key.get("display"),
            key.get("special-labels"),
        )

        # restoring images from cache file (preload_labels flag)
        # this applies to buttons with 'label' parameter set
        # If set to True, we must 'correct' image file_names here, because the
        # image post-loader load_images_datarefs_all is not called during current session
        if preload_labels:
            btn = preset[index]
            # dynamic elements (displays and gauges) were automatically handled by create_dynamic_filenames
            # in the Button constructor
            if not btn.display and not btn.gauge:
                for i, state_name in enumerate(btn.file_names):
                    # change state name for storing, allowing same icons with different labels
                    if btn.label:
                        state_name = btn.label + state_name
                        preset[index].file_names[i] = state_name
                    if btn.special_labels:
                        for j, spec_label in enumerate(btn.special_labels):
                            dynamic.get_text_pos(deck, spec_label)
                        prefix_state_name = dynamic.create_special_label_signature(btn.special_labels)
                        state_name = prefix_state_name + preset[index].file_names[i]
                        preset[index].file_names[i] = state_name

        if cmd_type == "dir":
            other_keysets = np.append(other_keysets, name)

    return preset, other_keysets


def add_yaml_suffix(filename):
    return filename + ".yaml"


def load_all_presets(deck, target_dir, deck_key_count, preload_labels=False):
    presets_all = {}
    # read root
    preset, keysets = load_preset(deck, target_dir, ACTION_CFG, deck_key_count,
                                  preload_labels=preload_labels)
    presets_all[ACTION_CFG_NAME] = preset
    # execute while there are keysets to be read and loaded into presets
    while keysets.size > 0:
        for _, key_set in enumerate(keysets):
            if key_set not in presets_all and key_set != "return":
                preset, other_keysets = load_preset(deck, target_dir, add_yaml_suffix(key_set), deck_key_count,
                                                    preload_labels=preload_labels)
                presets_all[key_set] = preset
                keysets = np.unique(np.concatenate((keysets, other_keysets), 0))

            keysets = np.delete(keysets, np.where(keysets == key_set))

    return presets_all


#
#
# X-Plane datarefs
#
#


def load_datarefs(presets_all):
    datarefs_all = {}
    for key_set_name, preset in presets_all.items():
        set_datarefs = np.empty(shape=0, dtype=object)
        for i, button in enumerate(preset):
            if button is None:
                continue

            if button.dataref:
                set_datarefs = np.append(set_datarefs, {
                    "name": button.name,
                    "index": button.index,
                    "icon": button.icon,
                    "dataref": button.dataref,
                    "dataref-multiplier": button.dataref_multiplier,
                    "dataref-states": button.dataref_states,
                    "file-names": button.file_names,
                    "current": button.current,
                    "dataref-min": button.dataref_min,
                    "dataref-max": button.dataref_max,
                })
        datarefs_all[key_set_name] = set_datarefs

    return datarefs_all


#
#
# Streamdeck images
#
#


# taken from https://python-elgato-streamdeck.readthedocs.io/en/stable/examples/basic.html
def render_key_image(deck, plane_conf_dir, icon_filename, label_text, special_labels, only_uppercase=False):
    # Ask forgiveness, not permission
    # This way we use nested approach to check first the plane specific icon set directory,
    # and next the icons/ directory for the asset
    icon = assetio.open_icon_asset(plane_conf_dir, icon_filename)

    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 0, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    if special_labels:
        for i, spec_label in enumerate(special_labels):
            draw = dynamic.load_special_label(spec_label, deck, draw)

    global DEFAULT_FONT
    if label_text:
        if only_uppercase and not label_text.isupper():
            print("WARN: label {} is not upper case only, "
                  "converting to upper (to disable this check out 'config.yaml'".format(label_text))
            label_text = label_text.upper()
        draw.text((image.width / 2, image.height - 8), text=label_text, font=DEFAULT_FONT, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)


def load_images_datarefs(deck, plane_conf_dir, presets_dir, only_uppercase):
    set_images = {}
    for _, button in enumerate(presets_dir):
        if button is None:
            continue

        # special case - gauge
        if button.gauge:
            if button.gauge["name"] in IMAGES_ALREADY_GENERATED:
                print("wait... presets for gauge {} already generated, skipping...".format(button.gauge["name"]))
                continue
            print("wait... generating gauge presets for {}".format(button.gauge["name"]))
            set_images.update(dynamic.load_gauge_images(button.gauge, deck, plane_conf_dir,
                                                        button.file_names))
            IMAGES_ALREADY_GENERATED[button.gauge["name"]] = "True"
            continue
        # special case - display
        if button.display:
            if button.display["name"] in IMAGES_ALREADY_GENERATED:
                print("wait... presets for display {} already generated, skipping...".format(button.display["name"]))
                continue
            print("wait... generating display presets for {}".format(button.display["name"]))
            set_images.update(dynamic.load_display_images(button.display, deck, plane_conf_dir,
                                                          button.file_names, button.dataref_states,
                                                          button.special_labels))
            IMAGES_ALREADY_GENERATED[button.display["name"]] = "True"
            continue

        for i, state_name in enumerate(button.file_names):
            # change file_names in preset according to images_all, allowing same icons with different labels
            # notice how this is executed in the post-processing stage
            # i.e. after the presets have long been generated
            # note: this does not apply to dynamic elements (displays, gauges)
            memory_img_name = state_name
            if button.label:
                memory_img_name = button.label + memory_img_name
                button.file_names[i] = memory_img_name
            if button.special_labels:
                prefix_state_name = dynamic.create_special_label_signature(button.special_labels)
                memory_img_name = prefix_state_name + button.file_names[i]
                button.file_names[i] = memory_img_name

            if memory_img_name not in set_images:
                state_image = render_key_image(deck, plane_conf_dir, state_name,
                                               button.label, button.special_labels, only_uppercase)
                set_images[memory_img_name] = state_image

    return set_images


def load_images_datarefs_all(deck, plane_conf_dir, presets_all, only_uppercase):
    set_images_all = {"none.png": render_key_image(deck, plane_conf_dir, get_filename_button_static_png("none"), None,
                                                   None, only_uppercase=only_uppercase),
                      "unknown.png": render_key_image(deck, plane_conf_dir, get_filename_button_static_png("unknown"),
                                                      None, None, only_uppercase=only_uppercase)}
    for _, dataref_dir in presets_all.items():
        images_single_dir = load_images_datarefs(deck, plane_conf_dir, dataref_dir, only_uppercase)
        set_images_all.update(images_single_dir)

    return set_images_all


#
# pickle helpers
#

# pickle is unable to handler 'memoryview' objects, we must convert them to bytearray and vice versa


def convert_to_save_format(images_all):
    images_bytearray = {}
    for key, img in images_all.items():
        images_bytearray[key] = img.tobytes()

    return images_bytearray


def convert_to_runtime_format(images_save_format):
    images_all = {}
    for key, img in images_save_format.items():
        images_all[key] = memoryview(img)

    return images_all
