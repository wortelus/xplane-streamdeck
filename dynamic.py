import numpy as np
from PIL import Image
from StreamDeck.ImageHelpers import PILHelper


def get_dataref_states(gauge):
    min_val = float(gauge["min"])
    max_val = float(gauge["max"] + 1)
    step = float(gauge["step"])

    fn_range = np.arange(min_val, max_val, step).tolist()
    return fn_range


def create_gauge_filenames(gauge, name, fn_range):
    file_names = np.empty(len(fn_range), dtype=object)
    for index, x in enumerate(fn_range):
        # no suffix needed, its not stored on hdd, only referenced in global images dict
        file_names[index] = name + "." + str(x)

    return file_names


def load_gauge_images(gauge, deck, file_names):
    center_needle = (float(gauge["needle-center"]["x"]), float(gauge["needle-center"]["y"]))
    total_range = float(gauge["max"] + 1) - float(gauge["min"])
    needle_multiplier = -float(gauge["range-degrees"]) / total_range

    set_images = {}

    # paths should be preprocessed from the Button __init__ constructor
    # thus no need to apply get_filename_button_static_png
    needle = Image.open(gauge["needle"])
    background = Image.open(gauge["background"])

    for i, fn in enumerate(file_names):
        final_img = background.copy()
        needle_cur = needle.copy()
        needle_cur = needle_cur.rotate(needle_multiplier * i, resample=Image.BICUBIC, center=center_needle)
        final_img.paste(needle_cur, mask=needle_cur)
        final_final_img = PILHelper.create_scaled_image(deck, final_img, margins=[0, 0, 0, 0])
        set_images[fn] = PILHelper.to_native_format(deck, final_final_img)

    return set_images

