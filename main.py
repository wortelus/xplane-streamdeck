import math
import pickle
import sys
import time
from os.path import exists, join

import numpy as np
import yaml
from StreamDeck.DeviceManager import DeviceManager
from yaml import load
import pyxpudpserver as XPUDP
import logging

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
try:
    import preprocessing
except ImportError:
    print("You don't seem to have preprocessing.py near its main.py. correct your installation")
    sys.exit(1)

logging.basicConfig(encoding='utf-8')


# 0 is to move down, 1 to move up
def move_up_down_button(key, key_index, direction):
    if fetch_datarefs[key_index] >= key.dataref_max:
        return 0
    if fetch_datarefs[key_index] <= key.dataref_min:
        return 1

    # still not hit dataref limit, direction unchanged
    return direction


def key_change_callback(deck, key_index, state):
    if state:
        key = current_preset[key_index]
        if key is None:
            return

        if key.cmd_type == "single":
            if key.cmd:
                XPUDP.pyXPUDPServer.sendXPCmd(key.cmd)
            elif key.cmd_mul:
                for _, cmd in enumerate(key.cmd_mul):
                    XPUDP.pyXPUDPServer.sendXPCmd(cmd)
        elif key.cmd_type == "dual":
            next_direction = move_up_down_button(key, key.index, key.switch_direction)
            if next_direction == 1:
                # send on commands
                if key.cmd_on:
                    XPUDP.pyXPUDPServer.sendXPCmd(key.cmd_on)
                elif key.cmd_on_mul:
                    for _, cmd in enumerate(key.cmd_on_mul):
                        XPUDP.pyXPUDPServer.sendXPCmd(cmd)
            else:
                # send off commands
                if key.cmd_off:
                    XPUDP.pyXPUDPServer.sendXPCmd(key.cmd_off)
                elif key.cmd_off_mul:
                    for _, cmd in enumerate(key.cmd_off_mul):
                        XPUDP.pyXPUDPServer.sendXPCmd(cmd)
            # update direction
            key.switch_direction = next_direction
        elif key.cmd_type == "dir":
            global current_preset_name
            global directory_stack
            if key.name == "return":
                current_preset_name = directory_stack.pop()
                change_dir(deck, current_preset_name)
            else:
                directory_stack.append(current_preset_name)
                current_preset_name = key.name
                change_dir(deck, key.name)
    else:
        # button release (commonly used for momentary switches as the fire test on pedestal of 737)
        key = current_preset[key_index]
        if key is None:
            return

        if key.cmd_release is not None:
            XPUDP.pyXPUDPServer.sendXPCmd(key.cmd_release)
        elif key.cmd_release_mul is not None:
            for _, cmd in enumerate(key.cmd_release_mul):
                XPUDP.pyXPUDPServer.sendXPCmd(cmd)


def update_key_image(deck, key, image):
    with deck:
        deck.set_key_image(key, image)


def deck_show(deck, datarefs):
    for dref in datarefs:
        sd_index = dref["index"]
        cur_val = XPUDP.pyXPUDPServer.getData(dref["dataref"])
        cur_val *= dref["dataref-multiplier"]
        floor_cur_val = math.floor(cur_val)
        fetch_datarefs[sd_index] = floor_cur_val
        if floor_cur_val in dref["dataref-states"]:
            dref_index = dref["dataref-states"].index(floor_cur_val)
            image_name = dref["file-names"][dref_index]
            update_key_image(deck, sd_index, images_all[image_name])


def deck_show_static(deck):
    for index, dir_button in enumerate(current_preset):
        if dir_button is None:
            update_key_image(deck, index, images_all["none.png"])
            continue
        if dir_button.dataref is not None:
            continue
        if not dir_button.icon:
            print("Warning: button {} with index of {} is trying to display static, "
                  "but icon parameter was not set in config, skipping..."
                  .format(dir_button.name, dir_button.index))
            continue

        image_name = dir_button.file_names[0]
        update_key_image(deck, dir_button.index, images_all[image_name])


def update_fetch_datarefs(current_deck):
    for dref in current_datarefs:
        sd_index = dref["index"]
        fd = fetch_datarefs[sd_index]
        cur_val = XPUDP.pyXPUDPServer.getData(dref["dataref"])
        cur_val *= dref["dataref-multiplier"]
        floor_cur_val = math.floor(cur_val)
        if fd == floor_cur_val:
            continue

        fetch_datarefs[sd_index] = floor_cur_val
        if floor_cur_val in dref["dataref-states"]:
            dref_index = dref["dataref-states"].index(floor_cur_val)
            image_name = dref["file-names"][dref_index]
            update_key_image(current_deck, sd_index, images_all[image_name])


def change_dir(current_deck, name):
    global current_preset
    current_preset = presets_all[name]
    global current_datarefs
    current_datarefs = datarefs_all[name]
    deck_show_static(current_deck)
    deck_show(current_deck, current_datarefs)


def main():
    print("Starting xplane-streamdeck by wortelus. This software is licensed under BSD 2-Clause License.")
    print("Copyright (c) 2022, Daniel Slavík All rights reserved.")
    deck_count = 0
    decks = DeviceManager().enumerate()
    deck_count = len(decks)
    print("found {} Stream Deck(s).".format(deck_count))

    # open and load config.yaml into global_cfg
    with open("config.yaml", "r") as stream:
        try:
            global_cfg = load(stream, Loader=Loader)
        except yaml.YAMLError as err:
            print("cannot load config.yaml, ensure you have proper syntax config {}".format(err))

    current_deck = None
    for index, deck in enumerate(decks):
        deck.open()
        deck.reset()
        serial = deck.get_serial_number()
        if serial == global_cfg["stream-decks"][0]["serial"]:
            current_deck = deck
            if "brightness" in global_cfg:
                deck.set_brightness(global_cfg["brightness"])
            print("\tDeck {} setting as default for current session".format(serial))
            break

        print("Deck #{} with key count {}".format(index, deck.key_count()))
        print("with serial {}".format(serial))
        deck.close()

    if not current_deck:
        print("Deck for current session NOT FOUND, verify the serial in config.yaml and index specified")
        sys.exit(1)

    # loading info and check for connected SD count == config.yaml SD count
    print("configuration for {} decks, {} connected".format(len(global_cfg["stream-decks"]), deck_count))
    if len(global_cfg["stream-decks"]) != deck_count:
        print("WARN: configuration is for {} decks, but {} connected"
              .format(len(global_cfg["stream-decks"]), deck_count))
        deck_count = min(deck_count, len(global_cfg["stream-decks"]))

    # starting the X-Plane UDP client
    XPUDP.pyXPUDPServer.initialiseUDP((global_cfg["server-ip"], global_cfg["server-port"]),
                                      (global_cfg["xp-ip"], global_cfg["xp-port"]),
                                      "X-Plane Stream Deck Manager")
    XPUDP.pyXPUDPServer.start()

    # for now the software works only for one panel
    panel = global_cfg["stream-decks"][0]
    keys_dir = str(panel["directory"])
    key_count = panel["keys"]

    try:
        preprocessing.load_default_font(global_cfg["default-font"], global_cfg["default-font-size"])
    except OSError as e:
        print("there was an error during loading font specified under the config.yaml. "
              "Have you installed it correctly?")
        print(e)

    cache_path = None
    caching_enabled = False
    load_cached_img = False
    if "cache-path" in global_cfg:
        cache_path = join(global_cfg["cache-path"], keys_dir + ".pkl")
        # check cache_path if is not False or None -> implicating it is enabled in config
        # and check if it exists
        # then we will load the cache file, thus skipping the loader load_images_datarefs_all
        if cache_path:
            caching_enabled = True
            if exists(cache_path):
                load_cached_img = True

    global presets_all
    presets_all = preprocessing.load_all_presets(current_deck, keys_dir, key_count, preload_labels=load_cached_img)
    global datarefs_all
    datarefs_all = preprocessing.load_datarefs(presets_all)
    global images_all

    if not caching_enabled:
        print("note: caching is disabled, loading will be noticeably slower")
        print("you can enable it by setting the field 'cache-path' in config.yaml")
        images_all = preprocessing.load_images_datarefs_all(
            current_deck, keys_dir, presets_all, global_cfg["always-upper-case"])
    elif load_cached_img:
        # images are stored as cache, open and load
        print("cache file {} is present, skipping pre-generation.".format(cache_path))
        print("note: if you changed configuration or icon set, you should delete the {} cache file".format(cache_path))
        print("loading cache...")
        with open(cache_path, 'rb') as f:
            # load and convert it to runtime format
            images_save_format = pickle.load(f)
            images_all = preprocessing.convert_to_runtime_format(images_save_format)
    else:
        # caching is enabled, but cache file not found
        print("cache file {} not found, starting the pre-generation.".format(cache_path))
        images_all = preprocessing.load_images_datarefs_all(
            current_deck, keys_dir, presets_all, global_cfg["always-upper-case"])
        # save images to cache-path
        print("saving the pregen to {}".format(cache_path))
        with open(cache_path, 'wb') as f:
            # convert to save format and save it
            images_save_format = preprocessing.convert_to_save_format(images_all)
            pickle.dump(images_save_format, f)

    global directory_stack
    directory_stack = []

    global current_preset
    current_preset = presets_all["actions"]  # key index and preset index is the same, contains entire Button objects
    global current_preset_name
    current_preset_name = "actions"
    global current_datarefs
    current_datarefs = datarefs_all["actions"]  # used for updating, contains only the showable buttons
    global fetch_datarefs
    fetch_datarefs = np.zeros(dtype=float, shape=key_count)

    current_deck.set_key_callback(key_change_callback)

    # show deck and set fetch_datarefs
    deck_show(current_deck, current_datarefs)
    deck_show_static(current_deck)

    print("xplane-streamdeck ready...")

    try:
        while True:
            time.sleep(0.05)
            update_fetch_datarefs(current_deck)
    except KeyboardInterrupt:
        print('X-Plane Manager by wortelus interrupted! closing the deck and udp connection...')
        # note: closing only current deck
        current_deck.close()
        XPUDP.pyXPUDPServer.quit()
        print('connections closed, stopping...')


if __name__ == "__main__":
    main()
