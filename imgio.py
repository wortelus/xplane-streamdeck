import sys
from os.path import join

import PIL
from PIL import Image

ASSETS_DIR = "icons"


# Hierarchical handler for opening icon assets first in the plane specific asset directory
# then trying the general asset directory
def open_icon_asset(plane_conf_dir, icon_filename):
    try:
        return Image.open(join(plane_conf_dir, ASSETS_DIR, icon_filename))
    except (FileNotFoundError, PIL.UnidentifiedImageError):
        # the icon is not in the plane specific directory
        # fallback to ASSET_DIR if no other unknown error is caught
        pass
    except Exception as e:
        print("unknown error while opening icon {} in the plane specific {} directory"
              .format(icon_filename, join(plane_conf_dir, ASSETS_DIR)))
        print("fall backing to the general asset directory {}".format(ASSETS_DIR))
        print(e)
    try:
        return Image.open(join(ASSETS_DIR, icon_filename))
    except (FileNotFoundError, PIL.UnidentifiedImageError):
        print("icon {} cannot be found either in the {} or {} directory"
              .format(icon_filename, join(plane_conf_dir, ASSETS_DIR), ASSETS_DIR))
        sys.exit(1)
    except Exception as e:
        print("unknown error while opening icon {} in the general {} directory"
              .format(icon_filename, ASSETS_DIR, e))
        print(e)
        sys.exit(1)
