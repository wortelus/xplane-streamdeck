import logging as logger
import sys
from os.path import join, exists

from StreamDeck.DeviceManager import ProbeError, DeviceManager
from xpsd import assetio
from xpsd.const import SERIAL_UNKNOWN, DEFAULT_BRIGHTNESS, DEFAULT_UPDATE_RATE


class RunningConfig(object):
    def __init__(self, global_config):
        self.global_cfg = global_config

        current_preset = global_config["stream-decks"][0]
        self.active_config = current_preset["active-preset"]

        self.only_uppercase = False
        self.active_config_path = join(assetio.ROOT_PATH, self.active_config)
        self.local_cfg = assetio.load_local_cfg(self.active_config_path)

        # only the first configuration works for now
        serial = assetio.load_serial(current_preset["serial"])
        self.active_deck = None
        self.key_count = 0
        self.connect_streamdeck(serial, current_preset.get("brightness"))

        # load config paths
        # only the first configuration works for now
        self.active_keyset_path = join(self.active_config_path,
                                       assetio.get_keyset_dir_name(self.key_count, self.local_cfg["force-config"]))

        self.default_font = None
        self.default_font_size = None
        self.read_local_cfg()

        # set the update rate
        self.update_rate = self.load_rate()

        # load caching options
        self.cache_path = None
        self.caching_enabled = False
        self.load_cached_img = False
        self.load_caching_options()

    def load_rate(self):
        if self.global_cfg["update-rate"]:
            r = float(1 / self.global_cfg["update-rate"])
            logger.info(f"setting update rate of {1/r}Hz ({r}s)")
            return r
        else:
            logger.warning(f"update-rate not set, setting {DEFAULT_UPDATE_RATE}")
            return 0.05

    def connect_streamdeck(self, serial, brightness=None):
        if brightness is None:
            logger.warning(f"brightness not set, setting {DEFAULT_BRIGHTNESS}")
            brightness = DEFAULT_BRIGHTNESS
        try:
            decks = DeviceManager().enumerate()
        except ProbeError as e:
            logger.error(
                "StreamDeck probe error, have you installed the LibUSB HIDAPI according to the README.md?")
            logger.error(e)
            sys.exit(1)

        deck_count = len(decks)
        logger.info("found {} Stream Deck(s).".format(deck_count))

        for index, deck in enumerate(decks):
            deck.open()
            deck.reset()
            s = deck.get_serial_number()
            if SERIAL_UNKNOWN == serial:
                deck.set_brightness(brightness)
                self.active_deck = deck
                self.key_count = deck.key_count()
                logger.warning("Serial number not set in the secret file. "
                               "If you run only one Stream Deck, this shouldn't matter")
                logger.info("Deck {} with {} keys setting as default for current session"
                            .format(index, self.key_count))
                return
            if s == serial:
                self.active_deck = deck
                self.key_count = deck.key_count()
                logger.info("Deck {} with {} keys setting as default for the current session"
                            .format(index, self.key_count))
                return
        logger.error("Stream Deck with given serial key was not found")
        sys.exit(1)

    def read_local_cfg(self):
        try:
            self.default_font, self.default_font_size = \
                assetio.load_default_font(self.local_cfg["default-font"], self.local_cfg["default-font-size"])
            if self.local_cfg["only-uppercase"]:
                self.only_uppercase = self.local_cfg["only-uppercase"]
        except OSError as e:
            logger.error("there was an error during loading font specified under the {} in {}. "
                         "Have you configured and installed the font correctly?"
                         .format(assetio.LOCAL_CONFIG_ALIAS, self.active_config_path))
            logger.error(e)
            sys.exit(1)

    def load_caching_options(self):
        if "caching-enabled" in self.local_cfg:
            self.cache_path = join(self.active_config_path,
                                   assetio.get_keyset_cache_name(self.key_count, self.local_cfg["force-config"]))
            # check cache_path if is not False or None -> implicating it is enabled in config
            # and check if it exists
            # then we will load the cache file, thus skipping the loader load_images_datarefs_all
            if self.cache_path:
                self.caching_enabled = True
                if exists(self.cache_path):
                    self.load_cached_img = True
