import numpy as np
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper
import assetio


def get_dataref_states(element, button_self):
    step = float(element["step"])

    decimal_divider = 1
    if step < 1.0:
        # count number of decimal places, do not use float, use input straight from configuration
        decimal_divider = 10 ** len(str(element["step"]).split(".")[1])
        element["min"] *= decimal_divider
        element["max"] *= decimal_divider
        # pretty hacky here, we must assume that the button_self is in fact a button object
        button_self.dataref_multiplier *= decimal_divider
        step = 1.0

    element["decimal-divider"] = decimal_divider

    min_val = float(element["min"])
    max_val = float(element["max"] + 1)
    fn_range = np.arange(min_val, max_val, step).tolist()
    return fn_range


def create_dynamic_filenames(name, fn_range, label, special_labels):
    name = str(name)
    if label:
        name = label + name
    if special_labels:
        name = create_special_label_signature(special_labels) + name

    file_names = np.empty(len(fn_range), dtype=object)
    for index, x in enumerate(fn_range):
        # no suffix needed, it's not stored on hdd, only referenced in global images dict
        file_names[index] = name + "." + str(x)

    return file_names


def get_text_pos(deck, special):
    if special["text-center"]["x"] == "center":
        special["text-center"]["x"] = deck.key_image_format()["size"][0] / 2
    if special["text-center"]["y"] == "center":
        special["text-center"]["y"] = deck.key_image_format()["size"][1] / 2

    return special["text-center"]


def load_truetype_font(element):
    font_path = assetio.get_font_path(element["font-path"])
    return ImageFont.truetype(font_path, element["font-size"])


#
# gauges
#

def load_gauge_images(gauge, deck, plane_conf_dir, file_names):
    center_needle = (float(gauge["needle-center"]["x"]), float(gauge["needle-center"]["y"]))
    total_range = float(gauge["max"] + 1) - float(gauge["min"])
    needle_multiplier = -float(gauge["range-degrees"]) / total_range

    set_images = {}

    # paths should be preprocessed from the Button __init__ constructor
    # thus no need to apply get_filename_button_static_png
    needle = assetio.open_icon_asset(plane_conf_dir, (gauge["needle"]))
    background = assetio.open_icon_asset(plane_conf_dir, (gauge["background"]))

    for i, fn in enumerate(file_names):
        final_img = background.copy()
        needle_cur = needle.copy()
        needle_cur = needle_cur.rotate(needle_multiplier * i, resample=Image.BICUBIC, center=center_needle)
        final_img.paste(needle_cur, mask=needle_cur)
        final_final_img = PILHelper.create_scaled_image(deck, final_img, margins=[0, 0, 0, 0])
        set_images[fn] = PILHelper.to_native_format(deck, final_final_img)

    return set_images


#
# displays
#


def load_display_images(display, deck, plane_conf_dir, file_names, dataref_states, special_labels):
    set_images = {}

    # if user preconfigured 'x' or 'y' position of text as center, we must set it here ->
    get_text_pos(deck, display)

    # paths should be preprocessed from the Button __init__ constructor
    # thus no need to apply get_filename_button_static_png
    background = assetio.open_icon_asset(plane_conf_dir, display["background"])
    # todo how not to load font every single time ?
    current_font = load_truetype_font(display)
    sl_fonts = None
    if special_labels:
        sl_fonts = np.empty(len(special_labels), dtype=object)
        for i, spec_label in enumerate(special_labels):
            sl_fonts[i] = load_truetype_font(spec_label)
    if len(dataref_states) != len(file_names):
        print("display of name {} has not the same len of dataref_states and file_names. this should not happen,"
              "submit a issue on wortelus/xplane-streamdeck GitHub repository, please".format(display["name"]))

    for i, fn in enumerate(file_names):
        final_img = background.copy()
        final_final_img = PILHelper.create_scaled_image(deck, final_img, margins=[0, 0, 0, 0])

        if display["keep-decimal"]:
            if display["zero-pad"]:
                display_text = str(dataref_states[i] / display["decimal-divider"]) \
                    .zfill(display["zero-pad"])
            else:
                display_text = str(dataref_states[i] / display["decimal-divider"])
        else:
            if display["zero-pad"]:
                display_text = str(int(dataref_states[i])).zfill(display["zero-pad"])
            else:
                display_text = str(int(dataref_states[i]))

        draw = ImageDraw.Draw(final_final_img)
        draw.text(
            (display["text-center"]["x"], display["text-center"]["y"]),
            text=display_text, font=current_font, anchor="ms", fill=display["color"])

        # special labels
        if special_labels:
            for j, spec_label in enumerate(special_labels):
                draw = load_special_label(spec_label, deck, draw, sl_fonts[j])

        set_images[fn] = PILHelper.to_native_format(deck, final_final_img)

    return set_images


#
# special labels
#

def create_special_label_signature(special_labels):
    output = "SpecialLabel/"
    for i, spec_label in enumerate(special_labels):
        output += str(spec_label["text-center"]["x"]) + \
                  str(spec_label["text-center"]["y"]) + \
                  str(spec_label["label"]) + \
                  str(spec_label["font-path"]) + \
                  str(spec_label["font-size"]) + \
                  str(spec_label["color"]) + \
                  str(spec_label["direction"]) + \
                  str(spec_label["align"])
    return output


def load_special_label(special_label, deck, draw, font=None):
    # if user preconfigured 'x' or 'y' position of text as center, we must set it here ->
    get_text_pos(deck, special_label)

    if not font:
        font = load_truetype_font(special_label)

    draw.text(
        (special_label["text-center"]["x"], special_label["text-center"]["y"]),
        text=special_label["label"], font=font, anchor="ms", fill=special_label["color"],
        # direction=special_label["direction"], ----- libraqm required
        align=special_label["align"])
    return draw
