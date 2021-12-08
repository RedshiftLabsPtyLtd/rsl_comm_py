#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 3 May 2020

import logging
import sys

from pathlib import Path

from rsl_comm_py.shearwater_spi import ShearWaterSpiUsbIss


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
    shearwater = ShearWaterSpiUsbIss(device=device_file)
    print(f"\n========== CONFIG REGISTERS ===================================")
    print(f"creg_com_settings             : {shearwater.creg_com_settings}")
    print(f"creg_com_rates1               : {shearwater.creg_com_rates1}")
    print(f"creg_com_rates2               : {shearwater.creg_com_rates2}")
    print(f"creg_com_rates3               : {shearwater.creg_com_rates3}")
    print(f"creg_com_rates4               : {shearwater.creg_com_rates4}")
    print(f"creg_com_rates5               : {shearwater.creg_com_rates5}")
    print(f"creg_com_rates6               : {shearwater.creg_com_rates6}")
    print(f"creg_com_rates7               : {shearwater.creg_com_rates7}")
    print(f"creg_misc_settings            : {shearwater.creg_misc_settings}")
    print(f"creg_gyro_1_meas_range        : {shearwater.creg_gyro_1_meas_range}")
    print(f"creg_gyro_1_trim_x            : {shearwater.creg_gyro_1_trim_x}")
    print(f"creg_gyro_1_trim_y            : {shearwater.creg_gyro_1_trim_y}")
    print(f"creg_gyro_1_trim_z            : {shearwater.creg_gyro_1_trim_z}")
    print(f"creg_gyro_2_meas_range        : {shearwater.creg_gyro_2_meas_range}")
    print(f"creg_gyro_2_trim_x            : {shearwater.creg_gyro_2_trim_x}")
    print(f"creg_gyro_2_trim_y            : {shearwater.creg_gyro_2_trim_y}")
    print(f"creg_gyro_2_trim_z            : {shearwater.creg_gyro_2_trim_z}")
    print(f"creg_mag_1_cal1_1             : {shearwater.creg_mag_1_cal1_1}")
    print(f"creg_mag_1_cal1_2             : {shearwater.creg_mag_1_cal1_2}")
    print(f"creg_mag_1_cal1_3             : {shearwater.creg_mag_1_cal1_3}")
    print(f"creg_mag_1_cal2_1             : {shearwater.creg_mag_1_cal2_1}")
    print(f"creg_mag_1_cal2_2             : {shearwater.creg_mag_1_cal2_2}")
    print(f"creg_mag_1_cal2_3             : {shearwater.creg_mag_1_cal2_3}")
    print(f"creg_mag_1_cal3_1             : {shearwater.creg_mag_1_cal3_1}")
    print(f"creg_mag_1_cal3_2             : {shearwater.creg_mag_1_cal3_2}")
    print(f"creg_mag_1_cal3_3             : {shearwater.creg_mag_1_cal3_3}")
    print(f"creg_mag_1_bias_x             : {shearwater.creg_mag_1_bias_x}")
    print(f"creg_mag_1_bias_y             : {shearwater.creg_mag_1_bias_y}")
    print(f"creg_mag_1_bias_z             : {shearwater.creg_mag_1_bias_z}")
    print(f"creg_mag_2_cal1_1             : {shearwater.creg_mag_2_cal1_1}")
    print(f"creg_mag_2_cal1_2             : {shearwater.creg_mag_2_cal1_2}")
    print(f"creg_mag_2_cal1_3             : {shearwater.creg_mag_2_cal1_3}")
    print(f"creg_mag_2_cal2_1             : {shearwater.creg_mag_2_cal2_1}")
    print(f"creg_mag_2_cal2_2             : {shearwater.creg_mag_2_cal2_2}")
    print(f"creg_mag_2_cal2_3             : {shearwater.creg_mag_2_cal2_3}")
    print(f"creg_mag_2_cal3_1             : {shearwater.creg_mag_2_cal3_1}")
    print(f"creg_mag_2_cal3_2             : {shearwater.creg_mag_2_cal3_2}")
    print(f"creg_mag_2_cal3_3             : {shearwater.creg_mag_2_cal3_3}")
    print(f"creg_mag_2_bias_x             : {shearwater.creg_mag_2_bias_x}")
    print(f"creg_mag_2_bias_y             : {shearwater.creg_mag_2_bias_y}")
    print(f"creg_mag_2_bias_z             : {shearwater.creg_mag_2_bias_z}")
    print(f"creg_accel_1_meas_range       : {shearwater.creg_accel_1_meas_range}")
    print(f"creg_accel_1_cal1_1           : {shearwater.creg_accel_1_cal1_1}")
    print(f"creg_accel_1_cal1_2           : {shearwater.creg_accel_1_cal1_2}")
    print(f"creg_accel_1_cal1_3           : {shearwater.creg_accel_1_cal1_3}")
    print(f"creg_accel_1_cal2_1           : {shearwater.creg_accel_1_cal2_1}")
    print(f"creg_accel_1_cal2_2           : {shearwater.creg_accel_1_cal2_2}")
    print(f"creg_accel_1_cal2_3           : {shearwater.creg_accel_1_cal2_3}")
    print(f"creg_accel_1_cal3_1           : {shearwater.creg_accel_1_cal3_1}")
    print(f"creg_accel_1_cal3_2           : {shearwater.creg_accel_1_cal3_2}")
    print(f"creg_accel_1_cal3_3           : {shearwater.creg_accel_1_cal3_3}")
    print(f"creg_accel_1_bias_x           : {shearwater.creg_accel_1_bias_x}")
    print(f"creg_accel_1_bias_y           : {shearwater.creg_accel_1_bias_y}")
    print(f"creg_accel_1_bias_z           : {shearwater.creg_accel_1_bias_z}")