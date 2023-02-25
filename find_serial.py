from StreamDeck.DeviceManager import DeviceManager

FLIP_ORIENTATIONS = {
    (False, False): "not mirrored",
    (True, False): "mirrored horizontally",
    (False, True): "mirrored vertically",
    (True, True): "mirrored horizontally/vertically",
}

if __name__ == "__main__":
    decks = DeviceManager().enumerate()
    for i, deck in enumerate(decks):
        deck.open()
        deck.reset()

        print("Deck {}".format(i))
        print(f"\t - Model: {deck.deck_type()}")
        print(f"\t - Serial Number: {deck.get_serial_number()}")
        print("\t - Key Count: {} ({}x{})".format(
            deck.key_count(),
            deck.key_layout()[0],
            deck.key_layout()[1]))
        print("\t - Hardware ID: {}".format(deck.id()))
        print("\t - Firmware Version: {}".format(deck.get_firmware_version()))
        if deck.is_visual():
            image_format = deck.key_image_format()
            print(f"\t - Button rendering: {image_format['size'][0]}x{image_format['size'][1]} pixels, "
                  f"{image_format['format']} format, rotated "
                  f"{image_format['rotation']} degrees, "
                  f"{FLIP_ORIENTATIONS[image_format['flip']]}")
        else:
            print("\t - Deck doesn't have visual output (screen)")

        deck.close()
