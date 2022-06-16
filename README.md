# X-Plane Stream Deck Manager
This is a manager for X-Plane <-> Elgato Stream Deck connection. Developed on Python 3.10 for X-Plane 11.51.

This software includes rich set of features for robust control of the simulator cockpit.

Developed with the idea taking away mouse controlling of most of the cockpit, 
works best together with other simulator peripherals (e.g. radio, A/P panel etc.)

**Currently supporting**:
- Stream Deck Mini
- Stream Deck MK1 (MK2 should work too)
- Stream Deck XL (tested)

### Features:
- Directories
- Toggle actions (single command)
- Multiple command actions
- Supporting multi-position switches (e.g. ENGINE START / IGNITION on 737) control via single button
- On-Off actions
- Sync with X-Plane's dataref to visually depict the actual state
- Multiple dataref states with each custom key image
- Multi-Deck support (WIP)

All of these features can be configurated in simple YAML configs. YAML is very easy to use
and simple format similar to JSON, but more human-readable and harder to cause a syntax error in.

### How it works
The streamdeck Python library provides modular access.

### Key Creation and Configuration
1. Create empty directory with any name (ex. B737), that name will need to be referenced in config.yaml. 
Your actions.yaml and other keysets (directories) will take place here.
Actual icons as files are going to be put under 'icons' directory.
2. The actions.yaml resembles the root directory of the stream deck keys.
3. xyz.yaml, ABC.yaml, 123.yaml... *.yaml resembles the keysets (directories),
you're going to reference the directories by their name in key configs with keys attributed as "dir".
4. Keyset can be left unreferenced, it will be simply ignored and NOT loaded into memory.

## Dependencies
- NumPy
- PyYAML
- streamdeck - Windows requires additional DLL's installed in its root Python executable directory
- Pillow
- pyxpudpserver

## License
Mozilla Public License 2.0

by wortelus, no warranty provided

www.wortelus.eu