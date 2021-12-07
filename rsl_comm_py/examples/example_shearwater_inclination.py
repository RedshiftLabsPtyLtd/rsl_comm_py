#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 31 March 2020

import logging
import os.path
import sys

from rsl_comm_py.shearwater_serial import ShearWaterSerial


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        format='[%(asctime)s.%(msecs)03d] [%(levelname)-8s]:  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(f'{os.path.basename(__file__)}.log'),
            logging.StreamHandler(sys.stdout),
        ])
    script_dir = os.path.dirname(__file__)
    device_file = os.path.join(script_dir, os.pardir, "um7py", "um7_A500CNHD.json")
    shearwater = ShearWaterSerial(device=device_file)

    print(f"\n========== INCLINATION ===================================")
    for _ in range(10000):
        print(f"dreg_velocity_time            : {shearwater.dreg_velocity_time[1]}")


