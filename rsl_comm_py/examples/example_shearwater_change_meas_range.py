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
            logging.FileHandler(f'{Path(__file__).stem}.log'),
            logging.StreamHandler(sys.stdout),
        ])
    script_dir = Path(__file__).parent
    device_file = script_dir.parent / "rsl_A500CNHD.json"
    shearwater = ShearWaterSerial(device=device_file)
    print(f"\n========== CHANGING MEASUREMENT RANGE EXAMPLE ==========================")
    print(f"Setting measurement range to default values:")
    shearwater.creg_gyro_1_meas_range = 0
    shearwater.creg_gyro_2_meas_range = 0
    shearwater.creg_accel_1_meas_range = 0
    print(f"creg_gyro_1_meas_range        : {shearwater.creg_gyro_1_meas_range}")
    print(f"creg_gyro_2_meas_range        : {shearwater.creg_gyro_2_meas_range}")
    print(f"creg_accel_1_meas_range       : {shearwater.creg_accel_1_meas_range}")
    print(f"Conversion coefficients:")
    print(f"hidden_gyro_1_conversion      : {shearwater.hidden_gyro_1_conversion}")
    print(f"hidden_gyro_2_conversion      : {shearwater.hidden_gyro_2_conversion}")
    print(f"hidden_accel_1_conversion     : {shearwater.hidden_accel_1_conversion}")
    print(f"hidden_mag_1_conversion       : {shearwater.hidden_mag_1_conversion}")
    print(f"hidden_mag_2_conversion       : {shearwater.hidden_mag_2_conversion}")
    print(f"Changing measurement range for all the sensors...")
    shearwater.creg_gyro_1_meas_range = 1
    shearwater.creg_gyro_2_meas_range = 2
    shearwater.creg_accel_1_meas_range = 3
    print(f"Updated config registers:")
    print(f"creg_gyro_1_meas_range        : {shearwater.creg_gyro_1_meas_range}")
    print(f"creg_gyro_2_meas_range        : {shearwater.creg_gyro_2_meas_range}")
    print(f"creg_accel_1_meas_range       : {shearwater.creg_accel_1_meas_range}")
    print(f"Updated conversion coefficients:")
    print(f"hidden_gyro_1_conversion      : {shearwater.hidden_gyro_1_conversion}")
    print(f"hidden_gyro_2_conversion      : {shearwater.hidden_gyro_2_conversion}")
    print(f"hidden_accel_1_conversion     : {shearwater.hidden_accel_1_conversion}")
    print(f"hidden_mag_1_conversion       : {shearwater.hidden_mag_1_conversion}")
    print(f"hidden_mag_2_conversion       : {shearwater.hidden_mag_2_conversion}")

