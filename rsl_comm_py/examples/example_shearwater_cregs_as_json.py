#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 17 August 2020

import logging
import os.path
import sys
import json

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
    creg_register_values = []
    _, uid_1 = shearwater.board_unique_id_1
    for reg in shearwater.svd_parser.cregs:
        name = reg.name.lower()
        reg, *_ = getattr(shearwater, name)
        creg_register_values.append(reg.as_dict())

    creg_register_str = json.dumps(creg_register_values, indent=2)

    with open(f'shearwater_creg_{uid_1:0X}.json', 'w') as fd:
        fd.write(creg_register_str)

