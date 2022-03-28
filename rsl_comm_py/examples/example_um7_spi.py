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
        """ Gyro Data """
        reg_read_spi = um7_spi.dreg_gyro_raw_xy
        reg_read_uart = um7_serial.dreg_gyro_raw_xy
        print(f"dreg_gyro_raw_xy_spi            : x={reg_read_spi[1]:+04}, y={reg_read_spi[2]:+04}, raw=0x{reg_read_spi[0].raw_value:08X} | {reg_read_spi[0].raw_value:08}")
        print(f"dreg_gyro_raw_xy_serial         : x={reg_read_uart[1]:+04}, y={reg_read_uart[2]:+04}, raw=0x{reg_read_uart[0].raw_value:08X} | {reg_read_uart[0].raw_value:08}")
        reg_read_spi = um7_spi.dreg_gyro_raw_z
        reg_read_uart = um7_serial.dreg_gyro_raw_z
        print(f"dreg_gyro_raw_z_spi             : z={reg_read_spi[1]:+04}, raw=0x{reg_read_spi[0].raw_value:08X} | {reg_read_spi[0].raw_value:08}")
        print(f"dreg_gyro_raw_z_serial          : z={reg_read_uart[1]:+04}, raw=0x{reg_read_uart[0].raw_value:08X} | {reg_read_uart[0].raw_value:08}")
        reg_read_spi = um7_spi.dreg_gyro_raw_time
        reg_read_uart = um7_serial.dreg_gyro_raw_time
        print(f"dreg_gyro_raw_time_spi          : Gt={reg_read_spi[1]:+04.6f}")
        print(f"dreg_gyro_raw_time_serial       : Gt={reg_read_uart[1]:+04.6f}")

        """ Accelerometer Data """
        reg_read_spi = um7_spi.dreg_accel_raw_xy
        reg_read_uart = um7_serial.dreg_accel_raw_xy
        print(f"dreg_accel_raw_xy_spi           : x={reg_read_spi[1]:+04}, y={reg_read_spi[2]:+04}, raw=0x{reg_read_spi[0].raw_value:08X} | {reg_read_spi[0].raw_value:08}")
        print(f"dreg_accel_raw_xy_serial        : x={reg_read_uart[1]:+04}, y={reg_read_uart[2]:+04}, raw=0x{reg_read_uart[0].raw_value:08X} | {reg_read_uart[0].raw_value:08}")
        reg_read_spi = um7_spi.dreg_accel_raw_z
        reg_read_uart = um7_serial.dreg_accel_raw_z
        print(f"dreg_accel_raw_z_spi            : z={reg_read_spi[1]:+04}, raw=0x{reg_read_spi[0].raw_value:08X} | {reg_read_spi[0].raw_value:08}")
        print(f"dreg_accel_raw_z_serial         : z={reg_read_uart[1]:+04}, raw=0x{reg_read_uart[0].raw_value:08X} | {reg_read_uart[0].raw_value:08}")
        reg_read_spi = um7_spi.dreg_accel_raw_time
        reg_read_uart = um7_serial.dreg_accel_raw_time
        print(f"dreg_accel_raw_time_spi         : t={reg_read_spi[1]:+04.6f}")
        print(f"dreg_accel_raw_time_serial      : t={reg_read_uart[1]:+04.6f}")

        """ Magnetometer Data """
        reg_read_spi = um7_spi.dreg_mag_raw_xy
        reg_read_uart = um7_serial.dreg_mag_raw_xy
        print(f"dreg_mag_raw_xy_spi             : x={reg_read_spi[1]:+04}, y={reg_read_spi[2]:+04}, raw=0x{reg_read_spi[0].raw_value:08X} | {reg_read_spi[0].raw_value:08}")
        print(f"dreg_mag_raw_xy_serial          : x={reg_read_uart[1]:+04}, y={reg_read_uart[2]:+04}, raw=0x{reg_read_uart[0].raw_value:08X} | {reg_read_uart[0].raw_value:08}")
        reg_read_spi = um7_spi.dreg_mag_raw_z
        reg_read_uart = um7_serial.dreg_mag_raw_z
        print(f"dreg_mag_raw_z_spi              : z={reg_read_spi[1]:+04}, raw=0x{reg_read_spi[0].raw_value:08X} | {reg_read_spi[0].raw_value:08}")
        print(f"dreg_mag_raw_z_serial           : z={reg_read_uart[1]:+04}, raw=0x{reg_read_uart[0].raw_value:08X} | {reg_read_uart[0].raw_value:08}")
        reg_read_spi = um7_spi.dreg_mag_raw_time
        reg_read_uart = um7_serial.dreg_mag_raw_time
        print(f"dreg_mag_raw_time_spi           : t={reg_read_spi[1]:+04.6f}")
        print(f"dreg_mag_raw_time_serial        : t={reg_read_uart[1]:+04.6f}")

        """ Temperature """
        reg_read_spi = um7_spi.dreg_temperature
        reg_read_uart = um7_serial.dreg_temperature
        print(f"dreg_temperature_spi            : T={reg_read_spi[1]:+04}, raw={reg_read_spi[0].raw_value}")
        print(f"dreg_temperature_serial         : T={reg_read_uart[1]:+04}, raw={reg_read_uart[0].raw_value}")
        reg_read_spi = um7_spi.dreg_temperature_time
        reg_read_uart = um7_serial.dreg_temperature_time
        print(f"dreg_temperature_time_spi       : Tt={reg_read_spi[1]:+04.6f}, raw={reg_read_spi[0].raw_value}")
        print(f"dreg_temperature_time_serial    : Tt={reg_read_uart[1]:+04.6f}, raw={reg_read_uart[0].raw_value}")

        """ Product ID """
        reg_read_spi = um7_spi.get_fw_revision
        reg_read_uart = um7_serial.get_fw_revision
        print(f"firmware_revision_spi           : {reg_read_spi}")
        print(f"firmware_revision_serial        : {reg_read_uart}")

        """ Firmware Build ID """
        reg_read_spi = um7_spi.build_id
        reg_read_uart = um7_serial.build_id
        print(f"build_id_spi                    : v{reg_read_spi[1]}.{reg_read_spi[2]}.{reg_read_spi[3]}, raw={reg_read_spi[0]}")
        print(f"build_id_serial                 : v{reg_read_uart[1]}.{reg_read_uart[2]}.{reg_read_uart[3]}, raw={reg_read_uart[0]}")
