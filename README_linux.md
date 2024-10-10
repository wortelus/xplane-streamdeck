# X-Plane Stream Deck Manager

## Linux installation
Linux installation is very straightforward. You only need:
- Python 3
- pip
- LibUSB HIDAPI library

You first install venv and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then you install the dependencies:

```bash
pip install -r requirements.txt
```

### LibUSB HIDAPI

The main difference is the **LibUSB HIDAPI** installation, which is really simple if
your distribution has the package in its repository.

For example, on **Debian 12** you can simply run the following command:

```bash
sudo apt-get install libhidapi-libusb0
```

and you are ready to go! If you are using a different distribution,
with a different package manager, the package name might be different.


### Usage

Don't forget to activate the virtual environment first:
```bash
source venv/bin/activate
```

Then you can run the script by:
```bash
python start.py
```