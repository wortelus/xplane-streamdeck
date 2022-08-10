# X-Plane Stream Deck Manager
![main screen](misc/main.jpg)

This is a manager for X-Plane <-> Elgato Stream Deck connection. Developed on Python 3.10 for X-Plane 11.51.

This software includes rich set of features for robust control of the simulator cockpit.

Developed with the idea taking away mouse controlling of most of the cockpit, 
works best together with other simulator peripherals (e.g. radio, A/P panel etc.)

**Note that configuration was done for 737 NG by Zibo only for now.**

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
- **Displays**
- **Gauges**
- **400+ custom made icons** for the 737 NG

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
- clone by git on your machine by `git clone https://github.com/wortelus/xplane-streamdeck.git`
- or download source code by **Download ZIP** and extract the files
- or download latest stable release under the **Releases** section
3. *(Optional step)* - **Add your custom font in the same directory as the `main.py`**
- current one set is OFL font **IBMPlexMono**
- the name the script will try to open is written in **config.yaml**
- The script searches first the working directory of the program, then `C:/Windows/Fonts`
- **MS33558** optional
- You can download it from the internet, this repository doesn't redistribute it.
- If you want to use downloaded font, put it under the `xplane-streamdeck` directory
4. **Install the dependencies by**

`.../xplane-streamdeck> python -m pip install -r dependencies.txt`

using cmd or PowerShell

5. **Install LibUSB HIDAPI**

- The *streamdeck* package requires LibUSB HIDAPI, install it by following this 
[guide](https://python-elgato-streamdeck.readthedocs.io/en/stable/pages/backend_libusb_hidapi.html)
from the official documentation source

6. **Update `config.yaml` for your preferences and enable UDP server in X-Plane settings**
- Mainly update the **serial number** of your Stream Deck with your **serial 
number** and number of keys according to your model. 
- Execute the xplane-streamdeck script to find the serial number out
- Check the font, IP addresses / ports and X-Plane's UDP server status in case of a problem
7. **Add the `streamdeck_handlers.lua` to `X-Plane 11\Resources\plugins\FlyWithLua\Scripts`**
- Ensure you have **FlyWithLua** installed

## Usage
Instructions for **Windows**

**Execute the script by running the `main.py` with Python 3 by:**

running `.../xplane-streamdeck> python .\main.py` under the *xplane-streamdeck* directory, 
while having the Stream Deck plugged in already

The program supports image caching, which saves several seconds of image preloading during launch
- To enable it, set `cache-path` field in `config.yaml`
- To disable, just remove the field or leave it blank
- NOTE: If you are tweaking your image set or configuration, it is recommended disable this feature 
to always see the up-to-date configuration state (or simply remove it, but the cache will be recreated)

## Additional Info
|        Lower Overhead 737 NG        |  MCP Collins 737 NG  |
|:-----------------------------------:|:--------------------:|
| ![lower overhead](misc/lwrovhd.jpg) | ![mcp](misc/mcp.jpg) |

*More example images in `misc/`*

### How it works
- The streamdeck Python library provides modular access
- X-Plane has its simple, yet powerful UDP protocol for communication with the external applications 
- You define your yaml configurations and icons 
- Only the needed files, icons and configurations are loaded into RAM 
- The software then efficiently runs in background updating your buttons and responding to state changes of the buttons 
- Performance hit is expected to be under 0.1%, while **updating 20x per second**
- You can change the update rate in the `main.py`

### Key Creation and Configuration
**Refer to the `B737-800X/README.md` for a guide on how to create/edit buttons.**

### What is planned / WIP?
- More types of labels
- Own X-Plane UDP handler
- Multi deck support

### Known Issues
- There is currently a bug in **pyxpudpserver** that sometimes causes the dataref updating of buttons to
freeze (giving you a message:
`
RuntimeError: dictionary changed size during iteration
`

    The proposed solution is to use locking instead of simple if condition in its main lib file.

    You can swap the `pyxpudpserver/XPlaneUDPServer.py` file from 
[forked version of pyxpudpserver](https://github.com/wortelus/pyXPUDPServer) after you install the dependencies
to apply the proposed unofficial solution. You can find its location in `xplane-streamdec/venv` (if using venv) or
in global `Python\Python310\Lib\site-packages\pyxpudpserver` found by executing following Python command:
```
>>> import os
>>> print(os.path)
```

- There is a known risk of crashes associated with running Stream Deck through USB hubs:
```
    raise TransportError("Failed to write out report (%d)" % result)
StreamDeck.Transport.Transport.TransportError: Failed to write out report (-1) 
```

### Acknowledgments
*IBMPlexMono-Bold.ttf* - Licensed under SIL Open Font License (OFL) 

IBM Plex™ is an international typeface family designed by Mike Abbink, IBM BX&D, in collaboration with Bold Monday, 
an independent Dutch type foundry. Plex was designed to capture IBM’s spirit and history, and to illustrate the 
unique relationship between mankind and machine—a principal theme for IBM since the turn of the century.

## License
BSD 2-Clause License

Copyright (c) 2022, Daniel Slavík All rights reserved.

www.wortelus.eu
