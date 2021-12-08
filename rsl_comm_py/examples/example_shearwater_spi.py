#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 31 March 2021

import logging
import sys

from pathlib import Path

from rsl_comm_py.shearwater_serial import ShearWaterSerial
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

    shearwater_spi = ShearWaterSpiUsbIss(port='/dev/ttyACM0')
    shearwater_serial = ShearWaterSerial(device=device_file)

    print(f"\n========== DATA REGISTERS ===================================")
    for _ in range(100):
        print(f"dreg_mag_1_raw_x_spi            : {shearwater_spi.dreg_mag_1_raw_x[0].raw_value}")
        print(f"dreg_mag_1_raw_x_serial         : {shearwater_serial.dreg_mag_1_raw_x[0].raw_value}")
        print(f"dreg_mag_1_raw_y_spi            : {shearwater_spi.dreg_mag_1_raw_y[0].raw_value}")
        print(f"dreg_mag_1_raw_y_serial         : {shearwater_serial.dreg_mag_1_raw_y[0].raw_value}")
        print(f"dreg_mag_1_raw_z_spi            : {shearwater_spi.dreg_mag_1_raw_z[0].raw_value}")
        print(f"dreg_mag_1_raw_z_serial         : {shearwater_serial.dreg_mag_1_raw_z[0].raw_value}")
        print(f"dreg_mag_1_raw_time_spi         : {shearwater_spi.dreg_mag_1_raw_time[0].raw_value}")
        print(f"dreg_mag_1_raw_time_serial      : {shearwater_serial.dreg_mag_1_raw_time[0].raw_value}")
        print(f"dreg_mag_2_raw_xy_spi           : {shearwater_spi.dreg_mag_2_raw_xy[0].raw_value}")
        print(f"dreg_mag_2_raw_xy_serial        : {shearwater_serial.dreg_mag_2_raw_xy[0].raw_value}")
        print(f"dreg_mag_2_raw_z_spi            : {shearwater_spi.dreg_mag_2_raw_z[0].raw_value}")
        print(f"dreg_mag_2_raw_z_serial         : {shearwater_serial.dreg_mag_2_raw_z[0].raw_value}")
        print(f"dreg_mag_2_raw_time_spi         : {shearwater_spi.dreg_mag_2_raw_time[0].raw_value}")
        print(f"dreg_mag_2_raw_time_serial      : {shearwater_serial.dreg_mag_2_raw_time[0].raw_value}")
        print(f"dreg_temperature_spi            : {shearwater_spi.dreg_temperature[0].raw_value}")
        print(f"dreg_temperature_serial         : {shearwater_serial.dreg_temperature[0].raw_value}")
        print(f"dreg_temperature_time_spi       : {shearwater_spi.dreg_temperature_time[0].raw_value}")
        print(f"dreg_temperature_time_serial    : {shearwater_serial.dreg_temperature_time[0].raw_value}")
        print(f"dreg_gyro_1_proc_x_spi          : {shearwater_spi.dreg_gyro_1_proc_x[0].raw_value}")
        print(f"dreg_gyro_1_proc_x_serial       : {shearwater_serial.dreg_gyro_1_proc_x[0].raw_value}")
        print(f"dreg_gyro_1_proc_y_spi          : {shearwater_spi.dreg_gyro_1_proc_y[0].raw_value}")
        print(f"dreg_gyro_1_proc_y_serial       : {shearwater_serial.dreg_gyro_1_proc_y[0].raw_value}")
        print(f"dreg_gyro_1_proc_z_spi          : {shearwater_spi.dreg_gyro_1_proc_z[0].raw_value}")
        print(f"dreg_gyro_1_proc_z_serial       : {shearwater_serial.dreg_gyro_1_proc_z[0].raw_value}")
        print(f"dreg_gyro_1_proc_time_spi       : {shearwater_spi.dreg_gyro_1_proc_time[0].raw_value}")
        print(f"dreg_gyro_1_proc_time_serial    : {shearwater_serial.dreg_gyro_1_proc_time[0].raw_value}")
        print(f"dreg_gyro_2_proc_x_spi          : {shearwater_spi.dreg_gyro_2_proc_x[0].raw_value}")
        print(f"dreg_gyro_2_proc_x_serial       : {shearwater_serial.dreg_gyro_2_proc_x[0].raw_value}")
        print(f"dreg_gyro_2_proc_y_spi          : {shearwater_spi.dreg_gyro_2_proc_y[0].raw_value}")
        print(f"dreg_gyro_2_proc_y_serial       : {shearwater_serial.dreg_gyro_2_proc_y[0].raw_value}")
        print(f"dreg_gyro_2_proc_z_spi          : {shearwater_spi.dreg_gyro_2_proc_z[0].raw_value}")
        print(f"dreg_gyro_2_proc_z_serial       : {shearwater_serial.dreg_gyro_2_proc_z[0].raw_value}")
        print(f"dreg_gyro_2_proc_time_spi       : {shearwater_spi.dreg_gyro_2_proc_time[0].raw_value}")
        print(f"dreg_gyro_2_proc_time_serial    : {shearwater_serial.dreg_gyro_2_proc_time[0].raw_value}")
        print(f"dreg_accel_1_proc_x_spi         : {shearwater_spi.dreg_accel_1_proc_x[0].raw_value}")
        print(f"dreg_accel_1_proc_x_serial      : {shearwater_serial.dreg_accel_1_proc_x[0].raw_value}")
        print(f"dreg_accel_1_proc_y_spi         : {shearwater_spi.dreg_accel_1_proc_y[0].raw_value}")
        print(f"dreg_accel_1_proc_y_serial      : {shearwater_serial.dreg_accel_1_proc_y[0].raw_value}")
        print(f"dreg_accel_1_proc_z_spi         : {shearwater_spi.dreg_accel_1_proc_z[0].raw_value}")
        print(f"dreg_accel_1_proc_z_serial      : {shearwater_serial.dreg_accel_1_proc_z[0].raw_value}")
        print(f"dreg_accel_1_proc_time_spi      : {shearwater_spi.dreg_accel_1_proc_time[0].raw_value}")
        print(f"dreg_accel_1_proc_time_serial   : {shearwater_serial.dreg_accel_1_proc_time[0].raw_value}")
        print(f"dreg_mag_1_proc_x_spi           : {shearwater_spi.dreg_mag_1_proc_x[0].raw_value}")
        print(f"dreg_mag_1_proc_x_serial        : {shearwater_serial.dreg_mag_1_proc_x[0].raw_value}")
        print(f"dreg_mag_1_proc_y_spi           : {shearwater_spi.dreg_mag_1_proc_y[0].raw_value}")
        print(f"dreg_mag_1_proc_y_serial        : {shearwater_serial.dreg_mag_1_proc_y[0].raw_value}")
        print(f"dreg_mag_1_proc_z_spi           : {shearwater_spi.dreg_mag_1_proc_z[0].raw_value}")
        print(f"dreg_mag_1_proc_z_serial        : {shearwater_serial.dreg_mag_1_proc_z[0].raw_value}")
        print(f"dreg_mag_1_norm_spi             : {shearwater_spi.dreg_mag_1_norm[0].raw_value}")
        print(f"dreg_mag_1_norm_serial          : {shearwater_serial.dreg_mag_1_norm[0].raw_value}")
        print(f"dreg_mag_1_proc_time_spi        : {shearwater_spi.dreg_mag_1_proc_time[0].raw_value}")
        print(f"dreg_mag_1_proc_time_serial     : {shearwater_serial.dreg_mag_1_proc_time[0].raw_value}")
        print(f"dreg_mag_2_proc_x_spi           : {shearwater_spi.dreg_mag_2_proc_x[0].raw_value}")
        print(f"dreg_mag_2_proc_x_serial        : {shearwater_serial.dreg_mag_2_proc_x[0].raw_value}")
        print(f"dreg_mag_2_proc_y_spi           : {shearwater_spi.dreg_mag_2_proc_y[0].raw_value}")
        print(f"dreg_mag_2_proc_y_serial        : {shearwater_serial.dreg_mag_2_proc_y[0].raw_value}")
        print(f"dreg_mag_2_proc_z_spi           : {shearwater_spi.dreg_mag_2_proc_z[0].raw_value}")
        print(f"dreg_mag_2_proc_z_serial        : {shearwater_serial.dreg_mag_2_proc_z[0].raw_value}")
        print(f"dreg_mag_2_norm_spi             : {shearwater_spi.dreg_mag_2_norm[0].raw_value}")
        print(f"dreg_mag_2_norm_serial          : {shearwater_serial.dreg_mag_2_norm[0].raw_value}")
        print(f"dreg_mag_2_proc_time_spi        : {shearwater_spi.dreg_mag_2_proc_time[0].raw_value}")
        print(f"dreg_mag_2_proc_time_serial     : {shearwater_serial.dreg_mag_2_proc_time[0].raw_value}")
        print(f"dreg_quat_ab_spi                : {shearwater_spi.dreg_quat_ab[0].raw_value}")
        print(f"dreg_quat_ab_serial             : {shearwater_serial.dreg_quat_ab[0].raw_value}")
        print(f"dreg_quat_cd_spi                : {shearwater_spi.dreg_quat_cd[0].raw_value}")
        print(f"dreg_quat_cd_serial             : {shearwater_serial.dreg_quat_cd[0].raw_value}")
        print(f"dreg_quat_time_spi              : {shearwater_spi.dreg_quat_time[0].raw_value}")
        print(f"dreg_quat_time_serial           : {shearwater_serial.dreg_quat_time[0].raw_value}")
        print(f"dreg_euler_phi_theta_spi        : {shearwater_spi.dreg_euler_phi_theta[0].raw_value}")
        print(f"dreg_euler_phi_theta_serial     : {shearwater_serial.dreg_euler_phi_theta[0].raw_value}")
        print(f"dreg_euler_psi_spi              : {shearwater_spi.dreg_euler_psi[0].raw_value}")
        print(f"dreg_euler_psi_serial           : {shearwater_serial.dreg_euler_psi[0].raw_value}")
        print(f"dreg_euler_phi_theta_dot_spi    : {shearwater_spi.dreg_euler_phi_theta_dot[0].raw_value}")
        print(f"dreg_euler_phi_theta_dot_serial : {shearwater_serial.dreg_euler_phi_theta_dot[0].raw_value}")
        print(f"dreg_euler_psi_dot_spi          : {shearwater_spi.dreg_euler_psi_dot[0].raw_value}")
        print(f"dreg_euler_psi_dot_serial       : {shearwater_serial.dreg_euler_psi_dot[0].raw_value}")
        print(f"dreg_euler_time_spi             : {shearwater_spi.dreg_euler_time[0].raw_value}")
        print(f"dreg_euler_time_serial          : {shearwater_serial.dreg_euler_time[0].raw_value}")

