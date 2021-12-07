#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 3 May 2020


import logging
import os.path
import sys

from rsl_comm_py.shearwater_serial import ShearWaterSerial


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
    device_file = os.path.join(script_dir, os.pardir, "um7py", "um7_A500CNHD.json")
    shearwater = ShearWaterSerial(device=device_file)

    for packet in shearwater.recv_euler_broadcast(num_packets=100):
        logging.warning(packet)

