#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 26 March 2022

import logging
import sys

from pathlib import Path

from rsl_comm_py.um7_serial import UM7Serial
from rsl_comm_py.um7_spi import UM7SpiUsbIss


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

    um7_spi = UM7SpiUsbIss(port='/dev/ttyACM0')
    um7_serial = UM7Serial(device=device_file)

    print(f"\n========== DATA REGISTERS ===================================")
    for _ in range(2):
        reg_read_spi = um7_spi.dreg_mag_raw_xy
        reg_read_uart = um7_spi.dreg_mag_raw_xy
        print(f"dreg_mag_raw_xy_spi             : x={reg_read_spi[1]:+04}, y={reg_read_spi[2]:+04}, raw={reg_read_spi[0].raw_value}")
        print(f"dreg_mag_raw_xy_serial          : {um7_serial.dreg_mag_raw_xy[0].raw_value}")
        print(f"dreg_mag_raw_z_spi              : {um7_spi.dreg_mag_raw_z[0].raw_value}")
        print(f"dreg_mag_raw_z_serial           : {um7_serial.dreg_mag_raw_z[0].raw_value}")
        print(f"dreg_mag_raw_time_spi           : {um7_spi.dreg_mag_raw_time[0].raw_value}")
        print(f"dreg_mag_raw_time_spi           : {um7_serial.dreg_mag_raw_time[0].raw_value}")
        # print(f"dreg_mag_1_raw_time_spi         : {um7_spi.dreg_mag_1_raw_time[0].raw_value}")
        # print(f"dreg_mag_1_raw_time_serial      : {um7_serial.dreg_mag_1_raw_time[0].raw_value}")
        # print(f"dreg_mag_2_raw_xy_spi           : {um7_spi.dreg_mag_2_raw_xy[0].raw_value}")
        # print(f"dreg_mag_2_raw_xy_serial        : {um7_serial.dreg_mag_2_raw_xy[0].raw_value}")
        # print(f"dreg_mag_2_raw_z_spi            : {um7_spi.dreg_mag_2_raw_z[0].raw_value}")
        # print(f"dreg_mag_2_raw_z_serial         : {um7_serial.dreg_mag_2_raw_z[0].raw_value}")
        # print(f"dreg_mag_2_raw_time_spi         : {um7_spi.dreg_mag_2_raw_time[0].raw_value}")
        # print(f"dreg_mag_2_raw_time_serial      : {um7_serial.dreg_mag_2_raw_time[0].raw_value}")
        # print(f"dreg_temperature_spi            : {um7_spi.dreg_temperature[0].raw_value}")
        # print(f"dreg_temperature_serial         : {um7_serial.dreg_temperature[0].raw_value}")
        # print(f"dreg_temperature_time_spi       : {um7_spi.dreg_temperature_time[0].raw_value}")
        # print(f"dreg_temperature_time_serial    : {um7_serial.dreg_temperature_time[0].raw_value}")
        # print(f"dreg_gyro_1_proc_x_spi          : {um7_spi.dreg_gyro_1_proc_x[0].raw_value}")
        # print(f"dreg_gyro_1_proc_x_serial       : {um7_serial.dreg_gyro_1_proc_x[0].raw_value}")
        # print(f"dreg_gyro_1_proc_y_spi          : {um7_spi.dreg_gyro_1_proc_y[0].raw_value}")
        # print(f"dreg_gyro_1_proc_y_serial       : {um7_serial.dreg_gyro_1_proc_y[0].raw_value}")
        # print(f"dreg_gyro_1_proc_z_spi          : {um7_spi.dreg_gyro_1_proc_z[0].raw_value}")
        # print(f"dreg_gyro_1_proc_z_serial       : {um7_serial.dreg_gyro_1_proc_z[0].raw_value}")
        # print(f"dreg_gyro_1_proc_time_spi       : {um7_spi.dreg_gyro_1_proc_time[0].raw_value}")
        # print(f"dreg_gyro_1_proc_time_serial    : {um7_serial.dreg_gyro_1_proc_time[0].raw_value}")
        # print(f"dreg_gyro_2_proc_x_spi          : {um7_spi.dreg_gyro_2_proc_x[0].raw_value}")
        # print(f"dreg_gyro_2_proc_x_serial       : {um7_serial.dreg_gyro_2_proc_x[0].raw_value}")
        # print(f"dreg_gyro_2_proc_y_spi          : {um7_spi.dreg_gyro_2_proc_y[0].raw_value}")
        # print(f"dreg_gyro_2_proc_y_serial       : {um7_serial.dreg_gyro_2_proc_y[0].raw_value}")
        # print(f"dreg_gyro_2_proc_z_spi          : {um7_spi.dreg_gyro_2_proc_z[0].raw_value}")
        # print(f"dreg_gyro_2_proc_z_serial       : {um7_serial.dreg_gyro_2_proc_z[0].raw_value}")
        # print(f"dreg_gyro_2_proc_time_spi       : {um7_spi.dreg_gyro_2_proc_time[0].raw_value}")
        # print(f"dreg_gyro_2_proc_time_serial    : {um7_serial.dreg_gyro_2_proc_time[0].raw_value}")
        # print(f"dreg_accel_1_proc_x_spi         : {um7_spi.dreg_accel_1_proc_x[0].raw_value}")
        # print(f"dreg_accel_1_proc_x_serial      : {um7_serial.dreg_accel_1_proc_x[0].raw_value}")
        # print(f"dreg_accel_1_proc_y_spi         : {um7_spi.dreg_accel_1_proc_y[0].raw_value}")
        # print(f"dreg_accel_1_proc_y_serial      : {um7_serial.dreg_accel_1_proc_y[0].raw_value}")
        # print(f"dreg_accel_1_proc_z_spi         : {um7_spi.dreg_accel_1_proc_z[0].raw_value}")
        # print(f"dreg_accel_1_proc_z_serial      : {um7_serial.dreg_accel_1_proc_z[0].raw_value}")
        # print(f"dreg_accel_1_proc_time_spi      : {um7_spi.dreg_accel_1_proc_time[0].raw_value}")
        # print(f"dreg_accel_1_proc_time_serial   : {um7_serial.dreg_accel_1_proc_time[0].raw_value}")
        # print(f"dreg_mag_1_proc_x_spi           : {um7_spi.dreg_mag_1_proc_x[0].raw_value}")
        # print(f"dreg_mag_1_proc_x_serial        : {um7_serial.dreg_mag_1_proc_x[0].raw_value}")
        # print(f"dreg_mag_1_proc_y_spi           : {um7_spi.dreg_mag_1_proc_y[0].raw_value}")
        # print(f"dreg_mag_1_proc_y_serial        : {um7_serial.dreg_mag_1_proc_y[0].raw_value}")
        # print(f"dreg_mag_1_proc_z_spi           : {um7_spi.dreg_mag_1_proc_z[0].raw_value}")
        # print(f"dreg_mag_1_proc_z_serial        : {um7_serial.dreg_mag_1_proc_z[0].raw_value}")
        # print(f"dreg_mag_1_norm_spi             : {um7_spi.dreg_mag_1_norm[0].raw_value}")
        # print(f"dreg_mag_1_norm_serial          : {um7_serial.dreg_mag_1_norm[0].raw_value}")
        # print(f"dreg_mag_1_proc_time_spi        : {um7_spi.dreg_mag_1_proc_time[0].raw_value}")
        # print(f"dreg_mag_1_proc_time_serial     : {um7_serial.dreg_mag_1_proc_time[0].raw_value}")
        # print(f"dreg_mag_2_proc_x_spi           : {um7_spi.dreg_mag_2_proc_x[0].raw_value}")
        # print(f"dreg_mag_2_proc_x_serial        : {um7_serial.dreg_mag_2_proc_x[0].raw_value}")
        # print(f"dreg_mag_2_proc_y_spi           : {um7_spi.dreg_mag_2_proc_y[0].raw_value}")
        # print(f"dreg_mag_2_proc_y_serial        : {um7_serial.dreg_mag_2_proc_y[0].raw_value}")
        # print(f"dreg_mag_2_proc_z_spi           : {um7_spi.dreg_mag_2_proc_z[0].raw_value}")
        # print(f"dreg_mag_2_proc_z_serial        : {um7_serial.dreg_mag_2_proc_z[0].raw_value}")
        # print(f"dreg_mag_2_norm_spi             : {um7_spi.dreg_mag_2_norm[0].raw_value}")
        # print(f"dreg_mag_2_norm_serial          : {um7_serial.dreg_mag_2_norm[0].raw_value}")
        # print(f"dreg_mag_2_proc_time_spi        : {um7_spi.dreg_mag_2_proc_time[0].raw_value}")
        # print(f"dreg_mag_2_proc_time_serial     : {um7_serial.dreg_mag_2_proc_time[0].raw_value}")
        # print(f"dreg_quat_ab_spi                : {um7_spi.dreg_quat_ab[0].raw_value}")
        # print(f"dreg_quat_ab_serial             : {um7_serial.dreg_quat_ab[0].raw_value}")
        # print(f"dreg_quat_cd_spi                : {um7_spi.dreg_quat_cd[0].raw_value}")
        # print(f"dreg_quat_cd_serial             : {um7_serial.dreg_quat_cd[0].raw_value}")
        # print(f"dreg_quat_time_spi              : {um7_spi.dreg_quat_time[0].raw_value}")
        # print(f"dreg_quat_time_serial           : {um7_serial.dreg_quat_time[0].raw_value}")
        # print(f"dreg_euler_phi_theta_spi        : {um7_spi.dreg_euler_phi_theta[0].raw_value}")
        # print(f"dreg_euler_phi_theta_serial     : {um7_serial.dreg_euler_phi_theta[0].raw_value}")
        # print(f"dreg_euler_psi_spi              : {um7_spi.dreg_euler_psi[0].raw_value}")
        # print(f"dreg_euler_psi_serial           : {um7_serial.dreg_euler_psi[0].raw_value}")
        # print(f"dreg_euler_phi_theta_dot_spi    : {um7_spi.dreg_euler_phi_theta_dot[0].raw_value}")
        # print(f"dreg_euler_phi_theta_dot_serial : {um7_serial.dreg_euler_phi_theta_dot[0].raw_value}")
        # print(f"dreg_euler_psi_dot_spi          : {um7_spi.dreg_euler_psi_dot[0].raw_value}")
        # print(f"dreg_euler_psi_dot_serial       : {um7_serial.dreg_euler_psi_dot[0].raw_value}")
        # print(f"dreg_euler_time_spi             : {um7_spi.dreg_euler_time[0].raw_value}")
        # print(f"dreg_euler_time_serial          : {um7_serial.dreg_euler_time[0].raw_value}")

