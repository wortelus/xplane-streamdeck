import argparse
import logging as logger
import signal
import sys

from xpsd import control

""" Main entry point for xplane-streamdeck by wortelus. """

formatter = logger.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

root = logger.getLogger()
root.setLevel(logger.INFO)

handler = logger.StreamHandler(sys.stdout)
handler.setLevel(logger.INFO)
handler.setFormatter(formatter)

root.addHandler(handler)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run xplane-streamdeck by wortelus.')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    return parser.parse_args()


def signal_handler(ctl):
    """Handler for graceful shutdown on SIGINT"""

    def handler(signum, frame):
        logger.info("SIGINT received, shutting down gracefully...")
        ctl.stop()  # Call ctl's stop method to clean up
        sys.exit(0)

    return handler


def main():
    args = parse_args()

    # Set log level based on debug flag
    if args.debug:
        root.setLevel(logger.DEBUG)
        handler.setLevel(logger.DEBUG)
        logger.debug("Debugging is enabled.")
    else:
        root.setLevel(logger.INFO)
        handler.setLevel(logger.INFO)

    logger.info("Starting xplane-streamdeck by wortelus. This software is licensed under BSD 2-Clause License.")
    logger.info("Copyright (c) 2022, Daniel Slavík All rights reserved.")

    conf = control.load()
    ctl = control.DeckControl(conf)

    signal.signal(signal.SIGINT, signal_handler(ctl))

    try:
        control.run(ctl, conf.update_rate)  # This runs the main loop
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        ctl.stop()
        sys.exit(1)


if __name__ == "__main__":
    main()
