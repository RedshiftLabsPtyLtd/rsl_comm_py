#!/usr/bin/env python

# Author: Dr. Konstantin Selyunin
# License: MIT

import argparse
import json
import sys

from argparse import RawTextHelpFormatter


def um7_autodetect(file_name=None):
    """
    :param file_name: by default ID of sensor will be assigned
    :return: id file will be created in target directory
    """
    json_config = {}
    if sys.platform.startswith('win32'):
        from serial.tools import list_ports
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
                    file_name = f"um7_{json_config['ID_SERIAL_SHORT']}.json"
                with open(file_name, 'w') as fp:
                    json.dump(json_config, fp, indent=2)
                return True, json_config
        # none of the devices was FTDI
        return False, {}
    else:
        import pyudev
        context = pyudev.Context()
        udev_keys = ['ID_VENDOR', 'ID_SERIAL_SHORT', 'ID_MODEL']
        for device in context.list_devices(subsystem='tty'):
            if device.get('ID_VENDOR') == 'FTDI':
                for key in udev_keys:
                    json_config[key] = device.get(key)
                if file_name is None:
                    file_name = f"um7_{json_config['ID_SERIAL_SHORT']}.json"
                with open(file_name, 'w') as fp:
                    json.dump(json_config, fp, indent=2)
                return True, json_config
        else:
            return False, {}


description = \
"""
Store UM7 udev parameters on a Linux-based system.
UM7 uses FTDI chip, and has no specific
descriptor information to differentiate itself 
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
2. Connect UM7 sensor;
3. Launch the script (with additional -f flag, which specifies file name);
4. The file `um7_[serial_id].json` containing device 
specific information appears on success.

This file will be used by UM7 drivers
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--file', type=str, help='')
    args = parser.parse_args(sys.argv[1:])
    ok, config = um7_autodetect(args.file)
    print(config)
    if not ok:
        print("FAILED to store ID of UM7! Check whether the sensor is connected!")
