from os.path import join

ROOT_PATH = ""

SERIAL_UNKNOWN = "SET_YOUR_SERIAL_HERE"
DEFAULT_BRIGHTNESS = 75

DEFAULT_UPDATE_RATE = 0.05  # 20x per second

LOCAL_CONFIG_ALIAS = "config.yaml"
GLOBAL_CONFIG_ALIAS = "config.yaml"
ASSETS_ALIAS = "icons"
FONTS_ALIAS = "fonts"

ASSETS_DIR = join(ROOT_PATH, ASSETS_ALIAS)
FONTS_DIR = join(ROOT_PATH, FONTS_ALIAS)
LOCAL_CONFIG_DIR = join(ROOT_PATH, LOCAL_CONFIG_ALIAS)
GLOBAL_CONFIG_DIR = join(ROOT_PATH, GLOBAL_CONFIG_ALIAS)

ACTION_CFG = "actions.yaml"
ACTION_CFG_ALIAS = "actions"

VITAL_FIELDS = ["index", "name"]
CMD_TYPES = ["none", "dir", "single", "dual"]

GAUGE_FIELDS = ["name", "background", "needle", "min", "max", "step", "needle-center", "range-degrees"]
DISPLAY_FIELDS = ["name", "text-center", "font-path", "font-size", "zero-pad",
                  "min", "max", "step", "keep-decimal", "background"]
