#!/usr/bin/env python

# Author: Dr. Konstantin Selyunin
# License: MIT

import argparse
import json
import sys

from argparse import RawTextHelpFormatter
from serial.tools import list_ports
from typing import Dict, Tuple


def autodetect(file_name=None) -> Tuple[bool, Dict]:
    json_config = {}
    device_list = list_ports.comports()
    for device in device_list:
        # go through device list and stop on first FTDI device
        if device.manufacturer == "FTDI":
            # found something, add keys
            # device.device is the port name (COM4 for example)
            json_config['ID_VENDOR'] = device.manufacturer
            json_config['ID_SERIAL_SHORT'] = device.serial_number
            # don't know what the model should look like so were making it "pid:vid"
            json_config['ID_MODEL'] = '{0:04x}:{1:04x}'.format(device.vid, device.pid)
            if file_name is None:
                file_name = f"rsl_{json_config['ID_SERIAL_SHORT']}.json"
            with open(file_name, 'w') as fp:
                json.dump(json_config, fp, indent=2)
            return True, json_config
    # none of the devices was FTDI
    return False, {}


def autodetect_windows(file_name=None):
    return autodetect(file_name)


def autodetect_linux(file_name=None):
    return autodetect(file_name)


def autodetect_mac(file_name=None):
    return autodetect(file_name)


def rsl_autodetect(file_name=None) -> Tuple[bool, Dict]:
    """
    :param file_name: by default ID of sensor will be assigned
    :return: id file will be created in target directory
    """
    if sys.platform.startswith('win32'):
        return autodetect_windows(file_name)
    elif sys.platform.startswith('linux'):
        return autodetect_linux(file_name)
    elif sys.platform.startswith('darwin'):
        return autodetect_mac(file_name)


description = \
"""
Store RSL-sensor USB2Serial parameters on a Linux, Windows, Mac.
If RSL Board is connected via the USB2Serial FTDI chip, 
and has no specific descriptor information to differentiate itself 
from other FTDI devices (e.g. stepper motors or other
devices implementing USB2Serial connection). 

In order to differentiate these devices, we 
have this script, which searches for available 
devices and stores information in a .json file.
\n
Follow the procedure below:
-------------------------------
\n
1. Disconnect all the USB2Serial-related devices;
2. Connect RSL sensor;
3. Launch the script (with additional -f flag, which specifies file name);
4. The file `rsl_[serial_id].json` containing device 
specific information appears on success.

This file will be used by UM7, UM8, shearwater drivers
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--file', type=str, help='')
    args = parser.parse_args(sys.argv[1:])
    ok, config = rsl_autodetect(args.file)
    print(config)
    if not ok:
        print("FAILED to store ID of the RSL-Board! Check whether the sensor is connected!")
