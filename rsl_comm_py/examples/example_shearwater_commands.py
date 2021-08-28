#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 3 May 2020

import logging
import os.path
import sys

from um7py.shearwater_serial import ShearWaterSerial


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

    print(f"\n========== COMMAND REGISTERS ===================================")
    print(f"get_fw_build_id               : {shearwater.get_fw_build_id}")
    print(f"get_fw_build_version          : {shearwater.get_fw_build_version}")
    print(f"board_unique_id_1             : {shearwater.board_unique_id_1}")
    print(f"board_unique_id_2             : {shearwater.board_unique_id_2}")
    print(f"protocol_version              : {shearwater.protocol_version}")

