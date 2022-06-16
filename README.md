# X-Plane Stream Deck Manager
This is a manager for X-Plane <-> Elgato Stream Deck connection. Developed on Python 3.10 for X-Plane 11.51.

**Currently supporting**:
- Strem Deck Mini
- Stream Deck MK1 (MK2 should work too)
- Stream Deck XL (tested)

### Features:
- Directories
- Toggle Actions (single command)
- Multiple Command Actions
- Supporting Multi-position switches (e.g. ENGINE START / IGNITION on 737)
- On-Off Actions
- Sync with X-Plane's dataref to visually depict the actual state
- Multiple Dataref States with each custom key image
- Multi-Deck support (WIP)

All of these features can be configurated in simple YAML configs. YAML is very easy to use
and simple format similar to JSON, but more human-readable and harder to cause a syntax error in.

### How it works
The streamdeck Python library provides modular access.

### Key Creation and Configuration
1. Create empty directory with any name (ex. B737), that name will need to be referenced in config.yaml. 
All your images, actions.yaml and other keysets (directories) will take place here
2. Actions.yaml resembles the root directory of the stream deck keys
3. xyz.yaml, ABC.yaml, 123.yaml... *.yaml resembles the keysets (directories),
you're going to reference the directories by their name in key configs with keys attributed as "directory".
5. Keyset can be left unreferenced, it will be simply ignored and NOT loaded into memory.

## Dependencies
- NumPy
- PyYAML
- streamdeck - Windows requires additional DLL's installed in its root Python executable directory
- Pillow

## License
MIT License 3.0

by wortelus, no warranty provided