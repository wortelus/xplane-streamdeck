import math
import threading
import time

import numpy as np
import yaml
from StreamDeck.DeviceManager import DeviceManager
from yaml import load
import pyxpudpserver as XPUDP

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
try:
    import preprocessing
except ImportError:
    print("You don't seem to have preprocessing.py near its main.py. correct your installation")
    exit(1)


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

            # todo auto_switch (global)
            # todo locking (switching directories)


def update_key_image(deck, key, image):
    with deck:
        deck.set_key_image(key, image)


def deck_show(deck, datarefs, images_all):
    for dref in datarefs:
        sd_index = dref["index"]
        fd = fetch_datarefs[sd_index]
        cur_val = XPUDP.pyXPUDPServer.getData(dref["dataref"])
        floor_cur_val = math.floor(cur_val)
        fetch_datarefs[sd_index] = floor_cur_val
        if floor_cur_val in dref["dataref-states"]:
            dref_index = dref["dataref-states"].index(floor_cur_val)
            image_name = dref["file_names"][dref_index]
            update_key_image(deck, sd_index, images_all[image_name])


def deck_show_static(deck, preset_current, images_all):
    for dir_button in preset_current:
        if dir_button.type != "dir" or dir_button.dataref is not None:
            continue
        if not dir_button["icon"]:
            print("Warning: button {} with index of {} is trying to display static, "
                  "but icon parameter was not set in config, skipping..."
                  .format(dir_button.name, dir_button.index))
            continue

        image_name = dir_button["icon"]
        update_key_image(deck, dir_button.index, images_all[image_name])


def main():
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
            print("\tDeck #{} setting as default for current session", index)

        print("\tDeck #{} with key count {}".format(index, deck.key_count()))
        print("\twith serial {}".format(serial))

    if not current_deck:
        print("Deck for current session NOT FOUND, verify the serial in config.yaml and index specified")
        exit(1)

    # loading info and check for connected SD count == config.yaml SD count
    print("config loaded for: {}".format(global_cfg["aircraft"]))
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
    keys_dir = panel["directory"]
    key_count = panel["keys"]
    dir_count = preprocessing.count_presets(keys_dir)

    presets_all = preprocessing.load_all_presets(keys_dir, key_count)
    datarefs_all = preprocessing.load_datarefs(presets_all)
    images_all = preprocessing.load_images_datarefs_all(current_deck, "ms33558.ttf", datarefs_all)

    global current_preset
    current_preset = presets_all["actions"]     # key index and preset index is the same, contains entire Button objects
    current_datarefs = datarefs_all["actions"]  # used for updating, contains only the showable buttons
    global fetch_datarefs
    fetch_datarefs = np.zeros(dtype=float, shape=key_count)

    current_deck.set_key_callback(key_change_callback)

    # show deck and set fetch_datarefs
    deck_show(current_deck, current_datarefs, images_all)

    while True:
        time.sleep(0.1)
        for dref in current_datarefs:
            sd_index = dref["index"]
            fd = fetch_datarefs[sd_index]
            cur_val = XPUDP.pyXPUDPServer.getData(dref["dataref"])
            floor_cur_val = math.floor(cur_val)
            if fd == floor_cur_val:
                continue

            fetch_datarefs[sd_index] = floor_cur_val
            if floor_cur_val in dref["dataref-states"]:
                dref_index = dref["dataref-states"].index(floor_cur_val)
                image_name = dref["file_names"][dref_index]
                update_key_image(current_deck, sd_index, images_all[image_name])



    print("done")


if __name__ == "__main__":
    main()
