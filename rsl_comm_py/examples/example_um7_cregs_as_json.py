#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 8 December 2021

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
            logging.FileHandler(f'{Path(__file__).stem}.log', mode='w'),
            logging.StreamHandler(sys.stdout),
        ])
    script_dir = Path(__file__).parent
    device_file = script_dir.parent / "rsl_A500CNP8.json"
    um7 = UM7Serial(device=device_file)
    creg_register_values = []
    for reg in um7.svd_parser.cregs:
        name = reg.name.lower()
        reg, *_ = getattr(um7, name)
        creg_register_values.append(reg.as_dict())

    creg_register_str = json.dumps(creg_register_values, indent=2)
    json_file_name = f'um7_cregs.json'
    with open(json_file_name, 'w') as fd:
        fd.write(creg_register_str)
    logging.warning(f'OK: Configuration settings written to file: `{json_file_name}`')
