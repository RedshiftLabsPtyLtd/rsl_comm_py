#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 3 May 2020

import logging
import sys

from pathlib import Path

from rsl_comm_py.shearwater_serial import ShearWaterSerial


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        format='[%(asctime)s.%(msecs)03d] [%(levelname)-8s]:  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(f'{Path(__file__).stem}.log', mode='w'),
            logging.StreamHandler(sys.stdout),
        ])
    script_dir = Path(__file__).parent
    device_file = script_dir.parent / "rsl_A500CNHD.json"
    shearwater = ShearWaterSerial(device=device_file)

    print(f"\n========== COMMAND REGISTERS ===================================")
    print(f"get_fw_build_id               : {shearwater.get_fw_build_id}")
    print(f"get_fw_build_version          : {shearwater.get_fw_build_version}")
    print(f"board_unique_id_1             : {shearwater.board_unique_id_1}")
    print(f"board_unique_id_2             : {shearwater.board_unique_id_2}")
    print(f"protocol_version              : {shearwater.protocol_version}")

