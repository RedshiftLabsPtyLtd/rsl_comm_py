#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 31 May 2020
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
    um7 = UM7Serial(port_name='/dev/ttyUSB0')

    print("um7 firmware revision: {}".format(um7.get_fw_revision))
    # for packet in um7.recv_broadcast(num_packets=1000):
    #     logging.warning(packet)

