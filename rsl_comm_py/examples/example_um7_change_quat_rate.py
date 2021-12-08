#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 27 November 2020


import logging
import os.path
import sys

from rsl_comm_py.um7_serial import UM7Serial


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        format='[%(asctime)s.%(msecs)03d]: %(message)s',
        datefmt='%H:%M:%S',
        handlers=[
            logging.FileHandler(f'{os.path.basename(__file__)}.log', mode='w'),
            logging.StreamHandler(sys.stdout),
        ])
    script_dir = os.path.dirname(__file__)
    device_file = os.path.join(script_dir, os.pardir, "um7py", "um7_A500CNP8.json")
    um7 = UM7Serial(device=device_file)
    creg_com_rates5, *_ = um7.creg_com_rates5
    print("creg_com_rates5: {}".format(creg_com_rates5))
    creg_com_settings, *_ = um7.creg_com_settings
    print("um7 creg_com_settings: {}".format(creg_com_settings))

    print(f"setting new quat rate: 20 Hz")
    # look at the register description -->
    # https://docs.redshiftlabs.com.au/register_map_current.html#creg-com-rates5
    # we are going to set the quaternion transmission rate to 20 Hz
    creg_com_rates5.set_field_value(QUAT_RATE=20)
    # we have now set a raw register value, let us write it in the sensor
    print(creg_com_rates5)
    um7.creg_com_rates5 = creg_com_rates5.raw_value

    # setting quaternion fusion
    creg_misc_settings, *_ = um7.creg_misc_settings
    creg_misc_settings.set_field_value(Q=1)
    um7.creg_misc_settings = creg_misc_settings.raw_value

    from time import sleep
    print("Sleeping 5 s... Zz")
    sleep(5)

    for packet in um7.recv_quaternion_broadcast(num_packets=100):
        logging.warning(packet)