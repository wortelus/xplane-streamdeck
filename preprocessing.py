import os.path

import numpy as np
import yaml
from yaml import safe_load
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
try:
    import dynamic
except ImportError:
    print("You don't seem to have dynamic.py near its main.py and preprocessing.py. correct your installation")
    exit(1)

ACTION_CFG = "actions.yaml"
ACTION_CFG_NAME = "actions"
ASSETS_DIR = "icons"

DEFAULT_FONT = None
DEFAULT_FONT_SIZE = 10

IMAGES_ALREADY_GENERATED = {}


#
# preset loading
#


def load_default_font(path, size):
    global DEFAULT_FONT_SIZE
    DEFAULT_FONT_SIZE = size
    global DEFAULT_FONT
    DEFAULT_FONT = ImageFont.truetype(path, size)


def get_filename_button_static_png(icon_name):
    return os.path.join(ASSETS_DIR, icon_name + ".png")


def get_filename_button_dataref_png(icon_name, state):
    return os.path.join(ASSETS_DIR, icon_name + "." + str(state) + ".png")


class Button(object):
    def __init__(self, index, name, icon, cmd_type, label=None, dataref=None, dataref_multiplier=None,
                 dataref_states=None, dataref_default=None, file_names=None, auto_switch=True,
                 cmd=None, cmd_mul=None, cmd_release=None, cmd_release_mul=None,
                 cmd_on=None, cmd_off=None, cmd_on_mul=None, cmd_off_mul=None,
                 gauge=None, display=None, special_label=None):
        # Constants
        self.index = index
        if self.index is None:
            print("ERROR: button with name {} has no set index, quitting...".format(name))
            quit(1)

        self.name = name
        if self.name is None or self.name == "":
            print("ERROR: button with index {} has no set name, quitting...".format(index))
            quit(1)

        self.icon = icon

        self.cmd_type = cmd_type
        if cmd_type is None or cmd_type == "":
            print("WARN: {} has no set type, setting none as default (no press action)".format(name))
            self.cmd_type = "none"

        # verify string type
        if label:
            label = str(label)
        self.label = label

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

        self.gauge = None
        self.display = None
        self.special_label = None
        if file_names is not None:
            self.file_names = np.empty(len(file_names), dtype=object)
            for i, fn in enumerate(file_names):
                self.file_names[i] = get_filename_button_static_png(fn)
        elif gauge:
            # overwrite default dataref_states
            self.dataref_states = dynamic.get_dataref_states(gauge)
            # special case - gauge with needles :)
            # here comes the dynamic.py into play
            self.gauge = gauge
            # preload full path for later image processing in dynamic.py
            self.gauge["background"] = get_filename_button_static_png(gauge["background"])
            self.gauge["needle"] = get_filename_button_static_png(gauge["needle"])
            # get own filenames, which really doesn't exist on disk and are created dynamically only for the runtime
            # so we pregenerate them artificial names for the use in main global images dict
            self.file_names = dynamic.create_dynamic_filenames(self.gauge["name"], self.dataref_states)
        elif display:
            # overwrite default dataref_states
            self.dataref_states = dynamic.get_dataref_states(display)
            # special case - display of number values
            # here comes the dynamic.py into play
            self.display = display

            if "color" not in display:
                # set default color
                self.display["color"] = "white"

            self.display["background"] = get_filename_button_static_png(display["background"])
            self.file_names = dynamic.create_dynamic_filenames(self.display["name"], self.dataref_states)
        elif special_label:
            # todo
            pass
        elif self.dataref_states is not None:
            self.file_names = np.empty(len(self.dataref_states), dtype=object)
            for i, state in enumerate(self.dataref_states):
                self.file_names[i] = get_filename_button_dataref_png(icon, state)
        else:
            self.file_names = np.empty(1, dtype=object)
            if icon is None:
                print("static icon is not present on {} button".format(name))
                exit(1)
            self.file_names[0] = get_filename_button_static_png(icon)


def load_preset(target_dir, yaml_keyset, deck_key_count, preload_labels=False):
    with open(os.path.join(target_dir, yaml_keyset)) as stream:
        try:
            preset_cfg = safe_load(stream)
        except yaml.YAMLError as err:
            print("cannot load {}, ensure you have proper syntax config {}".format(yaml_keyset, err))
            exit(1)

    keys = preset_cfg["actions"]
    # key_count = len(keys)

    preset = np.empty(deck_key_count, dtype=object)
    other_keysets = np.empty(shape=0, dtype=str)

    for _, key in enumerate(keys):
        index = key.get("index")
        name = key.get("name")
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
            key.get("special-label"),
        )

        # restoring images from cache file (preload_labels flag)
        # this applies to buttons with 'label' parameter set
        # If set to True, we must 'correct' image file_names here, because the
        # image post-loader load_images_datarefs_all is not called during current session
        if preload_labels:
            btn = preset[index]
            for i, state_name in enumerate(btn.file_names):
                # change state name for storing, allowing same icons with different labels
                if btn.label:
                    state_name = btn.label + state_name
                    preset[index].file_names[i] = state_name

        if cmd_type == "dir":
            other_keysets = np.append(other_keysets, name)

    return preset, other_keysets


def add_yaml_suffix(filename):
    return filename + ".yaml"


def load_all_presets(target_dir, deck_key_count, preload_labels=False):
    presets_all = {}
    # read root
    preset, keysets = load_preset(target_dir, ACTION_CFG, deck_key_count,
                                  preload_labels=preload_labels)
    presets_all[ACTION_CFG_NAME] = preset
    # execute while there are keysets to be read and loaded into presets
    while keysets.size > 0:
        for _, key_set in enumerate(keysets):
            if key_set not in presets_all and key_set != "return":
                preset, other_keysets = load_preset(target_dir, add_yaml_suffix(key_set), deck_key_count,
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
def render_key_image(deck, icon_filename, label_text, only_uppercase=False):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 0, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    global DEFAULT_FONT
    if label_text:
        if only_uppercase and not label_text.isupper():
            print("WARN: label {} is not upper case only, "
                  "converting to upper (to disable this check out 'config.yaml'".format(label_text))
            label_text = label_text.upper()
        draw.text((image.width / 2, image.height - 8), text=label_text, font=DEFAULT_FONT, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)


def load_images_datarefs(deck, presets_dir, only_uppercase):
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
            set_images.update(dynamic.load_gauge_images(button.gauge, deck, button.file_names))
            IMAGES_ALREADY_GENERATED[button.gauge["name"]] = "True"
            continue
        if button.display:
            if button.display["name"] in IMAGES_ALREADY_GENERATED:
                print("wait... presets for display {} already generated, skipping...".format(button.display["name"]))
                continue
            print("wait... generating display presets for {}".format(button.display["name"]))
            set_images.update(dynamic.load_display_images(button.display, deck,
                                                          button.file_names, button.dataref_states))
            IMAGES_ALREADY_GENERATED[button.display["name"]] = "True"
            continue

        for i, state_name in enumerate(button.file_names):
            if state_name not in set_images:
                state_image = render_key_image(deck, state_name, button.label, only_uppercase)

                # change file_names in preset according to images_all, allowing same icons with different labels
                # notice how this is executed in the post-processing stage
                # i.e. after the presets have long been generated
                if button.label:
                    state_name = button.label + state_name
                    button.file_names[i] = state_name

                set_images[state_name] = state_image

    return set_images


def load_images_datarefs_all(deck, presets_all, only_uppercase):
    set_images_all = {"none.png": render_key_image(deck, get_filename_button_static_png("none"), None, only_uppercase)}
    for _, dataref_dir in presets_all.items():
        images_single_dir = load_images_datarefs(deck, dataref_dir, only_uppercase)
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
