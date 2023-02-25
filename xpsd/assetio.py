import logging as logger
import sys
from os.path import join

import PIL
from PIL import Image, ImageFont
from yaml import YAMLError, load, Loader
from xpsd.const import ROOT_PATH, ASSETS_DIR, FONTS_DIR, GLOBAL_CONFIG_DIR, LOCAL_CONFIG_ALIAS


def load_global_cfg():
    with open(GLOBAL_CONFIG_DIR, "r") as stream:
        try:
            return load(stream, Loader=Loader)
        except YAMLError as err:
            logger.error("cannot load global config.yaml, ensure you have proper syntax config {}".format(err))
        except Exception as err:
            logger.error("unknown error while loading global config")
            logger.error(err)


def load_local_cfg(active_config_path):
    with open(join(active_config_path, LOCAL_CONFIG_ALIAS), "r") as stream:
        try:
            return load(stream, Loader=Loader)
        except YAMLError as err:
            logger.error("cannot load local config.yaml, ensure you have proper syntax config {}".format(err))
        except Exception as err:
            logger.error("unknown error while loading local config from {}".format(active_config_path))
            logger.error(err)


def load_serial(secret_filepath):
    with open(join(ROOT_PATH, secret_filepath), "r") as stream:
        try:
            y = load(stream, Loader=Loader)
            return y['serial']
        except YAMLError as err:
            logger.error("cannot load serial key from {}, ensure you have proper syntax config"
                         .format(secret_filepath))
            logger.error(err)
        except Exception as err:
            logger.error("unknown error while loading serial key from {}".format(secret_filepath))
            logger.error(err)


def load_default_font(name, size):
    path = get_font_path(name)

    default_font_size = size
    default_font = ImageFont.truetype(path, size)
    return default_font, default_font_size


def get_font_path(font_name):
    return join(FONTS_DIR, font_name)


def get_keyset_dir_name(key_count, force_config=None):
    if force_config:
        return force_config
    return "sd" + str(key_count)


def get_keyset_cache_name(key_count, force_config=None):
    return get_keyset_dir_name(key_count, force_config) + ".pkl"


def get_filename_button_static_png(icon_name):
    return join(icon_name + ".png")


def get_filename_button_dataref_png(icon_name, state):
    return join(icon_name + "." + str(state) + ".png")


def add_yaml_suffix(filename):
    return filename + ".yaml"


# Hierarchical handler for opening icon assets first in the plane specific asset directory
# then trying the general asset directory
def open_icon_asset(active_config_path, icon_filename):
    try:
        return Image.open(join(active_config_path, ASSETS_DIR, icon_filename))
    except (FileNotFoundError, PIL.UnidentifiedImageError):
        # the icon is not in the plane specific directory
        # fallback to ASSET_DIR if no other unknown error is caught
        pass
    except Exception as e:
        logger.warning("unknown error while opening icon {} in the plane specific {} directory"
                       .format(icon_filename, join(active_config_path, ASSETS_DIR)))
        logger.warning("fall backing to the general asset directory {}".format(ASSETS_DIR))
        logger.error(e)
    try:
        return Image.open(join(ASSETS_DIR, icon_filename))
    except (FileNotFoundError, PIL.UnidentifiedImageError):
        logger.error("icon {} cannot be found either in the {} or {} directory"
                     .format(icon_filename, join(active_config_path, ASSETS_DIR), ASSETS_DIR))
        sys.exit(1)
    except Exception as e:
        logger.error("unknown error while opening icon {} in the general {} directory"
                     .format(icon_filename, ASSETS_DIR))
        logger.error(e)
        sys.exit(1)
