#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 23 Dec 2020
# Modified: 08 December 2021


import logging
import sys

from pathlib import Path

from rsl_comm_py.um7_serial import UM7Serial


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
    device_file = script_dir.parent / "rsl_A500CNP8.json"
    um7 = UM7Serial(device=device_file)

    for packet in um7.recv_quaternion_broadcast(num_packets=10):
        logging.warning(packet)

