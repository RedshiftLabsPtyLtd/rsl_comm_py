#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 3 May 2020
# Example: reading broadcast packet of processed sensor data

import logging
import sys

from pathlib import Path

from rsl_comm_py.shearwater_serial import ShearWaterSerial


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        format='[%(asctime)s.%(msecs)03d]: %(message)s',
        datefmt='%H:%M:%S',
        handlers=[
            logging.FileHandler(f'{Path(__file__).stem}.log', mode='w'),
            logging.StreamHandler(sys.stdout),
        ])
    script_dir = Path(__file__).parent
    # NOTE: specify path to YOUR device file below (see README how to create such file):
    device_file = script_dir.parent / "rsl_A500CNHD.json"
    shearwater = ShearWaterSerial(device=device_file)

    for packet in shearwater.recv_all_proc_broadcast(num_packets=100):
        logging.warning(packet)
