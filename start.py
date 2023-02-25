import logging as logger
import sys

from xpsd import control

root = logger.getLogger()
root.setLevel(logger.INFO)

handler = logger.StreamHandler(sys.stdout)
handler.setLevel(logger.INFO)
formatter = logger.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def main():
    logger.info("Starting xplane-streamdeck by wortelus. This software is licensed under BSD 2-Clause License.")
    logger.info("Copyright (c) 2022, Daniel Slavík All rights reserved.")
    conf = control.load()
    ctl = control.DeckControl(conf)
    control.run(ctl)


if __name__ == "__main__":
    main()
