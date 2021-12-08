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

    print(f"\n========== DATA REGISTERS ===================================")
    print(f"dreg_health                   : {shearwater.dreg_health}")
    print(f"dreg_gyro_1_raw_xy            : {shearwater.dreg_gyro_1_raw_xy}")
    print(f"dreg_gyro_1_raw_z             : {shearwater.dreg_gyro_1_raw_z}")
    print(f"dreg_gyro_1_raw_time          : {shearwater.dreg_gyro_1_raw_time}")
    print(f"dreg_gyro_2_raw_xy            : {shearwater.dreg_gyro_2_raw_xy}")
    print(f"dreg_gyro_2_raw_z             : {shearwater.dreg_gyro_2_raw_z}")
    print(f"dreg_gyro_2_raw_time          : {shearwater.dreg_gyro_2_raw_time}")
    print(f"dreg_accel_1_raw_xy           : {shearwater.dreg_accel_1_raw_xy}")
    print(f"dreg_accel_1_raw_z            : {shearwater.dreg_accel_1_raw_z}")
    print(f"dreg_accel_1_raw_time         : {shearwater.dreg_accel_1_raw_time}")
    print(f"dreg_mag_1_raw_x              : {shearwater.dreg_mag_1_raw_x}")
    print(f"dreg_mag_1_raw_y              : {shearwater.dreg_mag_1_raw_y}")
    print(f"dreg_mag_1_raw_z              : {shearwater.dreg_mag_1_raw_z}")
    print(f"dreg_mag_1_raw_time           : {shearwater.dreg_mag_1_raw_time}")
    print(f"dreg_mag_2_raw_xy             : {shearwater.dreg_mag_2_raw_xy}")
    print(f"dreg_mag_2_raw_z              : {shearwater.dreg_mag_2_raw_z}")
    print(f"dreg_mag_2_raw_time           : {shearwater.dreg_mag_2_raw_time}")
    print(f"dreg_temperature              : {shearwater.dreg_temperature}")
    print(f"dreg_temperature_time         : {shearwater.dreg_temperature_time}")
    print(f"dreg_gyro_1_proc_x            : {shearwater.dreg_gyro_1_proc_x}")
    print(f"dreg_gyro_1_proc_y            : {shearwater.dreg_gyro_1_proc_y}")
    print(f"dreg_gyro_1_proc_z            : {shearwater.dreg_gyro_1_proc_z}")
    print(f"dreg_gyro_1_proc_time         : {shearwater.dreg_gyro_1_proc_time}")
    print(f"dreg_gyro_2_proc_x            : {shearwater.dreg_gyro_2_proc_x}")
    print(f"dreg_gyro_2_proc_y            : {shearwater.dreg_gyro_2_proc_y}")
    print(f"dreg_gyro_2_proc_z            : {shearwater.dreg_gyro_2_proc_z}")
    print(f"dreg_gyro_2_proc_time         : {shearwater.dreg_gyro_2_proc_time}")
    print(f"dreg_accel_1_proc_x           : {shearwater.dreg_accel_1_proc_x}")
    print(f"dreg_accel_1_proc_y           : {shearwater.dreg_accel_1_proc_y}")
    print(f"dreg_accel_1_proc_z           : {shearwater.dreg_accel_1_proc_z}")
    print(f"dreg_accel_1_proc_time        : {shearwater.dreg_accel_1_proc_time}")
    print(f"dreg_mag_1_proc_x             : {shearwater.dreg_mag_1_proc_x}")
    print(f"dreg_mag_1_proc_y             : {shearwater.dreg_mag_1_proc_y}")
    print(f"dreg_mag_1_proc_z             : {shearwater.dreg_mag_1_proc_z}")
    print(f"dreg_mag_1_norm               : {shearwater.dreg_mag_1_norm}")
    print(f"dreg_mag_1_proc_time          : {shearwater.dreg_mag_1_proc_time}")
    print(f"dreg_mag_2_proc_x             : {shearwater.dreg_mag_2_proc_x}")
    print(f"dreg_mag_2_proc_y             : {shearwater.dreg_mag_2_proc_y}")
    print(f"dreg_mag_2_proc_z             : {shearwater.dreg_mag_2_proc_z}")
    print(f"dreg_mag_2_norm               : {shearwater.dreg_mag_2_norm}")
    print(f"dreg_mag_2_proc_time          : {shearwater.dreg_mag_2_proc_time}")
    print(f"dreg_quat_ab                  : {shearwater.dreg_quat_ab}")
    print(f"dreg_quat_cd                  : {shearwater.dreg_quat_cd}")
    print(f"dreg_quat_time                : {shearwater.dreg_quat_time}")
    print(f"dreg_euler_phi_theta          : {shearwater.dreg_euler_phi_theta}")
    print(f"dreg_euler_psi                : {shearwater.dreg_euler_psi}")
    print(f"dreg_euler_phi_theta_dot      : {shearwater.dreg_euler_phi_theta_dot}")
    print(f"dreg_euler_psi_dot            : {shearwater.dreg_euler_psi_dot}")
    print(f"dreg_euler_time               : {shearwater.dreg_euler_time}")
    print(f"dreg_position_north           : {shearwater.dreg_position_north}")
    print(f"dreg_position_east            : {shearwater.dreg_position_east}")
    print(f"dreg_position_up              : {shearwater.dreg_position_up}")
    print(f"dreg_position_time            : {shearwater.dreg_position_time}")
    print(f"dreg_velocity_north           : {shearwater.dreg_velocity_north}")
    print(f"dreg_velocity_east            : {shearwater.dreg_velocity_east}")
    print(f"dreg_velocity_up              : {shearwater.dreg_velocity_up}")
    print(f"dreg_velocity_time            : {shearwater.dreg_velocity_time}")
    print(f"dreg_gyro_1_bias_x            : {shearwater.dreg_gyro_1_bias_x}")
    print(f"dreg_gyro_1_bias_y            : {shearwater.dreg_gyro_1_bias_y}")
    print(f"dreg_gyro_1_bias_z            : {shearwater.dreg_gyro_1_bias_z}")
    print(f"dreg_gyro_2_bias_x            : {shearwater.dreg_gyro_2_bias_x}")
    print(f"dreg_gyro_2_bias_y            : {shearwater.dreg_gyro_2_bias_y}")
    print(f"dreg_gyro_2_bias_z            : {shearwater.dreg_gyro_2_bias_z}")

