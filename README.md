# X-Plane Stream Deck Manager
![main screen](misc/main.jpg)

This is a manager for X-Plane <-> Elgato Stream Deck connection. Developed on Python 3.10 for X-Plane 11.51.

This software includes rich set of features for robust control of the simulator cockpit.

Developed with the idea taking away mouse controlling of most of the cockpit, 
works best together with other simulator peripherals (e.g. radio, A/P panel etc.)

**Currently supporting**:
- Stream Deck Mini
- Stream Deck MK1 (MK2 should work too)
- Stream Deck XL (tested)

### Features:
- Sync with X-Plane's dataref to visually depict the actual state
- Multiple dataref states with each custom key image
- Directories
- Toggle actions (single command)
- Multiple command actions
- Momentary switches
- Push / Release actions
- Supporting multi-position switches or knobs control via single button (cycling positions)
- Custom labels
- ***Gauges***
- ***400+ custom made icons*** for the 737 NG

All of these features can be configurated in simple YAML configs. YAML is very easy to use
and simple format similar to JSON, but more human-readable and harder to cause a syntax error in.

### Dependencies
- NumPy
- PyYAML
- streamdeck - Windows requires additional DLL's installed in directory under %PATH% variable (LibUSB HIDAPI)
- Pillow
- pyxpudpserver

## Installation
Instructions for **Windows**

1. **Download and install Python 3 (3.10 minimum recommended)**

- *choosing the option to add Python to %PATH% and removing the %PATH% length limit is **recommended***
- both are options during installation, otherwise you might have to include absolute path to Python to launch the script

2. **Clone this repository by:**
- `git clone https://github.com/wortelus/xplane-streamdeck.git`
- or download source code by **Download ZIP** and extract the files
3. **Add your font in the same directory as the `main.py`**
- **MS33558** recommended, the name the script will try to open is written in **config.yaml**
4. **Install the dependencies by**

`python -m pip install -r dependencies.txt`

5. **Install LibUSB HIDAPI**

- The *streamdeck* package requires LibUSB HIDAPI, install it by following this 
[guide](https://python-elgato-streamdeck.readthedocs.io/en/stable/pages/backend_libusb_hidapi.html)
from the official documentation source

## Usage
Instructions for **Windows**

**Execute the script by running the `main.py` with Python 3 by:**

running `python .\main.py` under the *xplane-streamdeck* directory, 
while having the Stream Deck plugged in already

### Additional Info

**Refer to the `B737-800X/README.md` for a guide on how to create/edit buttons.**

![lower overhead](misc/lwrovhd.jpg)
![mcp](misc/mcp.jpg)

*More example images in `misc/`*

#### Notes
A lot of buttons in the flight deck are momentary switches and buttons, which are expected to be held in position.
For that purpose, I have built a small LUA file with custom commands in `misc/streamdeck_handlers.lua`.
The momentary switches work on a way that the `command_begin` executes the `begin` part of the command, 
which switches it into the desired position, and `command_end` which returns the switch/button back into its 
stable position (also known as the `end` part of the command`. 

So, the bad news is that you have to create two commands for your each `begin` and `end` action everytime.

The X-Plane UDP protocol is limited in this way, the UDP protocol is able to execute only all 3 parts of the
command (yes, 3.. begin, continue, end), so I recommend solving it this way. You will map those two commands 
from the LUA handler in the`command` and `command-release` YAML configuration. 
Look for examples in `actions.yaml`, where it is used on fire warning or master caution of the 737 etc.
### How it works
- The streamdeck Python library provides modular access
- X-Plane has its simple, yet powerful UDP protocol for communication with the external applications 
- You define your yaml configurations and icons 
- Only the needed files, icons and configurations are loaded into RAM 
- The software then efficiently runs in background updating your buttons and responding to state changes of the buttons 
- Performance hit is expected to be under 0.1%, while **updating 20x per second**
- You can change the update rate in the `main.py`

### Key Creation and Configuration
1. Create empty directory with any name (ex. B737), that name will need to be referenced in config.yaml. 
Your actions.yaml and other keysets (directories) will take place here.
Actual icons as files are going to be put under 'icons' directory.
2. The actions.yaml resembles the root directory of the stream deck keys.
3. xyz.yaml, ABC.yaml, 123.yaml... *.yaml resembles the keysets (directories),
you're going to reference the directories by their name in key configs with keys attributed as "dir".
4. Keyset can be left unreferenced, it will be simply ignored and NOT loaded into memory.

**Refer to the `B737-800X/README.md` for a guide on how to create/edit buttons.**
### What is planned / WIP?
- Dynamic dataref display types
- More types of labels
- Multi deck support

### Known Issues
There is currently a bug in **pyxpudpserver** that causes the dataref updating of buttons to
freeze (giving you a message *"dictionary changed size during iteration"*.

The proposed solution is to use locking instead of simple if condition in its main lib file.

You can apply it yourself until this gets resolved.

## License
BSD 2-Clause License

Copyright (c) 2022, Daniel Slavík All rights reserved.

www.wortelus.eu
