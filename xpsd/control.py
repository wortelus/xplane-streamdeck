import math
import pickle
import sys
import time

import numpy as np
import pyxpudpserver as xpudp
import logging as logger

from xpsd.assetio import load_global_cfg
from xpsd.configuration import RunningConfig

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from xpsd import preprocessing


def update_key_image(deck, key, image):
    with deck:
        deck.set_key_image(key, image)


class DeckControl(object):
    def __init__(self, conf: RunningConfig):
        self.configuration = conf
        self.press = PressDomain(conf)

    def start(self):
        # starting the X-Plane UDP client
        xpudp_logger = logger.getLogger("UDPserver")
        xpudp_handler = XPUDPHandler()
        xpudp_logger.addHandler(xpudp_handler)
        xpudp.pyXPUDPServer.initialiseUDP(
            (self.configuration.global_cfg["server-ip"], self.configuration.global_cfg["server-port"]),
            (self.configuration.global_cfg["xp-ip"], self.configuration.global_cfg["xp-port"]),
            "X-Plane Stream Deck Manager")

        if xpudp_handler.Error:
            logger.error("The X-Plane UDP connection could not be initialized, "
                         "refer to README.md for potential causes.")
            sys.exit(1)
        elif xpudp_handler.OSError:
            logger.error(
                "The X-Plane UDP connection could not be initialized due to operating system error, this is probably"
                " caused by misconfiguration of port numbers or the xplane-streamdeck is launched twice.")
            sys.exit(1)

        xpudp.pyXPUDPServer.start()

    def update(self):
        self.press.view.update(self.configuration.active_deck)

    def stop(self):
        self.configuration.active_deck.close()
        xpudp.pyXPUDPServer.quit()


class ViewDomain(object):
    def __init__(self, conf: RunningConfig, presets_all, fetch_datarefs):
        self.presets_all = presets_all
        self.fetch_datarefs = fetch_datarefs

        self.datarefs_all = preprocessing.load_datarefs(self.presets_all)
        self.images = load_images(conf, presets_all)

        self.current_preset = self.presets_all[preprocessing.ACTION_CFG_ALIAS]
        self.current_preset_name = preprocessing.ACTION_CFG_ALIAS
        self.current_datarefs = self.datarefs_all[preprocessing.ACTION_CFG_ALIAS]

    def update(self, deck):
        self.deck_show(deck, self.current_datarefs)
        self.deck_show_static(deck)

    def deck_show(self, deck, datarefs):
        for dref in datarefs:
            sd_index = dref["index"]
            cur_val = xpudp.pyXPUDPServer.getData(dref["dataref"])
            cur_val *= dref["dataref-multiplier"]
            cur_val += dref["dataref-offset"]
            floor_cur_val = math.floor(cur_val)
            self.fetch_datarefs[sd_index] = floor_cur_val
            if floor_cur_val in dref["dataref-states"]:
                dref_index = dref["dataref-states"].index(floor_cur_val)
                image_name = dref["file-names"][dref_index]
                try:
                    update_key_image(deck, sd_index, self.images[image_name])
                except KeyError as e:
                    logger.error(
                        "unknown key at {} with name {}, image not found is: {}. Have you changed the configuration?"
                        " If so, delete the cache file to be recreated with new one."
                        .format(sd_index, dref["name"], str(e)))
                    update_key_image(deck, sd_index, self.images["unknown.png"])

    def deck_show_static(self, deck):
        for index, dir_button in enumerate(self.current_preset):
            if dir_button is None:
                update_key_image(deck, index, self.images["none.png"])
                continue
            if dir_button.dataref is not None:
                continue
            if not dir_button.icon:
                logger.error("Warning: button {} with index of {} is trying to display static, "
                             "but icon parameter was not set in config, skipping..."
                             .format(dir_button.name, dir_button.index))
                continue

            image_name = dir_button.file_names[0]
            try:
                update_key_image(deck, dir_button.index, self.images[image_name])
            except KeyError as e:
                logger.error(
                    "unknown key at {} with name {}, image not found is: {}. Have you changed the configuration?"
                    " If so, delete the cache file to be recreated with new one."
                    .format(index, dir_button.name, str(e)))
                update_key_image(deck, dir_button.index, self.images["unknown.png"])

    def update_fetch_datarefs(self, current_deck):
        for dref in self.current_datarefs:
            sd_index = dref["index"]
            fd = self.fetch_datarefs[sd_index]
            cur_val = xpudp.pyXPUDPServer.getData(dref["dataref"])
            cur_val *= dref["dataref-multiplier"]
            cur_val += dref["dataref-offset"]
            floor_cur_val = math.floor(cur_val)
            if fd == floor_cur_val:
                continue

            self.fetch_datarefs[sd_index] = floor_cur_val
            if floor_cur_val in dref["dataref-states"]:
                dref_index = dref["dataref-states"].index(floor_cur_val)
                image_name = dref["file-names"][dref_index]
                update_key_image(current_deck, sd_index, self.images[image_name])


class PressDomain(object):
    def __init__(self, conf: RunningConfig):
        self.presets_all = preprocessing.load_all_presets(conf, conf.load_cached_img)
        self.fetch_datarefs = np.zeros(dtype=float, shape=conf.key_count)

        self.presets_all = self.presets_all
        self.datarefs_all = preprocessing.load_datarefs(self.presets_all)

        self.directory_stack = []

        self.view = ViewDomain(conf, self.presets_all, self.fetch_datarefs)

    def key_change_callback(self, deck, key_index, state):
        if state:
            key = self.view.current_preset[key_index]
            if key is None:
                return

            if key.cmd_type == "single":
                if key.cmd:
                    xpudp.pyXPUDPServer.sendXPCmd(key.cmd)
                elif key.cmd_mul:
                    for _, cmd in enumerate(key.cmd_mul):
                        xpudp.pyXPUDPServer.sendXPCmd(cmd)
            elif key.cmd_type == "dual":
                next_direction = self.move_up_down_button(key, key.index, key.switch_direction)
                if next_direction == 1:
                    # send on commands
                    if key.cmd_on:
                        xpudp.pyXPUDPServer.sendXPCmd(key.cmd_on)
                    elif key.cmd_on_mul:
                        for _, cmd in enumerate(key.cmd_on_mul):
                            xpudp.pyXPUDPServer.sendXPCmd(cmd)
                else:
                    # send off commands
                    if key.cmd_off:
                        xpudp.pyXPUDPServer.sendXPCmd(key.cmd_off)
                    elif key.cmd_off_mul:
                        for _, cmd in enumerate(key.cmd_off_mul):
                            xpudp.pyXPUDPServer.sendXPCmd(cmd)
                # update direction
                key.switch_direction = next_direction
            elif key.cmd_type == "dir":
                if key.name == "return":
                    self.view.current_preset_name = self.directory_stack.pop()
                    self.change_dir(deck, self.view.current_preset_name)
                else:
                    self.directory_stack.append(self.view.current_preset_name)
                    self.view.current_preset_name = key.name
                    self.change_dir(deck, key.name)
        else:
            # button release (commonly used for momentary switches as the fire test on pedestal of 737)
            key = self.view.current_preset[key_index]
            if key is None:
                return

            if key.cmd_release is not None:
                xpudp.pyXPUDPServer.sendXPCmd(key.cmd_release)
            elif key.cmd_release_mul is not None:
                for _, cmd in enumerate(key.cmd_release_mul):
                    xpudp.pyXPUDPServer.sendXPCmd(cmd)

    # 0 is to move down, 1 to move up
    def move_up_down_button(self, key, key_index, direction):
        if self.fetch_datarefs[key_index] >= key.dataref_max:
            return 0
        if self.fetch_datarefs[key_index] <= key.dataref_min:
            return 1

        # still not hit dataref limit, direction unchanged
        return direction

    def change_dir(self, current_deck, name):
        self.view.current_preset = self.presets_all[name]
        self.view.current_datarefs = self.datarefs_all[name]
        self.view.deck_show_static(current_deck)
        self.view.deck_show(current_deck, self.view.current_datarefs)


# we have to catch an error during loading, we use this error logger handler for this purpose
class XPUDPHandler(logger.StreamHandler):
    def __init__(self):
        super().__init__(stream=sys.stderr)
        self.OSError = False
        self.Error = False

    def emit(self, record):
        if record.levelno >= 40 and record.exc_info[0] is OSError:
            self.OSError = True
        elif record.levelno >= 40:
            self.Error = True


def load_images(conf, presets_all):
    if not conf.caching_enabled:
        logger.info("note: caching is disabled, loading will be noticeably slower")
        logger.info("you can enable it by setting the field 'cache-path' in config.yaml")
        images = preprocessing.load_images_datarefs_all(
            conf, presets_all, conf.local_cfg["only-uppercase"])
    elif conf.load_cached_img:
        # images are stored as cache, open and load
        logger.info("cache file {} is present, skipping pre-generation".format(conf.cache_path))
        logger.info("note: if you changed configuration or icon set, you should delete the {} cache file".format(
            conf.cache_path))
        logger.info("loading cache...")
        with open(conf.cache_path, 'rb') as f:
            # load and convert it to runtime format
            images_save_format = pickle.load(f)
            images = preprocessing.convert_to_runtime_format(images_save_format)
    else:
        # caching is enabled, but cache file not found
        logger.info("cache file {} not found, starting the pre-generation".format(conf.cache_path))
        images = preprocessing.load_images_datarefs_all(
            conf, presets_all, conf.local_cfg["only-uppercase"])
        # save images to cache-path
        logger.info("saving cache to {}".format(conf.cache_path))
        with open(conf.cache_path, 'wb') as f:
            # convert to save format and save it
            images_save_format = preprocessing.convert_to_save_format(images)
            pickle.dump(images_save_format, f)

    return images


def load():
    global_cfg = load_global_cfg()
    conf = RunningConfig(global_cfg)
    return conf


def run(ctl: DeckControl, update_rate):
    ctl.start()
    ctl.configuration.active_deck.set_key_callback(ctl.press.key_change_callback)
    logger.info("xplane-streamdeck ready...")

    # show deck and set fetch_datarefs
    ctl.update()

    try:
        while True:
            time.sleep(update_rate)
            ctl.press.view.update_fetch_datarefs(ctl.configuration.active_deck)
    except KeyboardInterrupt:
        logger.info('X-Plane Manager by wortelus interrupted! closing the deck and udp connection...')
        # note: closing only current deck
        logger.info('connections closed, stopping...')
