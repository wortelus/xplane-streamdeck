import logging
import sys

VITAL_FIELDS = ["index", "name"]
CMD_TYPES = ["none", "dir", "single", "dual"]

GAUGE_FIELDS = ["name", "background", "needle", "min", "max", "step", "needle-center", "range-degrees"]
DISPLAY_FIELDS = ["name", "text-center", "font-path", "font-size", "zero-pad",
                  "min", "max", "step", "keep-decimal", "background"]


# returns nothing
def vital_check(index, name):
    if index is None:
        logging.error("index on button with name {} not set, quitting...".format(name))
        sys.exit(1)
    try:
        index = int(index)
    except ValueError:
        logging.error("button with name {} has non-numeric index -> check for mistype, quitting...".format(name))
        sys.exit(1)
    if name is None:
        logging.error("name on button with index of {} not set, quitting...".format(index))
        sys.exit(1)
    return


# returns accepted cmd_type
def cmd_check(index, name, cmd_type):
    if cmd_type is None or cmd_type == "":
        logging.warning("#{} {} has no set type, setting none as default (no press action)".format(index, name))
        return "none"

    for ct in CMD_TYPES:
        if cmd_type == ct:
            return cmd_type

    logging.warning("#{} {} has no known type of {}, setting none as default (no press action)"
                    .format(index, name, cmd_type))
    return "none"


# checks if label can be interpreted as str, returns label as str
def label_check(index, name, label):
    if not label:
        return label
    try:
        label = str(label)
        return label
    except ValueError:
        logging.error("#{} {} has non-string label, quitting...".format(index, name))
        sys.exit(1)


# checks if the commands are set corresponding to its cmd_type
# this just generates warnings, doesn't return anything
def cmd2_check(index, name, cmd_type, cmd=None, cmd_mul=None, cmd_release=None, cmd_release_mul=None,
               cmd_on=None, cmd_off=None, cmd_on_mul=None, cmd_off_mul=None):
    if cmd_type == "none":
        if cmd or cmd_mul or cmd_release or cmd_release_mul or cmd_on or cmd_off or cmd_on_mul or cmd_off_mul:
            logging.warning("#{} {} has set type of 'none', but commands are set too. The commands won't work"
                            .format(index, name))
    elif cmd_type == "single":
        if cmd_on or cmd_off or cmd_on_mul or cmd_off_mul:
            logging.warning("#{} {} has set type of 'single', but (some) on/off commands are set too. "
                            "The on/off commands won't work"
                            .format(index, name))
        if not cmd and not cmd_mul and not cmd_release and not cmd_release_mul:
            logging.warning("#{} {} has set type of 'single', but no single commands are set."
                            .format(index, name))
    elif cmd_type == "dual":
        if cmd or cmd_mul:
            logging.warning("#{} {} has set type of 'dual', but ''single'' commands are set too. "
                            "The single commands won't work"
                            .format(index, name))
        if cmd_release or cmd_release_mul:
            logging.warning("#{} {} has set type of 'dual' and release commands are set too. "
                            "The commands will be executed, but it's weird. "
                            "If it's intentional, you can ignore this message."
                            .format(index, name))
    return


# check if file_names and dataref_states are in sync
def file_names_check(index, name, file_names, dataref_states):
    if not file_names:
        return

    if dataref_states is None:
        logging.error("#{} {} has set file_names parameter, but not dataref_states are specified (is it static?)"
                      ",quitting...".format(index, name))
        sys.exit(1)

    if not isinstance(file_names, list) or not isinstance(dataref_states, list):
        logging.error("#{} {} has set file_names ({}) or dataref_states ({}) as not a list, quitting..."
                      .format(index, name, type(file_names), type(dataref_states)))
        sys.exit(1)

    if len(file_names) != len(dataref_states):
        logging.error("#{} {} has different length of file_names and dataref_states parameter, quitting..."
                      .format(index, name))
        sys.exit(1)
    return


# checks if gauge dict contains everything vital
def gauge_check(index, name, gauge):
    if not gauge:
        return

    for field in GAUGE_FIELDS:
        if field not in gauge:
            logging.error("#{} {} has set gauge, but parameter {} is missing, quitting..."
                          .format(index, name, field))
            sys.exit(1)

    # additional
    if "x" not in gauge["needle-center"] or "y" not in gauge["needle-center"]:
        logging.error("#{} {} has set gauge, but parameter x or y in 'needle-center' is missing, quitting..."
                      .format(index, name))
        sys.exit(1)

    return


# checks if display dict contains everything vital
def display_check(index, name, display):
    if not display:
        return

    for field in DISPLAY_FIELDS:
        if field not in display:
            logging.error("#{} {} has set display, but parameter {} is missing, quitting..."
                          .format(index, name, field))
            sys.exit(1)

    # additional
    if "x" not in display["text-center"] or "y" not in display["text-center"]:
        logging.error("#{} {} has set display, but parameter 'x' or 'y' in 'text-center' is missing, quitting..."
                      .format(index, name))
        sys.exit(1)

    return
