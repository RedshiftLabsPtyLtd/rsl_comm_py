#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 19 August 2020

import logging
import sys
import json

from pathlib import Path

from rsl_comm_py.um7_serial import UM7Serial


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        format='[%(asctime)s.%(msecs)03d] [%(levelname)-8s]:  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(f'{Path(__file__).stem}.log'),
            logging.StreamHandler(sys.stdout),
        ])
    script_dir = Path(__file__).parent
    device_file = script_dir.parent / "rsl_A500CNP8.json"
    um7 = UM7Serial(device=device_file)
    hidden_register_values = []
    um7.hidden_accel_variance = 55.77  # comment out later to check if flashing succeeded
    um7.hidden_gyro_variance = 23.23  # comment out later to check if flashing succeeded
    um7.flash_commit = 1  # comment out later to check if flashing succeeded

    for reg in um7.svd_parser.hidden_regs:
        name = reg.name.lower()
        reg, *_ = getattr(um7, name)
        hidden_register_values.append(reg.as_dict())

    hidden_register_str = json.dumps(hidden_register_values, indent=2)
    json_file_name = f'um7_hidden.json'
    with open(json_file_name, 'w') as fd:
        fd.write(hidden_register_str)

    logging.warning(f'OK: Hidden registers content written to file: `{json_file_name}`')

