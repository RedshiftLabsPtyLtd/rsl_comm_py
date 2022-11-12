#!/usr/bin/env python3
# Author: Eron, Dr. Konstantin Selyunin
# License: MIT
# Date: 12 November 2022

import logging
import sys

from pathlib import Path

from rsl_comm_py.shearwater_serial import ShearWaterSerial
from rsl_comm_py.shearwater_spi import ShearWaterSpiUsbIss
from time import sleep


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

    for run_idx in range(10):
        shearwater_spi = ShearWaterSpiUsbIss(port='/dev/ttyACM0')
        shearwater_serial = ShearWaterSerial(device=device_file)
        print(f"\n========== RUN {run_idx} ===================================")
        for _ in range(100):
            print(f"dreg_mag_1_raw_x_spi            : {shearwater_spi.dreg_mag_1_raw_x[0].raw_value}")
            print(f"dreg_mag_1_raw_x_serial         : {shearwater_serial.dreg_mag_1_raw_x[0].raw_value}")
        shearwater_spi = None
        shearwater_serial = None
        sleep(1)
