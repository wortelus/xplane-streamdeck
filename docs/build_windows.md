# Building Windows Executable
This guide will help you build the Windows executable for the _xplane-streamdeck_.

## Prerequisites
- Python 3.10 or later
- pip

## Building on Windows
- Run `build-windows.bat`
- Download HIDAPI DLL's from the [official documentation](https://python-elgato-streamdeck.readthedocs.io/en/stable/pages/backend_libusb_hidapi.html)
- Place the DLL's in the same directory as the executable
- Run the executable, the script will automatically detect the Stream Deck