#!/usr/bin/env python

# Author: Dr. Konstantin Selyunin
# License: MIT
# Created: 2020.08.19

import logging
import os.path
import struct

from abc import abstractmethod, ABC
from typing import Union, Tuple

from .rsl_xml_svd.rsl_svd_parser import RslSvdParser


class ShearWaterRegisters(ABC):

    def __init__(self, **kwargs):
        self.svd_parser = RslSvdParser(svd_file=ShearWaterRegisters.find_svd('shearwater.svd'))

    @staticmethod
    def find_svd(svd_file_name: str):
        parent_dir = os.path.join(os.path.dirname(__file__), os.pardir)
        for root, dirs, files in os.walk(parent_dir):
            if svd_file_name in files:
                return os.path.join(root, svd_file_name)

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def read_register(self, reg_addr: int, **kw) -> Tuple[bool, bytes]:
        pass

    @abstractmethod
    def write_register(self, reg_addr: int, reg_value: Union[int, bytes, float, str], **kw):
        pass

    @property
    def creg_com_settings(self):
        """
        The CREG_COM_SETTINGS register is used to set the boards serial port baud rate and to enable (disable) the
        automatic transmission of sensor data and estimated states (telemetry).
        Payload structure:
        [31:28] : BAUD_RATE -- Sets the baud rate of the boards main serial port:
        :return:  BAUD_RATE as bitField; 
        """
        addr = 0x00
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_COM_SETTINGS')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            # find value for BAUD_RATE bit field
            baud_rate_val = (reg.raw_value >> 28) & 0x000F
            baud_rate_enum = reg.find_field_by(name='BAUD_RATE').find_enum_entry_by(value=baud_rate_val)

            return reg, baud_rate_enum

    @creg_com_settings.setter
    def creg_com_settings(self, new_value):
        addr = 0x00
        self.write_register(addr, new_value)

    @property
    def creg_com_rates1(self):
        """
        The CREG_COM_RATES1 register sets desired telemetry transmission rates in Hz for raw accelerometer 1, gyro 1,
        gyro 2 and magnetometer 1 data. If the specified rate is 0, then no data is transmitted.
        Payload structure:
        [31:24] : RAW_ACCEL_1_RATE -- Specifies the desired raw accelerometer 1 data broadcast rate in Hz. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [23:16] : RAW_GYRO_1_RATE -- Specifies the desired raw gyro 1 data broadcast rate in Hz. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz
        [15:8]  : RAW_GYRO_2_RATE -- Specifies the desired raw gyro 2 data broadcast rate in Hz. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [7:0]   : RAW_MAG_1_RATE -- Specifies the desired raw magnetometer 1 data broadcast rate in Hz. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        :return:  RAW_ACCEL_1_RATE as uint8_t; RAW_GYRO_1_RATE as uint8_t; RAW_GYRO_2_RATE as uint8_t; RAW_MAG_1_RATE as uint8_t; 
        """
        addr = 0x01
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_COM_RATES1')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            raw_accel_1_rate, raw_gyro_1_rate, raw_gyro_2_rate, raw_mag_1_rate = struct.unpack('>BBBB', payload[0:4])
            return reg, raw_accel_1_rate, raw_gyro_1_rate, raw_gyro_2_rate, raw_mag_1_rate

    @creg_com_rates1.setter
    def creg_com_rates1(self, new_value):
        addr = 0x01
        self.write_register(addr, new_value)

    @property
    def creg_com_rates2(self):
        """
        The CREG_COM_RATES2 register sets desired telemetry transmission rates for the magnetometer 2, all raw data,
        and temperature data rate. The ALL_RAW_RATE setting has higher priority over the individual raw sensor data
        settings, i.e. whenever this bitfield is set, then the individual raw sensor settings are ignored and not
        used. If the specified rate is 0, then no data is transmitted.
        Payload structure:
        [31:24] : TEMP_RATE -- Specifies the desired broadcast rate for temperature data. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [23:16] : RAW_MAG_2_RATE -- Specifies the desired raw magnetometer 2 data broadcast rate in Hz. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [7:0]   : ALL_RAW_RATE -- Specifies the desired broadcast rate for all raw sensor data. If set, this overrides the broadcast rate setting for individual raw data broadcast rates. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        :return:  TEMP_RATE as uint8_t; RAW_MAG_2_RATE as uint8_t; ALL_RAW_RATE as uint8_t; 
        """
        addr = 0x02
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_COM_RATES2')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            temp_rate, raw_mag_2_rate, all_raw_rate = struct.unpack('>BBxB', payload[0:4])
            return reg, temp_rate, raw_mag_2_rate, all_raw_rate

    @creg_com_rates2.setter
    def creg_com_rates2(self, new_value):
        addr = 0x02
        self.write_register(addr, new_value)

    @property
    def creg_com_rates3(self):
        """
        The CREG_COM_RATES3 register sets desired telemetry transmission rates for processed sensor data for the
        sensors: the accelerometer 1, gyro 1, gyro 2, and magnetometer 1. If the specified rate is 0, then no data is
        transmitted.
        Payload structure:
        [31:24] : PROC_ACCEL_1_RATE -- Specifies the desired broadcast rate for processed accelerometer 1 data. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [23:16] : PROC_GYRO_1_RATE -- Specifies the desired broadcast rate for processed rate gyro 1 data. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [15:8]  : PROC_GYRO_2_RATE -- Specifies the desired broadcast rate for processed processed rate gyro 2 data. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [7:0]   : PROC_MAG_1_RATE -- Specifies the desired broadcast rate for processed magnetometer 1 data. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        :return:  PROC_ACCEL_1_RATE as uint8_t; PROC_GYRO_1_RATE as uint8_t; PROC_GYRO_2_RATE as uint8_t; PROC_MAG_1_RATE as uint8_t; 
        """
        addr = 0x03
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_COM_RATES3')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            proc_accel_1_rate, proc_gyro_1_rate, proc_gyro_2_rate, proc_mag_1_rate = struct.unpack('>BBBB', payload[0:4])
            return reg, proc_accel_1_rate, proc_gyro_1_rate, proc_gyro_2_rate, proc_mag_1_rate

    @creg_com_rates3.setter
    def creg_com_rates3(self, new_value):
        addr = 0x03
        self.write_register(addr, new_value)

    @property
    def creg_com_rates4(self):
        """
        The CREG_COM_RATES4 register defines the desired telemetry transmission rates for the processed data for the
        magnetometer 2, and for all processed data. The ALL_PROC_RATE setting has higher priority over the individual
        processed sensor data settings, i.e. whenever this bitfield is set, then the individual processed sensor
        transmission rate settings are ignored and not used. If the specified rate is 0, then no data is transmitted.
        Payload structure:
        [31:24] : PROC_MAG_2_RATE -- Specifies the desired broadcast rate for processed magnetometer 2 data. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [7:0]   : ALL_PROC_RATE -- Specifies the desired broadcast rate for raw all processed sensor data. If set, this overrides the broadcast rate setting for individual processed data broadcast rates. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        :return:  PROC_MAG_2_RATE as uint8_t; ALL_PROC_RATE as uint8_t; 
        """
        addr = 0x04
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_COM_RATES4')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            proc_mag_2_rate, all_proc_rate = struct.unpack('>BxxB', payload[0:4])
            return reg, proc_mag_2_rate, all_proc_rate

    @creg_com_rates4.setter
    def creg_com_rates4(self, new_value):
        addr = 0x04
        self.write_register(addr, new_value)

    @property
    def creg_com_rates5(self):
        """
        The CREG_COM_RATES5 register sets desired telemetry transmission rates for quaternions, Euler Angles,
        position, and velocity estimates. If the specified rate is 0, then no data is transmitted.
        Payload structure:
        [31:24] : QUAT_RATE -- Specifies the desired broadcast rate for quaternion data. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [23:16] : EULER_RATE -- Specifies the desired broadcast rate for Euler Angle data. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [15:8]  : POSITION_RATE -- Specifies the desired broadcast rate position. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [7:0]   : VELOCITY_RATE -- Specifies the desired broadcast rate for velocity. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        :return:  QUAT_RATE as uint8_t; EULER_RATE as uint8_t; POSITION_RATE as uint8_t; VELOCITY_RATE as uint8_t; 
        """
        addr = 0x05
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_COM_RATES5')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            quat_rate, euler_rate, position_rate, velocity_rate = struct.unpack('>BBBB', payload[0:4])
            return reg, quat_rate, euler_rate, position_rate, velocity_rate

    @creg_com_rates5.setter
    def creg_com_rates5(self, new_value):
        addr = 0x05
        self.write_register(addr, new_value)

    @property
    def creg_com_rates6(self):
        """
        The CREG_COM_RATES6 register sets desired telemetry transmission rates for pose (Euler/position packet),
        health, and gyro bias estimates for the gyro 1 and gyro 2. If the specified rate is 0, then no data is
        transmitted.
        Payload structure:
        [31:24] : POSE_RATE -- Specifies the desired broadcast rate for pose (Euler Angle and position) data. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [19:16] : HEALTH_RATE -- Specifies the desired broadcast rate for the sensor health packet.
        [15:8]  : GYRO_BIAS_1_RATE -- Specifies the desired broadcast rate for gyro 1 bias estimates. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        [7:0]   : GYRO_BIAS_2_RATE -- Specifies the desired broadcast rate for gyro 2 bias estimates. The data is stored as an unsigned 8-bit integer, yielding a maximum rate of 255 Hz.
        :return:  POSE_RATE as uint8_t; HEALTH_RATE as bitField; GYRO_BIAS_1_RATE as uint8_t; GYRO_BIAS_2_RATE as uint8_t; 
        """
        addr = 0x06
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_COM_RATES6')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            pose_rate, gyro_bias_1_rate, gyro_bias_2_rate = struct.unpack('>BxBB', payload[0:4])
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            # find value for HEALTH_RATE bit field
            health_rate_val = (reg.raw_value >> 16) & 0x000F
            health_rate_enum = reg.find_field_by(name='HEALTH_RATE').find_enum_entry_by(value=health_rate_val)

            return reg, pose_rate, gyro_bias_1_rate, gyro_bias_2_rate, reg, health_rate_enum

    @creg_com_rates6.setter
    def creg_com_rates6(self, new_value):
        addr = 0x06
        self.write_register(addr, new_value)

    @property
    def creg_com_rates7(self):
        """
        The CREG_COM_RATES7 register sets desired telemetry transmission rates in Hz for NMEA packets.
        Payload structure:
        [31:28] : NMEA_HEALTH_RATE -- Specifies the desired broadcast rate for Redshift Labs NMEA-style health packet.
        [27:24] : NMEA_POSE_RATE -- Specifies the desired broadcast rate for Redshift Labs NMEA-style pose (Euler Angle/position) packet.
        [23:20] : NMEA_ATTITUDE_RATE -- Specifies the desired broadcast rate for Redshift Labs NMEA-style attitude packet.
        [19:16] : NMEA_SENSOR_RATE -- Specifies the desired broadcast rate for Redshift Labs NMEA-style sensor data packet.
        [15:12] : NMEA_RATES_RATE -- Specifies the desired broadcast rate for Redshift Labs NMEA-style rate data packet.
        [11:8]  : NMEA_GPS_POSE_RATE -- Specifies the desired broadcast rate for Redshift Labs NMEA-style GPS pose packet.
        [7:4]   : NMEA_QUAT_RATE -- Specifies the desired broadcast rate for Redshift Labs NMEA-style quaternion packet.
        :return:  NMEA_HEALTH_RATE as bitField; NMEA_POSE_RATE as bitField; NMEA_ATTITUDE_RATE as bitField; NMEA_SENSOR_RATE as bitField; NMEA_RATES_RATE as bitField; NMEA_GPS_POSE_RATE as bitField; NMEA_QUAT_RATE as bitField; 
        """
        addr = 0x07
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_COM_RATES7')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            # find value for NMEA_HEALTH_RATE bit field
            nmea_health_rate_val = (reg.raw_value >> 28) & 0x000F
            nmea_health_rate_enum = reg.find_field_by(name='NMEA_HEALTH_RATE').find_enum_entry_by(value=nmea_health_rate_val)
            # find value for NMEA_POSE_RATE bit field
            nmea_pose_rate_val = (reg.raw_value >> 24) & 0x000F
            nmea_pose_rate_enum = reg.find_field_by(name='NMEA_POSE_RATE').find_enum_entry_by(value=nmea_pose_rate_val)
            # find value for NMEA_ATTITUDE_RATE bit field
            nmea_attitude_rate_val = (reg.raw_value >> 20) & 0x000F
            nmea_attitude_rate_enum = reg.find_field_by(name='NMEA_ATTITUDE_RATE').find_enum_entry_by(value=nmea_attitude_rate_val)
            # find value for NMEA_SENSOR_RATE bit field
            nmea_sensor_rate_val = (reg.raw_value >> 16) & 0x000F
            nmea_sensor_rate_enum = reg.find_field_by(name='NMEA_SENSOR_RATE').find_enum_entry_by(value=nmea_sensor_rate_val)
            # find value for NMEA_RATES_RATE bit field
            nmea_rates_rate_val = (reg.raw_value >> 12) & 0x000F
            nmea_rates_rate_enum = reg.find_field_by(name='NMEA_RATES_RATE').find_enum_entry_by(value=nmea_rates_rate_val)
            # find value for NMEA_GPS_POSE_RATE bit field
            nmea_gps_pose_rate_val = (reg.raw_value >> 8) & 0x000F
            nmea_gps_pose_rate_enum = reg.find_field_by(name='NMEA_GPS_POSE_RATE').find_enum_entry_by(value=nmea_gps_pose_rate_val)
            # find value for NMEA_QUAT_RATE bit field
            nmea_quat_rate_val = (reg.raw_value >> 4) & 0x000F
            nmea_quat_rate_enum = reg.find_field_by(name='NMEA_QUAT_RATE').find_enum_entry_by(value=nmea_quat_rate_val)

            return reg, nmea_health_rate_enum, nmea_pose_rate_enum, nmea_attitude_rate_enum, nmea_sensor_rate_enum, nmea_rates_rate_enum, nmea_gps_pose_rate_enum, nmea_quat_rate_enum

    @creg_com_rates7.setter
    def creg_com_rates7(self, new_value):
        addr = 0x07
        self.write_register(addr, new_value)

    @property
    def creg_misc_settings(self):
        """
        This register contains miscellaneous filter and sensor control options.
        Payload structure:
        [8]     : PPS -- If set, this bit causes the TX2 pin on the IO Expansion header to be used as the PPS input from an external GPS module. PPS pulses will then be used to synchronize the system clock to UTC time of day.
        [3]     : ZG -- If set, this bit causes the devicee to attempt to measure the rate gyro bias on startup. The sensor must be stationary on startup for this feature to work properly.
        [2]     : Q -- If this bit is set, the sensor will run in quaternion mode instead of Euler Angle mode.
        [1]     : MAG1 -- If set, the magnetometer 1 will be used in state updates.
        [0]     : MAG2 -- If set, the magnetometer 2 will be used in state updates.
        :return:  PPS as bitField; ZG as bitField; Q as bitField; MAG1 as bitField; MAG2 as bitField; 
        """
        addr = 0x08
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MISC_SETTINGS')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            # find value for PPS bit field
            pps_val = (reg.raw_value >> 8) & 0x0001
            pps_enum = reg.find_field_by(name='PPS').find_enum_entry_by(value=pps_val)
            # find value for ZG bit field
            zg_val = (reg.raw_value >> 3) & 0x0001
            zg_enum = reg.find_field_by(name='ZG').find_enum_entry_by(value=zg_val)
            # find value for Q bit field
            q_val = (reg.raw_value >> 2) & 0x0001
            q_enum = reg.find_field_by(name='Q').find_enum_entry_by(value=q_val)
            # find value for MAG1 bit field
            mag1_val = (reg.raw_value >> 1) & 0x0001
            mag1_enum = reg.find_field_by(name='MAG1').find_enum_entry_by(value=mag1_val)
            # find value for MAG2 bit field
            mag2_val = (reg.raw_value >> 0) & 0x0001
            mag2_enum = reg.find_field_by(name='MAG2').find_enum_entry_by(value=mag2_val)

            return reg, pps_enum, zg_enum, q_enum, mag1_enum, mag2_enum

    @creg_misc_settings.setter
    def creg_misc_settings(self, new_value):
        addr = 0x08
        self.write_register(addr, new_value)

    @property
    def creg_gyro_1_meas_range(self):
        """
        The CREG_GYRO_1_MEAS_RANGE register sets the desired measurement range for the gyro 1 sensor. If the rate is
        not set, then the default value of 2000 deg/s will be used as a measurement range.
        Payload structure:
        [1:0]   : MEAS_GYRO1 -- Specifies the desired measurement range for the gyro 1 measurements.
        :return:  MEAS_GYRO1 as bitField; 
        """
        addr = 0x09
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_GYRO_1_MEAS_RANGE')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            # find value for MEAS_GYRO1 bit field
            meas_gyro1_val = (reg.raw_value >> 0) & 0x0003
            meas_gyro1_enum = reg.find_field_by(name='MEAS_GYRO1').find_enum_entry_by(value=meas_gyro1_val)

            return reg, meas_gyro1_enum

    @creg_gyro_1_meas_range.setter
    def creg_gyro_1_meas_range(self, new_value):
        addr = 0x09
        self.write_register(addr, new_value)

    @property
    def creg_gyro_1_trim_x(self):
        """
        This register sets the x-axis rate gyro 1 trim, which is used to add additional bias compensation for the rate
        gyros during calls to the ZERO_GYRO_BIAS command.
        Payload structure:
        [31:0]  : GYRO_1_TRIM_X -- 32-bit IEEE Floating Point Value
        :return:  GYRO_1_TRIM_X as float; 
        """
        addr = 0x0A
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_GYRO_1_TRIM_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_trim_x,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_trim_x, 

    @creg_gyro_1_trim_x.setter
    def creg_gyro_1_trim_x(self, new_value):
        addr = 0x0A
        self.write_register(addr, new_value)

    @property
    def creg_gyro_1_trim_y(self):
        """
        This register sets the y-axis rate gyro 1 trim, which is used to add additional bias compensation for the rate
        gyros during calls to the ZERO_GYRO_BIAS command.
        Payload structure:
        [31:0]  : GYRO_1_TRIM_Y -- 32-bit IEEE Floating Point Value
        :return:  GYRO_1_TRIM_Y as float; 
        """
        addr = 0x0B
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_GYRO_1_TRIM_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_trim_y,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_trim_y, 

    @creg_gyro_1_trim_y.setter
    def creg_gyro_1_trim_y(self, new_value):
        addr = 0x0B
        self.write_register(addr, new_value)

    @property
    def creg_gyro_1_trim_z(self):
        """
        This register sets the z-axis rate gyro 1 trim, which is used to add additional bias compensation for the rate
        gyros during calls to the ZERO_GYRO_BIAS command.
        Payload structure:
        [31:0]  : GYRO_1_TRIM_Z -- 32-bit IEEE Floating Point Value
        :return:  GYRO_1_TRIM_Z as float; 
        """
        addr = 0x0C
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_GYRO_1_TRIM_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_trim_z,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_trim_z, 

    @creg_gyro_1_trim_z.setter
    def creg_gyro_1_trim_z(self, new_value):
        addr = 0x0C
        self.write_register(addr, new_value)

    @property
    def creg_gyro_2_meas_range(self):
        """
        The CREG_GYRO_2_MEAS_RANGE register sets the desired measurement range for the gyro 2 sensor. If the rate is
        not set, then the default value of 2000 deg/s will be used as a measurement range.
        Payload structure:
        [1:0]   : MEAS_GYRO2 -- Specifies the desired measurement range for the gyro 2 measurements.
        :return:  MEAS_GYRO2 as bitField; 
        """
        addr = 0x0D
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_GYRO_2_MEAS_RANGE')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            # find value for MEAS_GYRO2 bit field
            meas_gyro2_val = (reg.raw_value >> 0) & 0x0003
            meas_gyro2_enum = reg.find_field_by(name='MEAS_GYRO2').find_enum_entry_by(value=meas_gyro2_val)

            return reg, meas_gyro2_enum

    @creg_gyro_2_meas_range.setter
    def creg_gyro_2_meas_range(self, new_value):
        addr = 0x0D
        self.write_register(addr, new_value)

    @property
    def creg_gyro_2_trim_x(self):
        """
        This register sets the x-axis rate gyro 2 trim, which is used to add additional bias compensation for the rate
        gyros during calls to the ZERO_GYRO_BIAS command.
        Payload structure:
        [31:0]  : GYRO_2_TRIM_X -- 32-bit IEEE Floating Point Value
        :return:  GYRO_2_TRIM_X as float; 
        """
        addr = 0x0E
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_GYRO_2_TRIM_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_trim_x,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_trim_x, 

    @creg_gyro_2_trim_x.setter
    def creg_gyro_2_trim_x(self, new_value):
        addr = 0x0E
        self.write_register(addr, new_value)

    @property
    def creg_gyro_2_trim_y(self):
        """
        This register sets the y-axis rate gyro 2 trim, which is used to add additional bias compensation for the rate
        gyros during calls to the ZERO_GYRO_BIAS command.
        Payload structure:
        [31:0]  : GYRO_2_TRIM_Y -- 32-bit IEEE Floating Point Value
        :return:  GYRO_2_TRIM_Y as float; 
        """
        addr = 0x0F
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_GYRO_2_TRIM_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_trim_y,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_trim_y, 

    @creg_gyro_2_trim_y.setter
    def creg_gyro_2_trim_y(self, new_value):
        addr = 0x0F
        self.write_register(addr, new_value)

    @property
    def creg_gyro_2_trim_z(self):
        """
        This register sets the z-axis rate gyro 2 trim, which is used to add additional bias compensation for the rate
        gyros during calls to the ZERO_GYRO_BIAS command.
        Payload structure:
        [31:0]  : GYRO_2_TRIM_Z -- 32-bit IEEE Floating Point Value
        :return:  GYRO_2_TRIM_Z as float; 
        """
        addr = 0x10
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_GYRO_2_TRIM_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_trim_z,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_trim_z, 

    @creg_gyro_2_trim_z.setter
    def creg_gyro_2_trim_z(self, new_value):
        addr = 0x10
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_cal1_1(self):
        """
        Row 1, Column 1 of magnetometer 1 calibration matrix.
        Payload structure:
        [31:0]  : MAG_1_CAL1_1 -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_CAL1_1 as float; 
        """
        addr = 0x11
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_CAL1_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_cal1_1,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_cal1_1, 

    @creg_mag_1_cal1_1.setter
    def creg_mag_1_cal1_1(self, new_value):
        addr = 0x11
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_cal1_2(self):
        """
        Row 1, Column 2 of magnetometer 1 calibration matrix.
        Payload structure:
        [31:0]  : MAG_1_CAL1_2 -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_CAL1_2 as float; 
        """
        addr = 0x12
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_CAL1_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_cal1_2,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_cal1_2, 

    @creg_mag_1_cal1_2.setter
    def creg_mag_1_cal1_2(self, new_value):
        addr = 0x12
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_cal1_3(self):
        """
        Row 1, Column 3 of magnetometer 1 calibration matrix.
        Payload structure:
        [31:0]  : MAG_1_CAL1_3 -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_CAL1_3 as float; 
        """
        addr = 0x13
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_CAL1_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_cal1_3,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_cal1_3, 

    @creg_mag_1_cal1_3.setter
    def creg_mag_1_cal1_3(self, new_value):
        addr = 0x13
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_cal2_1(self):
        """
        Row 2, Column 1 of magnetometer 1 calibration matrix.
        Payload structure:
        [31:0]  : MAG_1_CAL2_1 -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_CAL2_1 as float; 
        """
        addr = 0x14
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_CAL2_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_cal2_1,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_cal2_1, 

    @creg_mag_1_cal2_1.setter
    def creg_mag_1_cal2_1(self, new_value):
        addr = 0x14
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_cal2_2(self):
        """
        Row 2, Column 2 of magnetometer 1 calibration matrix.
        Payload structure:
        [31:0]  : MAG_1_CAL2_2 -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_CAL2_2 as float; 
        """
        addr = 0x15
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_CAL2_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_cal2_2,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_cal2_2, 

    @creg_mag_1_cal2_2.setter
    def creg_mag_1_cal2_2(self, new_value):
        addr = 0x15
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_cal2_3(self):
        """
        Row 2, Column 3 of magnetometer 1 calibration matrix.
        Payload structure:
        [31:0]  : MAG_1_CAL2_3 -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_CAL2_3 as float; 
        """
        addr = 0x16
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_CAL2_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_cal2_3,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_cal2_3, 

    @creg_mag_1_cal2_3.setter
    def creg_mag_1_cal2_3(self, new_value):
        addr = 0x16
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_cal3_1(self):
        """
        Row 3, Column 1 of magnetometer 1 calibration matrix.
        Payload structure:
        [31:0]  : MAG_1_CAL3_1 -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_CAL3_1 as float; 
        """
        addr = 0x17
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_CAL3_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_cal3_1,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_cal3_1, 

    @creg_mag_1_cal3_1.setter
    def creg_mag_1_cal3_1(self, new_value):
        addr = 0x17
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_cal3_2(self):
        """
        Row 3, Column 2 of magnetometer 1 calibration matrix.
        Payload structure:
        [31:0]  : MAG_1_CAL3_2 -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_CAL3_2 as float; 
        """
        addr = 0x18
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_CAL3_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_cal3_2,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_cal3_2, 

    @creg_mag_1_cal3_2.setter
    def creg_mag_1_cal3_2(self, new_value):
        addr = 0x18
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_cal3_3(self):
        """
        Row 3, Column 3 of magnetometer 1 calibration matrix.
        Payload structure:
        [31:0]  : MAG_1_CAL3_3 -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_CAL3_3 as float; 
        """
        addr = 0x19
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_CAL3_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_cal3_3,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_cal3_3, 

    @creg_mag_1_cal3_3.setter
    def creg_mag_1_cal3_3(self, new_value):
        addr = 0x19
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_bias_x(self):
        """
        This register stores a bias term for the magnetometer 1 x-axis for hard-iron calibration. This term can be
        computed by performing magnetometer calibration with the Redshift labs Serial Interface.
        Payload structure:
        [31:0]  : MAG_1_BIAS_X -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_BIAS_X as float; 
        """
        addr = 0x1A
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_BIAS_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_bias_x,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_bias_x, 

    @creg_mag_1_bias_x.setter
    def creg_mag_1_bias_x(self, new_value):
        addr = 0x1A
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_bias_y(self):
        """
        This register stores a bias term for the magnetometer 1 y-axis for hard-iron calibration. This term can be
        computed by performing magnetometer calibration with the Redshift labs Serial Interface.
        Payload structure:
        [31:0]  : MAG_1_BIAS_Y -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_BIAS_Y as float; 
        """
        addr = 0x1B
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_BIAS_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_bias_y,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_bias_y, 

    @creg_mag_1_bias_y.setter
    def creg_mag_1_bias_y(self, new_value):
        addr = 0x1B
        self.write_register(addr, new_value)

    @property
    def creg_mag_1_bias_z(self):
        """
        This register stores a bias term for the magnetometer 1 z-axis for hard-iron calibration. This term can be
        computed by performing magnetometer calibration with the Redshift labs Serial Interface.
        Payload structure:
        [31:0]  : MAG_1_BIAS_Z -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_BIAS_Z as float; 
        """
        addr = 0x1C
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_1_BIAS_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_bias_z,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_bias_z, 

    @creg_mag_1_bias_z.setter
    def creg_mag_1_bias_z(self, new_value):
        addr = 0x1C
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_cal1_1(self):
        """
        Row 1, Column 1 of magnetometer 2 calibration matrix.
        Payload structure:
        [31:0]  : MAG_2_CAL1_1 -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_CAL1_1 as float; 
        """
        addr = 0x1D
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_CAL1_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_cal1_1,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_cal1_1, 

    @creg_mag_2_cal1_1.setter
    def creg_mag_2_cal1_1(self, new_value):
        addr = 0x1D
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_cal1_2(self):
        """
        Row 1, Column 2 of magnetometer 2 calibration matrix.
        Payload structure:
        [31:0]  : MAG_2_CAL1_2 -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_CAL1_2 as float; 
        """
        addr = 0x1E
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_CAL1_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_cal1_2,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_cal1_2, 

    @creg_mag_2_cal1_2.setter
    def creg_mag_2_cal1_2(self, new_value):
        addr = 0x1E
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_cal1_3(self):
        """
        Row 1, Column 3 of magnetometer 2 calibration matrix.
        Payload structure:
        [31:0]  : MAG_2_CAL1_3 -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_CAL1_3 as float; 
        """
        addr = 0x1F
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_CAL1_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_cal1_3,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_cal1_3, 

    @creg_mag_2_cal1_3.setter
    def creg_mag_2_cal1_3(self, new_value):
        addr = 0x1F
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_cal2_1(self):
        """
        Row 2, Column 1 of magnetometer 2 calibration matrix.
        Payload structure:
        [31:0]  : MAG_2_CAL2_1 -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_CAL2_1 as float; 
        """
        addr = 0x20
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_CAL2_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_cal2_1,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_cal2_1, 

    @creg_mag_2_cal2_1.setter
    def creg_mag_2_cal2_1(self, new_value):
        addr = 0x20
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_cal2_2(self):
        """
        Row 2, Column 2 of magnetometer 2 calibration matrix.
        Payload structure:
        [31:0]  : MAG_2_CAL2_2 -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_CAL2_2 as float; 
        """
        addr = 0x21
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_CAL2_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_cal2_2,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_cal2_2, 

    @creg_mag_2_cal2_2.setter
    def creg_mag_2_cal2_2(self, new_value):
        addr = 0x21
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_cal2_3(self):
        """
        Row 2, Column 3 of magnetometer 2 calibration matrix.
        Payload structure:
        [31:0]  : MAG_2_CAL2_3 -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_CAL2_3 as float; 
        """
        addr = 0x22
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_CAL2_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_cal2_3,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_cal2_3, 

    @creg_mag_2_cal2_3.setter
    def creg_mag_2_cal2_3(self, new_value):
        addr = 0x22
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_cal3_1(self):
        """
        Row 3, Column 1 of magnetometer 2 calibration matrix.
        Payload structure:
        [31:0]  : MAG_2_CAL3_1 -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_CAL3_1 as float; 
        """
        addr = 0x23
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_CAL3_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_cal3_1,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_cal3_1, 

    @creg_mag_2_cal3_1.setter
    def creg_mag_2_cal3_1(self, new_value):
        addr = 0x23
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_cal3_2(self):
        """
        Row 3, Column 2 of magnetometer 2 calibration matrix.
        Payload structure:
        [31:0]  : MAG_2_CAL3_2 -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_CAL3_2 as float; 
        """
        addr = 0x24
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_CAL3_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_cal3_2,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_cal3_2, 

    @creg_mag_2_cal3_2.setter
    def creg_mag_2_cal3_2(self, new_value):
        addr = 0x24
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_cal3_3(self):
        """
        Row 3, Column 3 of magnetometer 2 calibration matrix.
        Payload structure:
        [31:0]  : MAG_2_CAL3_3 -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_CAL3_3 as float; 
        """
        addr = 0x25
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_CAL3_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_cal3_3,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_cal3_3, 

    @creg_mag_2_cal3_3.setter
    def creg_mag_2_cal3_3(self, new_value):
        addr = 0x25
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_bias_x(self):
        """
        This register stores a bias term for the magnetometer 2 x-axis for hard-iron calibration. This term can be
        computed by performing magnetometer calibration with the Redshift labs Serial Interface.
        Payload structure:
        [31:0]  : MAG_2_BIAS_X -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_BIAS_X as float; 
        """
        addr = 0x26
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_BIAS_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_bias_x,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_bias_x, 

    @creg_mag_2_bias_x.setter
    def creg_mag_2_bias_x(self, new_value):
        addr = 0x26
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_bias_y(self):
        """
        This register stores a bias term for the magnetometer 2 y-axis for hard-iron calibration. This term can be
        computed by performing magnetometer calibration with the Redshift labs Serial Interface.
        Payload structure:
        [31:0]  : MAG_2_BIAS_Y -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_BIAS_Y as float; 
        """
        addr = 0x27
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_BIAS_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_bias_y,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_bias_y, 

    @creg_mag_2_bias_y.setter
    def creg_mag_2_bias_y(self, new_value):
        addr = 0x27
        self.write_register(addr, new_value)

    @property
    def creg_mag_2_bias_z(self):
        """
        This register stores a bias term for the magnetometer 2 z-axis for hard-iron calibration. This term can be
        computed by performing magnetometer calibration with the Redshift labs Serial Interface.
        Payload structure:
        [31:0]  : MAG_2_BIAS_Z -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_BIAS_Z as float; 
        """
        addr = 0x28
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_MAG_2_BIAS_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_bias_z,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_bias_z, 

    @creg_mag_2_bias_z.setter
    def creg_mag_2_bias_z(self, new_value):
        addr = 0x28
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_meas_range(self):
        """
        The CREG_ACCEL_1_MEAS_RANGE register sets the desired measurement range for the accelerometer 1. If the rate
        is not set, then the default value of the +-2 g will be used as a measurement range.
        Payload structure:
        [1:0]   : MEAS_ACC1 -- Specifies the desired measurement range for the accelerometer 1 measurements.
        :return:  MEAS_ACC1 as bitField; 
        """
        addr = 0x29
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_MEAS_RANGE')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            # find value for MEAS_ACC1 bit field
            meas_acc1_val = (reg.raw_value >> 0) & 0x0003
            meas_acc1_enum = reg.find_field_by(name='MEAS_ACC1').find_enum_entry_by(value=meas_acc1_val)

            return reg, meas_acc1_enum

    @creg_accel_1_meas_range.setter
    def creg_accel_1_meas_range(self, new_value):
        addr = 0x29
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_cal1_1(self):
        """
        Row 1, Column 1 of accelerometer 1 calibration matrix.
        Payload structure:
        [31:0]  : ACCEL_1_CAL1_1 -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_CAL1_1 as float; 
        """
        addr = 0x2A
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_CAL1_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_cal1_1,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_cal1_1, 

    @creg_accel_1_cal1_1.setter
    def creg_accel_1_cal1_1(self, new_value):
        addr = 0x2A
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_cal1_2(self):
        """
        Row 1, Column 2 of accelerometer 1 calibration matrix.
        Payload structure:
        [31:0]  : ACCEL_1_CAL1_2 -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_CAL1_2 as float; 
        """
        addr = 0x2B
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_CAL1_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_cal1_2,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_cal1_2, 

    @creg_accel_1_cal1_2.setter
    def creg_accel_1_cal1_2(self, new_value):
        addr = 0x2B
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_cal1_3(self):
        """
        Row 1, Column 3 of accelerometer 1 calibration matrix.
        Payload structure:
        [31:0]  : ACCEL_1_CAL1_3 -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_CAL1_3 as float; 
        """
        addr = 0x2C
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_CAL1_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_cal1_3,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_cal1_3, 

    @creg_accel_1_cal1_3.setter
    def creg_accel_1_cal1_3(self, new_value):
        addr = 0x2C
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_cal2_1(self):
        """
        Row 2, Column 1 of accelerometer 1 calibration matrix.
        Payload structure:
        [31:0]  : ACCEL_1_CAL2_1 -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_CAL2_1 as float; 
        """
        addr = 0x2D
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_CAL2_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_cal2_1,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_cal2_1, 

    @creg_accel_1_cal2_1.setter
    def creg_accel_1_cal2_1(self, new_value):
        addr = 0x2D
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_cal2_2(self):
        """
        Row 2, Column 2 of accelerometer 1 calibration matrix.
        Payload structure:
        [31:0]  : ACCEL_1_CAL2_2 -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_CAL2_2 as float; 
        """
        addr = 0x2E
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_CAL2_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_cal2_2,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_cal2_2, 

    @creg_accel_1_cal2_2.setter
    def creg_accel_1_cal2_2(self, new_value):
        addr = 0x2E
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_cal2_3(self):
        """
        Row 2, Column 3 of accelerometer 1 calibration matrix.
        Payload structure:
        [31:0]  : ACCEL_1_CAL2_3 -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_CAL2_3 as float; 
        """
        addr = 0x2F
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_CAL2_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_cal2_3,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_cal2_3, 

    @creg_accel_1_cal2_3.setter
    def creg_accel_1_cal2_3(self, new_value):
        addr = 0x2F
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_cal3_1(self):
        """
        Row 3, Column 1 of accelerometer 1 calibration matrix.
        Payload structure:
        [31:0]  : ACCEL_1_CAL3_1 -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_CAL3_1 as float; 
        """
        addr = 0x30
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_CAL3_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_cal3_1,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_cal3_1, 

    @creg_accel_1_cal3_1.setter
    def creg_accel_1_cal3_1(self, new_value):
        addr = 0x30
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_cal3_2(self):
        """
        Row 3, Column 2 of accelerometer 1 calibration matrix.
        Payload structure:
        [31:0]  : ACCEL_1_CAL3_2 -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_CAL3_2 as float; 
        """
        addr = 0x31
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_CAL3_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_cal3_2,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_cal3_2, 

    @creg_accel_1_cal3_2.setter
    def creg_accel_1_cal3_2(self, new_value):
        addr = 0x31
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_cal3_3(self):
        """
        Row 3, Column 3 of accelerometer 1 calibration matrix.
        Payload structure:
        [31:0]  : ACCEL_1_CAL3_3 -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_CAL3_3 as float; 
        """
        addr = 0x32
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_CAL3_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_cal3_3,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_cal3_3, 

    @creg_accel_1_cal3_3.setter
    def creg_accel_1_cal3_3(self, new_value):
        addr = 0x32
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_bias_x(self):
        """
        This register stores a bias term for the accelerometer 1 x-axis for bias calibration. This term can be
        computed by performing calibrate accelerometers command within the Redshift labs Serial Interface.
        Payload structure:
        [31:0]  : ACCEL_1_BIAS_X -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_BIAS_X as float; 
        """
        addr = 0x33
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_BIAS_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_bias_x,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_bias_x, 

    @creg_accel_1_bias_x.setter
    def creg_accel_1_bias_x(self, new_value):
        addr = 0x33
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_bias_y(self):
        """
        This register stores a bias term for the accelerometer 1 y-axis for bias calibration. This term can be
        computed by performing calibrate accelerometers command within the Redshift labs Serial Interface.
        Payload structure:
        [31:0]  : ACCEL_1_BIAS_Y -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_BIAS_Y as float; 
        """
        addr = 0x34
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_BIAS_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_bias_y,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_bias_y, 

    @creg_accel_1_bias_y.setter
    def creg_accel_1_bias_y(self, new_value):
        addr = 0x34
        self.write_register(addr, new_value)

    @property
    def creg_accel_1_bias_z(self):
        """
        This register stores a bias term for the accelerometer 1 z-axis for bias calibration. This term can be
        computed by performing calibrate accelerometers command within the Redshift labs Serial Interface.
        Payload structure:
        [31:0]  : ACCEL_1_BIAS_Z -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_BIAS_Z as float; 
        """
        addr = 0x35
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='CREG_ACCEL_1_BIAS_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_bias_z,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_bias_z, 

    @creg_accel_1_bias_z.setter
    def creg_accel_1_bias_z(self, new_value):
        addr = 0x35
        self.write_register(addr, new_value)

    @property
    def dreg_health(self):
        """
        The health register reports the current status of the sensors on the board. Monitoring the health register is
        the easiest way to watch for other problems that could affect the behavior of the board, status of the
        sensors. The analogous to the health register, the status of the GPS signal can be monitored in the
        DREG_GPS_HEALTH
        Payload structure:
        [8]     : OVF -- Overflow bit. This bit is set if the board is attempting to transmit data over the serial port faster than is allowed given the baud-rate. If this bit is set, reduce broadcast rates in the COM_RATES registers.
        [7]     : ACC1_N -- This bit is set if the sensor detects that the norm of the accelerometer measurement is too far away from 1G to be used (i.e. during aggressive acceleration or high vibration).
        [6]     : MAG1_N -- This bit is set if the sensor detects that the norm of the magnetometer measurement for the magnetometer 1 is too far away from 1.0 to be trusted. Usually indicates bad calibration, local field distortions, or both.
        [5]     : MAG2_N -- This bit is set if the sensor detects that the norm of the magnetometer measurement for the magnetometer 2 is too far away from 1.0 to be trusted. Usually indicates bad calibration, local field distortions, or both.
        [4]     : ACCEL1 -- This bit will be set if the accelerometer 1 fails to initialize on startup.
        [3]     : GYRO1 -- This bit will be set if the rate gyro 1 fails to initialize on startup.
        [2]     : GYRO2 -- This bit will be set if the rate gyro 2 fails to initialize on startup.
        [1]     : MAG1 -- This bit will be set if the magnetometer 1 fails to initialize on startup.
        [0]     : MAG2 -- This bit will be set if the magnetometer 2 fails to initialize on startup.
        :return:  OVF as bitField; ACC1_N as bitField; MAG1_N as bitField; MAG2_N as bitField; ACCEL1 as bitField; GYRO1 as bitField; GYRO2 as bitField; MAG1 as bitField; MAG2 as bitField; 
        """
        addr = 0x55
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_HEALTH')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            # find value for OVF bit field
            ovf_val = (reg.raw_value >> 8) & 0x0001
            ovf_enum = reg.find_field_by(name='OVF').find_enum_entry_by(value=ovf_val)
            # find value for ACC1_N bit field
            acc1_n_val = (reg.raw_value >> 7) & 0x0001
            acc1_n_enum = reg.find_field_by(name='ACC1_N').find_enum_entry_by(value=acc1_n_val)
            # find value for MAG1_N bit field
            mag1_n_val = (reg.raw_value >> 6) & 0x0001
            mag1_n_enum = reg.find_field_by(name='MAG1_N').find_enum_entry_by(value=mag1_n_val)
            # find value for MAG2_N bit field
            mag2_n_val = (reg.raw_value >> 5) & 0x0001
            mag2_n_enum = reg.find_field_by(name='MAG2_N').find_enum_entry_by(value=mag2_n_val)
            # find value for ACCEL1 bit field
            accel1_val = (reg.raw_value >> 4) & 0x0001
            accel1_enum = reg.find_field_by(name='ACCEL1').find_enum_entry_by(value=accel1_val)
            # find value for GYRO1 bit field
            gyro1_val = (reg.raw_value >> 3) & 0x0001
            gyro1_enum = reg.find_field_by(name='GYRO1').find_enum_entry_by(value=gyro1_val)
            # find value for GYRO2 bit field
            gyro2_val = (reg.raw_value >> 2) & 0x0001
            gyro2_enum = reg.find_field_by(name='GYRO2').find_enum_entry_by(value=gyro2_val)
            # find value for MAG1 bit field
            mag1_val = (reg.raw_value >> 1) & 0x0001
            mag1_enum = reg.find_field_by(name='MAG1').find_enum_entry_by(value=mag1_val)
            # find value for MAG2 bit field
            mag2_val = (reg.raw_value >> 0) & 0x0001
            mag2_enum = reg.find_field_by(name='MAG2').find_enum_entry_by(value=mag2_val)

            return reg, ovf_enum, acc1_n_enum, mag1_n_enum, mag2_n_enum, accel1_enum, gyro1_enum, gyro2_enum, mag1_enum, mag2_enum

    @property
    def dreg_gyro_1_raw_xy(self):
        """
        Contains raw X and Y axis rate gyro 1 data.
        Payload structure:
        [31:16] : GYRO_1_RAW_X -- Gyro X (2s complement 16-bit integer)
        [15:0]  : GYRO_1_RAW_Y -- Gyro Y (2s complement 16-bit integer)
        :return:  GYRO_1_RAW_X as int16_t; GYRO_1_RAW_Y as int16_t; 
        """
        addr = 0x56
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_1_RAW_XY')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            gyro_1_raw_x, gyro_1_raw_y = struct.unpack('>hh', payload[0:4])
            return reg, gyro_1_raw_x, gyro_1_raw_y

    @property
    def dreg_gyro_1_raw_z(self):
        """
        Contains raw Z axis rate gyro 1 data.
        Payload structure:
        [31:16] : GYRO_1_RAW_Z -- Gyro Z (2s complement 16-bit integer)
        :return:  GYRO_1_RAW_Z as int16_t; 
        """
        addr = 0x57
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_1_RAW_Z')
            reg.raw_value, = struct.unpack('>hxx', payload[0:4])
            gyro_1_raw_z,  = struct.unpack('>hxx', payload[0:4])
            return reg, gyro_1_raw_z, 

    @property
    def dreg_gyro_1_raw_time(self):
        """
        Contains time at which the last rate gyro 1 data was acquired.
        Payload structure:
        [31:0]  : GYRO_1_RAW_TIME -- 32-bit IEEE Floating Point Value
        :return:  GYRO_1_RAW_TIME as float; 
        """
        addr = 0x58
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_1_RAW_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_raw_time,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_raw_time, 

    @property
    def dreg_gyro_2_raw_xy(self):
        """
        Contains raw X and Y axis rate gyro 2 data.
        Payload structure:
        [31:16] : GYRO_2_RAW_X -- Gyro X (2s complement 16-bit integer)
        [15:0]  : GYRO_2_RAW_Y -- Gyro Y (2s complement 16-bit integer)
        :return:  GYRO_2_RAW_X as int16_t; GYRO_2_RAW_Y as int16_t; 
        """
        addr = 0x59
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_2_RAW_XY')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            gyro_2_raw_x, gyro_2_raw_y = struct.unpack('>hh', payload[0:4])
            return reg, gyro_2_raw_x, gyro_2_raw_y

    @property
    def dreg_gyro_2_raw_z(self):
        """
        Contains raw Z axis rate gyro 2 data.
        Payload structure:
        [31:16] : GYRO_2_RAW_Z -- Gyro Z (2s complement 16-bit integer)
        :return:  GYRO_2_RAW_Z as int16_t; 
        """
        addr = 0x5A
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_2_RAW_Z')
            reg.raw_value, = struct.unpack('>hxx', payload[0:4])
            gyro_2_raw_z,  = struct.unpack('>hxx', payload[0:4])
            return reg, gyro_2_raw_z, 

    @property
    def dreg_gyro_2_raw_time(self):
        """
        Contains time at which the last rate gyro 2 data was acquired.
        Payload structure:
        [31:0]  : GYRO_2_RAW_TIME -- 32-bit IEEE Floating Point Value
        :return:  GYRO_2_RAW_TIME as float; 
        """
        addr = 0x5B
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_2_RAW_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_raw_time,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_raw_time, 

    @property
    def dreg_accel_1_raw_xy(self):
        """
        Contains raw X and Y axis accelerometer 1 data.
        Payload structure:
        [31:16] : ACCEL_1_RAW_X -- Accel X (2s complement 16-bit integer)
        [15:0]  : ACCEL_1_RAW_Y -- Accel Y (2s complement 16-bit integer)
        :return:  ACCEL_1_RAW_X as int16_t; ACCEL_1_RAW_Y as int16_t; 
        """
        addr = 0x5C
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_ACCEL_1_RAW_XY')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            accel_1_raw_x, accel_1_raw_y = struct.unpack('>hh', payload[0:4])
            return reg, accel_1_raw_x, accel_1_raw_y

    @property
    def dreg_accel_1_raw_z(self):
        """
        Contains raw Z axis accelerometer 1 data.
        Payload structure:
        [31:16] : ACCEL_1_RAW_Z -- Accel Z (2s complement 16-bit integer)
        :return:  ACCEL_1_RAW_Z as int16_t; 
        """
        addr = 0x5D
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_ACCEL_1_RAW_Z')
            reg.raw_value, = struct.unpack('>hxx', payload[0:4])
            accel_1_raw_z,  = struct.unpack('>hxx', payload[0:4])
            return reg, accel_1_raw_z, 

    @property
    def dreg_accel_1_raw_time(self):
        """
        Contains time at which the last raw data sample for the accelerometer 1 was acquired.
        Payload structure:
        [31:0]  : ACCEL_1_RAW_TIME -- 32-bit IEEE Floating Point Value
        :return:  ACCEL_1_RAW_TIME as float; 
        """
        addr = 0x5E
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_ACCEL_1_RAW_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_raw_time,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_raw_time, 

    @property
    def dreg_mag_1_raw_x(self):
        """
        Contains raw x axis magnetometer 1 data.
        Payload structure:
        [31:0]  : MAG_1_RAW_X -- 32-bit signed integer value
        :return:  MAG_1_RAW_X as int32_t; 
        """
        addr = 0x5F
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_1_RAW_X')
            reg.raw_value, = struct.unpack('>i', payload[0:4])
            mag_1_raw_x,  = struct.unpack('>i', payload[0:4])
            return reg, mag_1_raw_x, 

    @property
    def dreg_mag_1_raw_y(self):
        """
        Contains raw y axis magnetometer 1 data.
        Payload structure:
        [31:0]  : MAG_1_RAW_Y -- 32-bit signed integer value
        :return:  MAG_1_RAW_Y as int32_t; 
        """
        addr = 0x60
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_1_RAW_Y')
            reg.raw_value, = struct.unpack('>i', payload[0:4])
            mag_1_raw_y,  = struct.unpack('>i', payload[0:4])
            return reg, mag_1_raw_y, 

    @property
    def dreg_mag_1_raw_z(self):
        """
        Contains raw z axis magnetometer 1 data.
        Payload structure:
        [31:0]  : MAG_1_RAW_Z -- 32-bit signed integer value
        :return:  MAG_1_RAW_Z as int32_t; 
        """
        addr = 0x61
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_1_RAW_Z')
            reg.raw_value, = struct.unpack('>i', payload[0:4])
            mag_1_raw_z,  = struct.unpack('>i', payload[0:4])
            return reg, mag_1_raw_z, 

    @property
    def dreg_mag_1_raw_time(self):
        """
        Contains time at which the last magnetometer data from the magnetometer 1 was acquired.
        Payload structure:
        [31:0]  : MAG_1_RAW_TIME -- 32-bit IEEE Floating Point Value
        :return:  MAG_1_RAW_TIME as float; 
        """
        addr = 0x62
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_1_RAW_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_raw_time,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_raw_time, 

    @property
    def dreg_mag_2_raw_xy(self):
        """
        Contains raw X and Y axis magnetometer 2 data.
        Payload structure:
        [31:16] : MAG_2_RAW_X -- Magnetometer X (2s complement 16-bit integer)
        [15:0]  : MAG_2_RAW_Y -- Magnetometer Y (2s complement 16-bit integer)
        :return:  MAG_2_RAW_X as int16_t; MAG_2_RAW_Y as int16_t; 
        """
        addr = 0x63
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_2_RAW_XY')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            mag_2_raw_x, mag_2_raw_y = struct.unpack('>hh', payload[0:4])
            return reg, mag_2_raw_x, mag_2_raw_y

    @property
    def dreg_mag_2_raw_z(self):
        """
        Contains raw Z axis magnetometer 2 data.
        Payload structure:
        [31:16] : MAG_2_RAW_Z -- Magnetometer Z (2s complement 16-bit integer)
        :return:  MAG_2_RAW_Z as int16_t; 
        """
        addr = 0x64
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_2_RAW_Z')
            reg.raw_value, = struct.unpack('>hxx', payload[0:4])
            mag_2_raw_z,  = struct.unpack('>hxx', payload[0:4])
            return reg, mag_2_raw_z, 

    @property
    def dreg_mag_2_raw_time(self):
        """
        Contains time at which the last magnetometer data from the magnetometer 2 was acquired.
        Payload structure:
        [31:0]  : MAG_2_RAW_TIME -- 32-bit IEEE Floating Point Value
        :return:  MAG_2_RAW_TIME as float; 
        """
        addr = 0x65
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_2_RAW_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_raw_time,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_raw_time, 

    @property
    def dreg_temperature(self):
        """
        Contains the temperature output of the onboard temperature sensor.
        Payload structure:
        [31:0]  : TEMPERATURE -- Temperature in degrees Celcius (32-bit IEEE Floating Point)
        :return:  TEMPERATURE as float; 
        """
        addr = 0x66
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_TEMPERATURE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            temperature,  = struct.unpack('>f', payload[0:4])
            return reg, temperature, 

    @property
    def dreg_temperature_time(self):
        """
        Contains time at which the last temperature was acquired.
        Payload structure:
        [31:0]  : TEMPERATURE_TIME -- 32-bit IEEE Floating Point Value
        :return:  TEMPERATURE_TIME as float; 
        """
        addr = 0x67
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_TEMPERATURE_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            temperature_time,  = struct.unpack('>f', payload[0:4])
            return reg, temperature_time, 

    @property
    def dreg_gyro_1_proc_x(self):
        """
        Contains the actual measured angular rate from the gyro 1 for the x axis in degrees/sec after calibration has
        been applied.
        Payload structure:
        [31:0]  : GYRO_1_PROC_X -- Gyro X in degrees / sec (32-bit IEEE Floating Point Value)
        :return:  GYRO_1_PROC_X as float; 
        """
        addr = 0x68
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_1_PROC_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_proc_x,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_proc_x, 

    @property
    def dreg_gyro_1_proc_y(self):
        """
        Contains the actual measured angular rate from the gyro 1 for the y axis in degrees/sec after calibration has
        been applied.
        Payload structure:
        [31:0]  : GYRO_1_PROC_Y -- Gyro Y in degrees / sec (32-bit IEEE Floating Point Value)
        :return:  GYRO_1_PROC_Y as float; 
        """
        addr = 0x69
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_1_PROC_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_proc_y,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_proc_y, 

    @property
    def dreg_gyro_1_proc_z(self):
        """
        Contains the actual measured angular rate from the gyro 1 for the z axis in degrees/sec after calibration has
        been applied.
        Payload structure:
        [31:0]  : GYRO_1_PROC_Z -- Gyro Z in degrees / sec (32-bit IEEE Floating Point Value)
        :return:  GYRO_1_PROC_Z as float; 
        """
        addr = 0x6A
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_1_PROC_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_proc_z,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_proc_z, 

    @property
    def dreg_gyro_1_proc_time(self):
        """
        Contains the time at which the last rate gyro data from the gyro 1 was measured.
        Payload structure:
        [31:0]  : GYRO_1_PROC_TIME -- Gyro 1 time stamp (32-bit IEEE Floating Point Value)
        :return:  GYRO_1_PROC_TIME as float; 
        """
        addr = 0x6B
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_1_PROC_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_proc_time,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_proc_time, 

    @property
    def dreg_gyro_2_proc_x(self):
        """
        Contains the actual measured angular rate from the gyro 2 for the x axis in degrees/sec after calibration has
        been applied.
        Payload structure:
        [31:0]  : GYRO_2_PROC_X -- Gyro X in degrees / sec (32-bit IEEE Floating Point Value)
        :return:  GYRO_2_PROC_X as float; 
        """
        addr = 0x6C
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_2_PROC_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_proc_x,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_proc_x, 

    @property
    def dreg_gyro_2_proc_y(self):
        """
        Contains the actual measured angular rate from the gyro 2 for the y axis in degrees/sec after calibration has
        been applied.
        Payload structure:
        [31:0]  : GYRO_2_PROC_Y -- Gyro Y in degrees / sec (32-bit IEEE Floating Point Value)
        :return:  GYRO_2_PROC_Y as float; 
        """
        addr = 0x6D
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_2_PROC_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_proc_y,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_proc_y, 

    @property
    def dreg_gyro_2_proc_z(self):
        """
        Contains the actual measured angular rate from the gyro 2 for the z axis in degrees/sec after calibration has
        been applied.
        Payload structure:
        [31:0]  : GYRO_2_PROC_Z -- Gyro Z in degrees / sec (32-bit IEEE Floating Point Value)
        :return:  GYRO_2_PROC_Z as float; 
        """
        addr = 0x6E
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_2_PROC_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_proc_z,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_proc_z, 

    @property
    def dreg_gyro_2_proc_time(self):
        """
        Contains the time at which the last rate gyro data from the gyro 2 was measured.
        Payload structure:
        [31:0]  : GYRO_2_PROC_TIME -- Gyro 2 time stamp (32-bit IEEE Floating Point Value)
        :return:  GYRO_2_PROC_TIME as float; 
        """
        addr = 0x6F
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_2_PROC_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_proc_time,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_proc_time, 

    @property
    def dreg_accel_1_proc_x(self):
        """
        Contains the actual measured acceleration from the accelerometer 1 for the x axis in m/s2 after calibration
        has been applied.
        Payload structure:
        [31:0]  : ACCEL_1_PROC_X -- Acceleration X in m/s2 (32-bit IEEE Floating Point Value)
        :return:  ACCEL_1_PROC_X as float; 
        """
        addr = 0x70
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_ACCEL_1_PROC_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_proc_x,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_proc_x, 

    @property
    def dreg_accel_1_proc_y(self):
        """
        Contains the actual measured acceleration from the accelerometer 1 for the y axis in m/s2 after calibration
        has been applied.
        Payload structure:
        [31:0]  : ACCEL_1_PROC_Y -- Acceleration Y in m/s2 (32-bit IEEE Floating Point Value)
        :return:  ACCEL_1_PROC_Y as float; 
        """
        addr = 0x71
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_ACCEL_1_PROC_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_proc_y,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_proc_y, 

    @property
    def dreg_accel_1_proc_z(self):
        """
        Contains the actual measured acceleration from the accelerometer 1 for the z axis in m/s2 after calibration
        has been applied.
        Payload structure:
        [31:0]  : ACCEL_1_PROC_Z -- Acceleration Z in m/s2 (32-bit IEEE Floating Point Value)
        :return:  ACCEL_1_PROC_Z as float; 
        """
        addr = 0x72
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_ACCEL_1_PROC_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_proc_z,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_proc_z, 

    @property
    def dreg_accel_1_proc_time(self):
        """
        Contains the time at which the last acceleration data from the accelerometer 1 was measured.
        Payload structure:
        [31:0]  : ACCEL_1_PROC_TIME -- Accelerometer 1 time stamp (32-bit IEEE Floating Point Value)
        :return:  ACCEL_1_PROC_TIME as float; 
        """
        addr = 0x73
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_ACCEL_1_PROC_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            accel_1_proc_time,  = struct.unpack('>f', payload[0:4])
            return reg, accel_1_proc_time, 

    @property
    def dreg_mag_1_proc_x(self):
        """
        Contains the actual measured magnetic field from the magnetometer 1 for the x axis in mT after calibration has
        been applied.
        Payload structure:
        [31:0]  : MAG_1_PROC_X -- Magnetometer X in mT (32-bit IEEE Floating Point Value)
        :return:  MAG_1_PROC_X as float; 
        """
        addr = 0x74
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_1_PROC_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_proc_x,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_proc_x, 

    @property
    def dreg_mag_1_proc_y(self):
        """
        Contains the actual measured magnetic field from the magnetometer 1 for the y axis in mT after calibration has
        been applied.
        Payload structure:
        [31:0]  : MAG_1_PROC_Y -- Magnetometer Y in mT (32-bit IEEE Floating Point Value)
        :return:  MAG_1_PROC_Y as float; 
        """
        addr = 0x75
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_1_PROC_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_proc_y,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_proc_y, 

    @property
    def dreg_mag_1_proc_z(self):
        """
        Contains the actual measured magnetic field from the magnetometer 1 for the z axis in mT after calibration has
        been applied.
        Payload structure:
        [31:0]  : MAG_1_PROC_Z -- Magnetometer Z in mT (32-bit IEEE Floating Point Value)
        :return:  MAG_1_PROC_Z as float; 
        """
        addr = 0x76
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_1_PROC_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_proc_z,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_proc_z, 

    @property
    def dreg_mag_1_norm(self):
        """
        Contains the L2-norm (magnetic norm) for the measured magnetic field from the magnetometer 1 computed over the
        calibrated values.
        Payload structure:
        [31:0]  : MAG_1_NORM -- Magnetic norm (32-bit IEEE Floating Point Value)
        :return:  MAG_1_NORM as float; 
        """
        addr = 0x77
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_1_NORM')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_norm,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_norm, 

    @property
    def dreg_mag_1_proc_time(self):
        """
        Contains the time stamp at which the calibrated magnetometer 1 data was acquired.
        Payload structure:
        [31:0]  : MAG_1_PROC_TIME -- Magnetometer 1 time stamp (32-bit IEEE Floating Point Value)
        :return:  MAG_1_PROC_TIME as float; 
        """
        addr = 0x78
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_1_PROC_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_1_proc_time,  = struct.unpack('>f', payload[0:4])
            return reg, mag_1_proc_time, 

    @property
    def dreg_mag_2_proc_x(self):
        """
        Contains the actual measured magnetic field from the magnetometer 2 for the x axis in mT after calibration has
        been applied.
        Payload structure:
        [31:0]  : MAG_2_PROC_X -- Magnetometer X in mT (32-bit IEEE Floating Point Value)
        :return:  MAG_2_PROC_X as float; 
        """
        addr = 0x79
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_2_PROC_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_proc_x,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_proc_x, 

    @property
    def dreg_mag_2_proc_y(self):
        """
        Contains the actual measured magnetic field from the magnetometer 2 for the y axis in mT after calibration has
        been applied.
        Payload structure:
        [31:0]  : MAG_2_PROC_Y -- Magnetometer Y in mT (32-bit IEEE Floating Point Value)
        :return:  MAG_2_PROC_Y as float; 
        """
        addr = 0x7A
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_2_PROC_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_proc_y,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_proc_y, 

    @property
    def dreg_mag_2_proc_z(self):
        """
        Contains the actual measured magnetic field from the magnetometer 2 for the z axis in mT after calibration has
        been applied.
        Payload structure:
        [31:0]  : MAG_2_PROC_Z -- Magnetometer Z in mT (32-bit IEEE Floating Point Value)
        :return:  MAG_2_PROC_Z as float; 
        """
        addr = 0x7B
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_2_PROC_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_proc_z,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_proc_z, 

    @property
    def dreg_mag_2_norm(self):
        """
        Contains the L2-norm (magnetic norm) for the measured magnetic field from the magnetometer 2 computed over the
        calibrated values.
        Payload structure:
        [31:0]  : MAG_2_NORM -- Magnetic norm (32-bit IEEE Floating Point Value)
        :return:  MAG_2_NORM as float; 
        """
        addr = 0x7C
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_2_NORM')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_norm,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_norm, 

    @property
    def dreg_mag_2_proc_time(self):
        """
        Contains the time stamp at which the calibrated magnetometer 2 data was acquired.
        Payload structure:
        [31:0]  : MAG_2_PROC_TIME -- Magnetometer 2 time stamp (32-bit IEEE Floating Point Value)
        :return:  MAG_2_PROC_TIME as float; 
        """
        addr = 0x7D
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_MAG_2_PROC_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            mag_2_proc_time,  = struct.unpack('>f', payload[0:4])
            return reg, mag_2_proc_time, 

    @property
    def dreg_quat_ab(self):
        """
        Contains the first two components (a and b) of the estimated quaternion attitude.
        Payload structure:
        [31:16] : QUAT_A -- First quaternion component. Stored as a 16-bit signed integer. To get the actual value, divide by 29789.09091.
        [15:0]  : QUAT_B -- Second quaternion component. Stored as a 16-bit signed integer. To get the actual value, divide by 29789.09091.
        :return:  QUAT_A as int16_t; QUAT_B as int16_t; 
        """
        addr = 0x7E
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_QUAT_AB')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            quat_a, quat_b = struct.unpack('>hh', payload[0:4])
            return reg, quat_a, quat_b

    @property
    def dreg_quat_cd(self):
        """
        Contains the second two components (c and d) of the estimated quaternion attitude.
        Payload structure:
        [31:16] : QUAT_C -- Third quaternion component. Stored as a 16-bit signed integer. To get the actual value, divide by 29789.09091.
        [15:0]  : QUAT_D -- Fourth quaternion component. Stored as a 16-bit signed integer. To get the actual value, divide by 29789.09091.
        :return:  QUAT_C as int16_t; QUAT_D as int16_t; 
        """
        addr = 0x7F
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_QUAT_CD')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            quat_c, quat_d = struct.unpack('>hh', payload[0:4])
            return reg, quat_c, quat_d

    @property
    def dreg_quat_time(self):
        """
        Contains the time that the quaternion attitude was estimated.
        Payload structure:
        [31:0]  : QUAT_TIME -- Quaternion time (32-bit IEEE Floating Point Value)
        :return:  QUAT_TIME as float; 
        """
        addr = 0x80
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_QUAT_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            quat_time,  = struct.unpack('>f', payload[0:4])
            return reg, quat_time, 

    @property
    def dreg_euler_phi_theta(self):
        """
        Contains the pitch and roll angle estimates.
        Payload structure:
        [31:16] : PHI -- Roll angle. Stored as a 16-bit signed integer. To get the actual value, divide by 91.02222.
        [15:0]  : THETA -- Pitch angle. Stored as a 16-bit signed integer. To get the actual value, divide by 91.02222.
        :return:  PHI as int16_t; THETA as int16_t; 
        """
        addr = 0x81
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_EULER_PHI_THETA')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            phi, theta = struct.unpack('>hh', payload[0:4])
            return reg, phi, theta

    @property
    def dreg_euler_psi(self):
        """
        Contains the yaw angle estimate.
        Payload structure:
        [31:16] : PSI -- Yaw angle. Stored as a 16-bit signed integer. To get the actual value, divide by 91.02222.
        :return:  PSI as int16_t; 
        """
        addr = 0x82
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_EULER_PSI')
            reg.raw_value, = struct.unpack('>hxx', payload[0:4])
            psi,  = struct.unpack('>hxx', payload[0:4])
            return reg, psi, 

    @property
    def dreg_euler_phi_theta_dot(self):
        """
        Contains the pitch and roll rate estimates.
        Payload structure:
        [31:16] : PHI_DOT -- Roll rate. Stored as a 16-bit signed integer. To get the actual value, divide by 16.0.
        [15:0]  : THETA_DOT -- Pitch rate. Stored as a 16-bit signed integer. To get the actual value, divide by 16.0.
        :return:  PHI_DOT as int16_t; THETA_DOT as int16_t; 
        """
        addr = 0x83
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_EULER_PHI_THETA_DOT')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            phi_dot, theta_dot = struct.unpack('>hh', payload[0:4])
            return reg, phi_dot, theta_dot

    @property
    def dreg_euler_psi_dot(self):
        """
        Contains the yaw rate estimate.
        Payload structure:
        [31:16] : PSI_DOT -- Yaw rate. Stored as a 16-bit signed integer. To get the actual value, divide by 16.0.
        :return:  PSI_DOT as int16_t; 
        """
        addr = 0x84
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_EULER_PSI_DOT')
            reg.raw_value, = struct.unpack('>hxx', payload[0:4])
            psi_dot,  = struct.unpack('>hxx', payload[0:4])
            return reg, psi_dot, 

    @property
    def dreg_euler_time(self):
        """
        Contains the time that the Euler Angles were estimated.
        Payload structure:
        [31:0]  : EULER_TIME -- Euler time (32-bit IEEE Floating Point Value)
        :return:  EULER_TIME as float; 
        """
        addr = 0x85
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_EULER_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            euler_time,  = struct.unpack('>f', payload[0:4])
            return reg, euler_time, 

    @property
    def dreg_position_north(self):
        """
        Contains the measured north position in meters from the latitude specified in CREG_HOME_NORTH.
        Payload structure:
        [31:0]  : POSITION_NORTH -- North Position (32-bit IEEE Floating Point Value)
        :return:  POSITION_NORTH as float; 
        """
        addr = 0x86
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_POSITION_NORTH')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            position_north,  = struct.unpack('>f', payload[0:4])
            return reg, position_north, 

    @property
    def dreg_position_east(self):
        """
        Contains the measured east position in meters from the longitude specified in CREG_HOME_EAST.
        Payload structure:
        [31:0]  : POSITION_EAST -- East Position (32-bit IEEE Floating Point Value)
        :return:  POSITION_EAST as float; 
        """
        addr = 0x87
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_POSITION_EAST')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            position_east,  = struct.unpack('>f', payload[0:4])
            return reg, position_east, 

    @property
    def dreg_position_up(self):
        """
        Contains the measured altitude in meters from the altitude specified in CREG_HOME_UP.
        Payload structure:
        [31:0]  : POSITION_UP -- Altitude (32-bit IEEE Floating Point Value)
        :return:  POSITION_UP as float; 
        """
        addr = 0x88
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_POSITION_UP')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            position_up,  = struct.unpack('>f', payload[0:4])
            return reg, position_up, 

    @property
    def dreg_position_time(self):
        """
        Contains the time at which the position was acquired.
        Payload structure:
        [31:0]  : POSITION_TIME -- Position Time (32-bit IEEE Floating Point Value)
        :return:  POSITION_TIME as float; 
        """
        addr = 0x89
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_POSITION_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            position_time,  = struct.unpack('>f', payload[0:4])
            return reg, position_time, 

    @property
    def dreg_velocity_north(self):
        """
        Contains the measured north velocity in m/s.
        Payload structure:
        [31:0]  : VELOCITY_NORTH -- North Velocity (32-bit IEEE Floating Point Value)
        :return:  VELOCITY_NORTH as float; 
        """
        addr = 0x8A
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_VELOCITY_NORTH')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            velocity_north,  = struct.unpack('>f', payload[0:4])
            return reg, velocity_north, 

    @property
    def dreg_velocity_east(self):
        """
        Contains the measured east velocity in m/s.
        Payload structure:
        [31:0]  : VELOCITY_EAST -- East Velocity (32-bit IEEE Floating Point Value)
        :return:  VELOCITY_EAST as float; 
        """
        addr = 0x8B
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_VELOCITY_EAST')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            velocity_east,  = struct.unpack('>f', payload[0:4])
            return reg, velocity_east, 

    @property
    def dreg_velocity_up(self):
        """
        Contains the measured altitude velocity in m/s.
        Payload structure:
        [31:0]  : VELOCITY_UP -- Altitude Velocity (32-bit IEEE Floating Point Value)
        :return:  VELOCITY_UP as float; 
        """
        addr = 0x8C
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_VELOCITY_UP')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            velocity_up,  = struct.unpack('>f', payload[0:4])
            return reg, velocity_up, 

    @property
    def dreg_velocity_time(self):
        """
        Contains the time at which the velocity was measured.
        Payload structure:
        [31:0]  : VELOCITY_TIME -- Velocity time (32-bit IEEE Floating Point Value)
        :return:  VELOCITY_TIME as float; 
        """
        addr = 0x8D
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_VELOCITY_TIME')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            velocity_time,  = struct.unpack('>f', payload[0:4])
            return reg, velocity_time, 

    @property
    def dreg_gyro_1_bias_x(self):
        """
        Contains the estimated x-axis bias for the gyro 1 in degrees/s.
        Payload structure:
        [31:0]  : GYRO_1_BIAS_X -- Gyro 1 bias X (32-bit IEEE Floating Point Value)
        :return:  GYRO_1_BIAS_X as float; 
        """
        addr = 0x8E
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_1_BIAS_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_bias_x,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_bias_x, 

    @property
    def dreg_gyro_1_bias_y(self):
        """
        Contains the estimated y-axis bias for the gyro 1 in degrees/s.
        Payload structure:
        [31:0]  : GYRO_1_BIAS_Y -- Gyro 1 bias Y (32-bit IEEE Floating Point Value)
        :return:  GYRO_1_BIAS_Y as float; 
        """
        addr = 0x8F
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_1_BIAS_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_bias_y,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_bias_y, 

    @property
    def dreg_gyro_1_bias_z(self):
        """
        Contains the estimated z-axis bias for the gyro 1 in degrees/s.
        Payload structure:
        [31:0]  : GYRO_1_BIAS_Z -- Gyro 1 bias Z (32-bit IEEE Floating Point Value)
        :return:  GYRO_1_BIAS_Z as float; 
        """
        addr = 0x90
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_1_BIAS_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_1_bias_z,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_1_bias_z, 

    @property
    def dreg_gyro_2_bias_x(self):
        """
        Contains the estimated x-axis bias for the gyro 2 in degrees/s.
        Payload structure:
        [31:0]  : GYRO_2_BIAS_X -- Gyro 2 bias X (32-bit IEEE Floating Point Value)
        :return:  GYRO_2_BIAS_X as float; 
        """
        addr = 0x91
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_2_BIAS_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_bias_x,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_bias_x, 

    @property
    def dreg_gyro_2_bias_y(self):
        """
        Contains the estimated y-axis bias for the gyro 2 in degrees/s.
        Payload structure:
        [31:0]  : GYRO_2_BIAS_Y -- Gyro 2 bias Y (32-bit IEEE Floating Point Value)
        :return:  GYRO_2_BIAS_Y as float; 
        """
        addr = 0x92
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_2_BIAS_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_bias_y,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_bias_y, 

    @property
    def dreg_gyro_2_bias_z(self):
        """
        Contains the estimated z-axis bias for the gyro 2 in degrees/s.
        Payload structure:
        [31:0]  : GYRO_2_BIAS_Z -- Gyro 2 bias Z (32-bit IEEE Floating Point Value)
        :return:  GYRO_2_BIAS_Z as float; 
        """
        addr = 0x93
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='DREG_GYRO_2_BIAS_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            gyro_2_bias_z,  = struct.unpack('>f', payload[0:4])
            return reg, gyro_2_bias_z, 

    @property
    def get_fw_build_id(self):
        """
        Firmware build identification string: a four byte ASCII character sequence which corresponds to a firmware
        series.
        Payload structure:
        [31:0]  : FW_BUILD_ID -- Firmware Build ID string
        :return:  FW_BUILD_ID as string; 
        """
        addr = 0xAA
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='GET_FW_BUILD_ID')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            fw_build_id = struct.unpack('>4s', payload[0:4])[0].decode('utf-8')
            return fw_build_id

    @property
    def get_fw_build_version(self):
        """
        Firmware build version provides the unique identifier of the firmware programmed in the board. A response is
        four bytes long and identifies major and minor build version, and the build number.
        Payload structure:
        [31:24] : VERSION_MAJOR -- 8-bit unsigned integer major version number
        [23:16] : VERSION_MINOR -- 8-bit unsigned integer minor version number
        [15:0]  : BUILD_ID -- 16-bit unsigned integer build ID number
        :return:  VERSION_MAJOR as uint8_t; VERSION_MINOR as uint8_t; BUILD_ID as uint16_t; 
        """
        addr = 0xAB
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='GET_FW_BUILD_VERSION')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            version_major, version_minor, build_id = struct.unpack('>BBH', payload[0:4])
            return reg, version_major, version_minor, build_id

    @property
    def flash_commit(self):
        raise RuntimeError('flash_commit has no getter! The register flash_commit is write-only!')

    @flash_commit.setter
    def flash_commit(self, new_value):
        addr = 0xAC
        self.write_register(addr, new_value)

    @property
    def reset_to_factory(self):
        raise RuntimeError('reset_to_factory has no getter! The register reset_to_factory is write-only!')

    @reset_to_factory.setter
    def reset_to_factory(self, new_value):
        addr = 0xAD
        self.write_register(addr, new_value)

    @property
    def zero_gyros(self):
        raise RuntimeError('zero_gyros has no getter! The register zero_gyros is write-only!')

    @zero_gyros.setter
    def zero_gyros(self, new_value):
        addr = 0xAE
        self.write_register(addr, new_value)

    @property
    def set_home_position(self):
        raise RuntimeError('set_home_position has no getter! The register set_home_position is write-only!')

    @set_home_position.setter
    def set_home_position(self, new_value):
        addr = 0xB0
        self.write_register(addr, new_value)

    @property
    def set_mag_reference(self):
        raise RuntimeError('set_mag_reference has no getter! The register set_mag_reference is write-only!')

    @set_mag_reference.setter
    def set_mag_reference(self, new_value):
        addr = 0xB1
        self.write_register(addr, new_value)

    @property
    def calibrate_accelerometers(self):
        raise RuntimeError('calibrate_accelerometers has no getter! The register calibrate_accelerometers is write-only!')

    @calibrate_accelerometers.setter
    def calibrate_accelerometers(self, new_value):
        addr = 0xB2
        self.write_register(addr, new_value)

    @property
    def reset_fusion(self):
        raise RuntimeError('reset_fusion has no getter! The register reset_fusion is write-only!')

    @reset_fusion.setter
    def reset_fusion(self, new_value):
        addr = 0xB3
        self.write_register(addr, new_value)

    @property
    def enable_zupt(self):
        raise RuntimeError('enable_zupt has no getter! The register enable_zupt is write-only!')

    @enable_zupt.setter
    def enable_zupt(self, new_value):
        addr = 0xB4
        self.write_register(addr, new_value)

    @property
    def euler_mode(self):
        raise RuntimeError('euler_mode has no getter! The register euler_mode is write-only!')

    @euler_mode.setter
    def euler_mode(self, new_value):
        addr = 0xB5
        self.write_register(addr, new_value)

    @property
    def quaternion_mode(self):
        raise RuntimeError('quaternion_mode has no getter! The register quaternion_mode is write-only!')

    @quaternion_mode.setter
    def quaternion_mode(self, new_value):
        addr = 0xB6
        self.write_register(addr, new_value)

    @property
    def enable_rt_calibration(self):
        raise RuntimeError('enable_rt_calibration has no getter! The register enable_rt_calibration is write-only!')

    @enable_rt_calibration.setter
    def enable_rt_calibration(self, new_value):
        addr = 0xB7
        self.write_register(addr, new_value)

    @property
    def en_mag_anomaly_detection(self):
        raise RuntimeError('en_mag_anomaly_detection has no getter! The register en_mag_anomaly_detection is write-only!')

    @en_mag_anomaly_detection.setter
    def en_mag_anomaly_detection(self, new_value):
        addr = 0xB8
        self.write_register(addr, new_value)

    @property
    def run_self_tests(self):
        raise RuntimeError('run_self_tests has no getter! The register run_self_tests is write-only!')

    @run_self_tests.setter
    def run_self_tests(self, new_value):
        addr = 0xB9
        self.write_register(addr, new_value)

    @property
    def enable_external_event(self):
        raise RuntimeError('enable_external_event has no getter! The register enable_external_event is write-only!')

    @enable_external_event.setter
    def enable_external_event(self, new_value):
        addr = 0xBA
        self.write_register(addr, new_value)

    @property
    def enable_gnns_fusion(self):
        raise RuntimeError('enable_gnns_fusion has no getter! The register enable_gnns_fusion is write-only!')

    @enable_gnns_fusion.setter
    def enable_gnns_fusion(self, new_value):
        addr = 0xBB
        self.write_register(addr, new_value)

    @property
    def enable_usr_euler_output(self):
        raise RuntimeError('enable_usr_euler_output has no getter! The register enable_usr_euler_output is write-only!')

    @enable_usr_euler_output.setter
    def enable_usr_euler_output(self, new_value):
        addr = 0xBC
        self.write_register(addr, new_value)

    @property
    def enable_dead_reckoning(self):
        raise RuntimeError('enable_dead_reckoning has no getter! The register enable_dead_reckoning is write-only!')

    @enable_dead_reckoning.setter
    def enable_dead_reckoning(self, new_value):
        addr = 0xBD
        self.write_register(addr, new_value)

    @property
    def enable_heave_sway_surge(self):
        raise RuntimeError('enable_heave_sway_surge has no getter! The register enable_heave_sway_surge is write-only!')

    @enable_heave_sway_surge.setter
    def enable_heave_sway_surge(self, new_value):
        addr = 0xBE
        self.write_register(addr, new_value)

    @property
    def enable_ukf(self):
        raise RuntimeError('enable_ukf has no getter! The register enable_ukf is write-only!')

    @enable_ukf.setter
    def enable_ukf(self, new_value):
        addr = 0xBF
        self.write_register(addr, new_value)

    @property
    def board_unique_id_1(self):
        """
        First 32-bits of the 64-bits of the board unique identifier. Bits of the unique identifier cannot be modified
        by the user.
        Payload structure:
        [31:0]  : BOARD_UNIQUE_ID_1_BITS -- Board unique ID bits
        :return:  BOARD_UNIQUE_ID_1_BITS as uint32_t; 
        """
        addr = 0xFD
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='BOARD_UNIQUE_ID_1')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            board_unique_id_1_bits,  = struct.unpack('>I', payload[0:4])
            return reg, board_unique_id_1_bits, 

    @property
    def board_unique_id_2(self):
        """
        Last 32-bits of the 64-bits of the board unique identifier. Bits of the unique identifier cannot be modified
        by the user.
        Payload structure:
        [31:0]  : BOARD_UNIQUE_ID_2_BITS -- Board unique ID bits
        :return:  BOARD_UNIQUE_ID_2_BITS as uint32_t; 
        """
        addr = 0xFE
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='BOARD_UNIQUE_ID_2')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            board_unique_id_2_bits,  = struct.unpack('>I', payload[0:4])
            return reg, board_unique_id_2_bits, 

    @property
    def protocol_version(self):
        """
        String version of the protocol.
        Payload structure:
        [31:0]  : PROTOCOL_VERSION_STR -- Protocol version string
        :return:  PROTOCOL_VERSION_STR as string; 
        """
        addr = 0xFF
        ok, payload = self.read_register(addr)
        if ok:
            reg = self.svd_parser.find_register_by(name='PROTOCOL_VERSION')
            reg.raw_value, = struct.unpack('>I', payload[0:4])
            protocol_version_str = struct.unpack('>4s', payload[0:4])[0].decode('utf-8')
            return protocol_version_str


    @property
    def hidden_gyro_1_variance(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_VARIANCE -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_VARIANCE as float; 
        """
        addr = 0x00
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_VARIANCE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_variance,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_variance, 

    @hidden_gyro_1_variance.setter
    def hidden_gyro_1_variance(self, new_value):
        addr = 0x00
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_2_variance(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_VARIANCE -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_VARIANCE as float; 
        """
        addr = 0x01
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_VARIANCE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_variance,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_variance, 

    @hidden_gyro_2_variance.setter
    def hidden_gyro_2_variance(self, new_value):
        addr = 0x01
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_accel_1_variance(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_VARIANCE -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_VARIANCE as float; 
        """
        addr = 0x02
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_VARIANCE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_variance,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_variance, 

    @hidden_accel_1_variance.setter
    def hidden_accel_1_variance(self, new_value):
        addr = 0x02
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_variance(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_VARIANCE -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_VARIANCE as float; 
        """
        addr = 0x03
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_VARIANCE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_variance,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_variance, 

    @hidden_mag_1_variance.setter
    def hidden_mag_1_variance(self, new_value):
        addr = 0x03
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_variance(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_VARIANCE -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_VARIANCE as float; 
        """
        addr = 0x04
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_VARIANCE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_variance,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_variance, 

    @hidden_mag_2_variance.setter
    def hidden_mag_2_variance(self, new_value):
        addr = 0x04
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gps_course_variance(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GPS_COURSE_VARIANCE -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GPS_COURSE_VARIANCE as float; 
        """
        addr = 0x05
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GPS_COURSE_VARIANCE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gps_course_variance,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gps_course_variance, 

    @hidden_gps_course_variance.setter
    def hidden_gps_course_variance(self, new_value):
        addr = 0x05
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gps_position_variance(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GPS_POSITION_VARIANCE -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GPS_POSITION_VARIANCE as float; 
        """
        addr = 0x06
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GPS_POSITION_VARIANCE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gps_position_variance,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gps_position_variance, 

    @hidden_gps_position_variance.setter
    def hidden_gps_position_variance(self, new_value):
        addr = 0x06
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gps_velocity_variance(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GPS_VELOCITY_VARIANCE -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GPS_VELOCITY_VARIANCE as float; 
        """
        addr = 0x07
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GPS_VELOCITY_VARIANCE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gps_velocity_variance,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gps_velocity_variance, 

    @hidden_gps_velocity_variance.setter
    def hidden_gps_velocity_variance(self, new_value):
        addr = 0x07
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_static_press_variance(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_STATIC_PRESS_VARIANCE -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_STATIC_PRESS_VARIANCE as float; 
        """
        addr = 0x08
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_STATIC_PRESS_VARIANCE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_static_press_variance,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_static_press_variance, 

    @hidden_static_press_variance.setter
    def hidden_static_press_variance(self, new_value):
        addr = 0x08
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_diff_press_variance(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_DIFF_PRESS_VARIANCE -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_DIFF_PRESS_VARIANCE as float; 
        """
        addr = 0x09
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_DIFF_PRESS_VARIANCE')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_diff_press_variance,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_diff_press_variance, 

    @hidden_diff_press_variance.setter
    def hidden_diff_press_variance(self, new_value):
        addr = 0x09
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_q_uvw(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_Q_UVW -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_Q_UVW as float; 
        """
        addr = 0x0A
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_Q_UVW')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_q_uvw,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_q_uvw, 

    @hidden_q_uvw.setter
    def hidden_q_uvw(self, new_value):
        addr = 0x0A
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_q_quaternion(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_Q_QUATERNION -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_Q_QUATERNION as float; 
        """
        addr = 0x0B
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_Q_QUATERNION')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_q_quaternion,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_q_quaternion, 

    @hidden_q_quaternion.setter
    def hidden_q_quaternion(self, new_value):
        addr = 0x0B
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_q_gps_position(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_Q_GPS_POSITION -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_Q_GPS_POSITION as float; 
        """
        addr = 0x0C
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_Q_GPS_POSITION')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_q_gps_position,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_q_gps_position, 

    @hidden_q_gps_position.setter
    def hidden_q_gps_position(self, new_value):
        addr = 0x0C
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_q_bias(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_Q_BIAS -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_Q_BIAS as float; 
        """
        addr = 0x0D
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_Q_BIAS')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_q_bias,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_q_bias, 

    @hidden_q_bias.setter
    def hidden_q_bias(self, new_value):
        addr = 0x0D
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_q_euler_angles(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_Q_EULER_ANGLES -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_Q_EULER_ANGLES as float; 
        """
        addr = 0x0E
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_Q_EULER_ANGLES')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_q_euler_angles,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_q_euler_angles, 

    @hidden_q_euler_angles.setter
    def hidden_q_euler_angles(self, new_value):
        addr = 0x0E
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_low_vg_accel_noise_factor(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_LOW_VG_ACCEL_NOISE_FACTOR -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_LOW_VG_ACCEL_NOISE_FACTOR as float; 
        """
        addr = 0x0F
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_LOW_VG_ACCEL_NOISE_FACTOR')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_low_vg_accel_noise_factor,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_low_vg_accel_noise_factor, 

    @hidden_low_vg_accel_noise_factor.setter
    def hidden_low_vg_accel_noise_factor(self, new_value):
        addr = 0x0F
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_lpf_tau_groundspeed(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_LPF_TAU_GROUNDSPEED -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_LPF_TAU_GROUNDSPEED as float; 
        """
        addr = 0x10
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_LPF_TAU_GROUNDSPEED')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_lpf_tau_groundspeed,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_lpf_tau_groundspeed, 

    @hidden_lpf_tau_groundspeed.setter
    def hidden_lpf_tau_groundspeed(self, new_value):
        addr = 0x10
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_lpf_tau_gyro_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_LPF_TAU_GYRO_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_LPF_TAU_GYRO_1 as float; 
        """
        addr = 0x11
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_LPF_TAU_GYRO_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_lpf_tau_gyro_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_lpf_tau_gyro_1, 

    @hidden_lpf_tau_gyro_1.setter
    def hidden_lpf_tau_gyro_1(self, new_value):
        addr = 0x11
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_lpf_tau_gyro_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_LPF_TAU_GYRO_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_LPF_TAU_GYRO_2 as float; 
        """
        addr = 0x12
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_LPF_TAU_GYRO_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_lpf_tau_gyro_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_lpf_tau_gyro_2, 

    @hidden_lpf_tau_gyro_2.setter
    def hidden_lpf_tau_gyro_2(self, new_value):
        addr = 0x12
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_lpf_tau_accel_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_LPF_TAU_ACCEL_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_LPF_TAU_ACCEL_1 as float; 
        """
        addr = 0x13
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_LPF_TAU_ACCEL_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_lpf_tau_accel_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_lpf_tau_accel_1, 

    @hidden_lpf_tau_accel_1.setter
    def hidden_lpf_tau_accel_1(self, new_value):
        addr = 0x13
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_lpf_tau_mag_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_LPF_TAU_MAG_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_LPF_TAU_MAG_1 as float; 
        """
        addr = 0x14
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_LPF_TAU_MAG_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_lpf_tau_mag_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_lpf_tau_mag_1, 

    @hidden_lpf_tau_mag_1.setter
    def hidden_lpf_tau_mag_1(self, new_value):
        addr = 0x14
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_lpf_tau_mag_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_LPF_TAU_MAG_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_LPF_TAU_MAG_2 as float; 
        """
        addr = 0x15
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_LPF_TAU_MAG_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_lpf_tau_mag_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_lpf_tau_mag_2, 

    @hidden_lpf_tau_mag_2.setter
    def hidden_lpf_tau_mag_2(self, new_value):
        addr = 0x15
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_x_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_X_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_X_POW_0 as float; 
        """
        addr = 0x16
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_X_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_x_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_x_pow_0, 

    @hidden_c_gyro_1_bias_x_pow_0.setter
    def hidden_c_gyro_1_bias_x_pow_0(self, new_value):
        addr = 0x16
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_x_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_X_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_X_POW_1 as float; 
        """
        addr = 0x17
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_X_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_x_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_x_pow_1, 

    @hidden_c_gyro_1_bias_x_pow_1.setter
    def hidden_c_gyro_1_bias_x_pow_1(self, new_value):
        addr = 0x17
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_x_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_X_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_X_POW_2 as float; 
        """
        addr = 0x18
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_X_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_x_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_x_pow_2, 

    @hidden_c_gyro_1_bias_x_pow_2.setter
    def hidden_c_gyro_1_bias_x_pow_2(self, new_value):
        addr = 0x18
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_x_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_X_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_X_POW_3 as float; 
        """
        addr = 0x19
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_X_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_x_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_x_pow_3, 

    @hidden_c_gyro_1_bias_x_pow_3.setter
    def hidden_c_gyro_1_bias_x_pow_3(self, new_value):
        addr = 0x19
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_y_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_Y_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_Y_POW_0 as float; 
        """
        addr = 0x1A
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_Y_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_y_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_y_pow_0, 

    @hidden_c_gyro_1_bias_y_pow_0.setter
    def hidden_c_gyro_1_bias_y_pow_0(self, new_value):
        addr = 0x1A
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_y_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_Y_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_Y_POW_1 as float; 
        """
        addr = 0x1B
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_Y_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_y_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_y_pow_1, 

    @hidden_c_gyro_1_bias_y_pow_1.setter
    def hidden_c_gyro_1_bias_y_pow_1(self, new_value):
        addr = 0x1B
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_y_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_Y_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_Y_POW_2 as float; 
        """
        addr = 0x1C
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_Y_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_y_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_y_pow_2, 

    @hidden_c_gyro_1_bias_y_pow_2.setter
    def hidden_c_gyro_1_bias_y_pow_2(self, new_value):
        addr = 0x1C
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_y_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_Y_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_Y_POW_3 as float; 
        """
        addr = 0x1D
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_Y_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_y_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_y_pow_3, 

    @hidden_c_gyro_1_bias_y_pow_3.setter
    def hidden_c_gyro_1_bias_y_pow_3(self, new_value):
        addr = 0x1D
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_z_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_Z_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_Z_POW_0 as float; 
        """
        addr = 0x1E
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_Z_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_z_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_z_pow_0, 

    @hidden_c_gyro_1_bias_z_pow_0.setter
    def hidden_c_gyro_1_bias_z_pow_0(self, new_value):
        addr = 0x1E
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_z_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_Z_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_Z_POW_1 as float; 
        """
        addr = 0x1F
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_Z_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_z_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_z_pow_1, 

    @hidden_c_gyro_1_bias_z_pow_1.setter
    def hidden_c_gyro_1_bias_z_pow_1(self, new_value):
        addr = 0x1F
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_z_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_Z_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_Z_POW_2 as float; 
        """
        addr = 0x20
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_Z_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_z_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_z_pow_2, 

    @hidden_c_gyro_1_bias_z_pow_2.setter
    def hidden_c_gyro_1_bias_z_pow_2(self, new_value):
        addr = 0x20
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_bias_z_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_BIAS_Z_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_BIAS_Z_POW_3 as float; 
        """
        addr = 0x21
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_BIAS_Z_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_bias_z_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_bias_z_pow_3, 

    @hidden_c_gyro_1_bias_z_pow_3.setter
    def hidden_c_gyro_1_bias_z_pow_3(self, new_value):
        addr = 0x21
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_x_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_X_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_X_POW_0 as float; 
        """
        addr = 0x22
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_X_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_x_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_x_pow_0, 

    @hidden_c_gyro_1_scale_x_pow_0.setter
    def hidden_c_gyro_1_scale_x_pow_0(self, new_value):
        addr = 0x22
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_x_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_X_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_X_POW_1 as float; 
        """
        addr = 0x23
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_X_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_x_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_x_pow_1, 

    @hidden_c_gyro_1_scale_x_pow_1.setter
    def hidden_c_gyro_1_scale_x_pow_1(self, new_value):
        addr = 0x23
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_x_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_X_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_X_POW_2 as float; 
        """
        addr = 0x24
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_X_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_x_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_x_pow_2, 

    @hidden_c_gyro_1_scale_x_pow_2.setter
    def hidden_c_gyro_1_scale_x_pow_2(self, new_value):
        addr = 0x24
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_x_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_X_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_X_POW_3 as float; 
        """
        addr = 0x25
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_X_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_x_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_x_pow_3, 

    @hidden_c_gyro_1_scale_x_pow_3.setter
    def hidden_c_gyro_1_scale_x_pow_3(self, new_value):
        addr = 0x25
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_y_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_Y_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_Y_POW_0 as float; 
        """
        addr = 0x26
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_Y_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_y_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_y_pow_0, 

    @hidden_c_gyro_1_scale_y_pow_0.setter
    def hidden_c_gyro_1_scale_y_pow_0(self, new_value):
        addr = 0x26
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_y_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_Y_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_Y_POW_1 as float; 
        """
        addr = 0x27
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_Y_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_y_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_y_pow_1, 

    @hidden_c_gyro_1_scale_y_pow_1.setter
    def hidden_c_gyro_1_scale_y_pow_1(self, new_value):
        addr = 0x27
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_y_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_Y_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_Y_POW_2 as float; 
        """
        addr = 0x28
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_Y_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_y_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_y_pow_2, 

    @hidden_c_gyro_1_scale_y_pow_2.setter
    def hidden_c_gyro_1_scale_y_pow_2(self, new_value):
        addr = 0x28
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_y_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_Y_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_Y_POW_3 as float; 
        """
        addr = 0x29
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_Y_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_y_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_y_pow_3, 

    @hidden_c_gyro_1_scale_y_pow_3.setter
    def hidden_c_gyro_1_scale_y_pow_3(self, new_value):
        addr = 0x29
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_z_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_Z_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_Z_POW_0 as float; 
        """
        addr = 0x2A
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_Z_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_z_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_z_pow_0, 

    @hidden_c_gyro_1_scale_z_pow_0.setter
    def hidden_c_gyro_1_scale_z_pow_0(self, new_value):
        addr = 0x2A
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_z_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_Z_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_Z_POW_1 as float; 
        """
        addr = 0x2B
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_Z_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_z_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_z_pow_1, 

    @hidden_c_gyro_1_scale_z_pow_1.setter
    def hidden_c_gyro_1_scale_z_pow_1(self, new_value):
        addr = 0x2B
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_z_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_Z_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_Z_POW_2 as float; 
        """
        addr = 0x2C
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_Z_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_z_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_z_pow_2, 

    @hidden_c_gyro_1_scale_z_pow_2.setter
    def hidden_c_gyro_1_scale_z_pow_2(self, new_value):
        addr = 0x2C
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_1_scale_z_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_1_SCALE_Z_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_1_SCALE_Z_POW_3 as float; 
        """
        addr = 0x2D
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_1_SCALE_Z_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_1_scale_z_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_1_scale_z_pow_3, 

    @hidden_c_gyro_1_scale_z_pow_3.setter
    def hidden_c_gyro_1_scale_z_pow_3(self, new_value):
        addr = 0x2D
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_1_alignment1_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_ALIGNMENT1_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_ALIGNMENT1_1 as float; 
        """
        addr = 0x2E
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_ALIGNMENT1_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_alignment1_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_alignment1_1, 

    @hidden_gyro_1_alignment1_1.setter
    def hidden_gyro_1_alignment1_1(self, new_value):
        addr = 0x2E
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_1_alignment1_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_ALIGNMENT1_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_ALIGNMENT1_2 as float; 
        """
        addr = 0x2F
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_ALIGNMENT1_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_alignment1_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_alignment1_2, 

    @hidden_gyro_1_alignment1_2.setter
    def hidden_gyro_1_alignment1_2(self, new_value):
        addr = 0x2F
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_1_alignment1_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_ALIGNMENT1_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_ALIGNMENT1_3 as float; 
        """
        addr = 0x30
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_ALIGNMENT1_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_alignment1_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_alignment1_3, 

    @hidden_gyro_1_alignment1_3.setter
    def hidden_gyro_1_alignment1_3(self, new_value):
        addr = 0x30
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_1_alignment2_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_ALIGNMENT2_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_ALIGNMENT2_1 as float; 
        """
        addr = 0x31
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_ALIGNMENT2_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_alignment2_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_alignment2_1, 

    @hidden_gyro_1_alignment2_1.setter
    def hidden_gyro_1_alignment2_1(self, new_value):
        addr = 0x31
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_1_alignment2_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_ALIGNMENT2_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_ALIGNMENT2_2 as float; 
        """
        addr = 0x32
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_ALIGNMENT2_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_alignment2_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_alignment2_2, 

    @hidden_gyro_1_alignment2_2.setter
    def hidden_gyro_1_alignment2_2(self, new_value):
        addr = 0x32
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_1_alignment2_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_ALIGNMENT2_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_ALIGNMENT2_3 as float; 
        """
        addr = 0x33
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_ALIGNMENT2_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_alignment2_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_alignment2_3, 

    @hidden_gyro_1_alignment2_3.setter
    def hidden_gyro_1_alignment2_3(self, new_value):
        addr = 0x33
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_1_alignment3_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_ALIGNMENT3_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_ALIGNMENT3_1 as float; 
        """
        addr = 0x34
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_ALIGNMENT3_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_alignment3_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_alignment3_1, 

    @hidden_gyro_1_alignment3_1.setter
    def hidden_gyro_1_alignment3_1(self, new_value):
        addr = 0x34
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_1_alignment3_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_ALIGNMENT3_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_ALIGNMENT3_2 as float; 
        """
        addr = 0x35
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_ALIGNMENT3_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_alignment3_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_alignment3_2, 

    @hidden_gyro_1_alignment3_2.setter
    def hidden_gyro_1_alignment3_2(self, new_value):
        addr = 0x35
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_1_alignment3_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_ALIGNMENT3_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_ALIGNMENT3_3 as float; 
        """
        addr = 0x36
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_ALIGNMENT3_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_alignment3_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_alignment3_3, 

    @hidden_gyro_1_alignment3_3.setter
    def hidden_gyro_1_alignment3_3(self, new_value):
        addr = 0x36
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_x_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_X_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_X_POW_0 as float; 
        """
        addr = 0x37
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_X_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_x_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_x_pow_0, 

    @hidden_c_gyro_2_bias_x_pow_0.setter
    def hidden_c_gyro_2_bias_x_pow_0(self, new_value):
        addr = 0x37
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_x_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_X_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_X_POW_1 as float; 
        """
        addr = 0x38
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_X_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_x_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_x_pow_1, 

    @hidden_c_gyro_2_bias_x_pow_1.setter
    def hidden_c_gyro_2_bias_x_pow_1(self, new_value):
        addr = 0x38
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_x_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_X_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_X_POW_2 as float; 
        """
        addr = 0x39
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_X_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_x_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_x_pow_2, 

    @hidden_c_gyro_2_bias_x_pow_2.setter
    def hidden_c_gyro_2_bias_x_pow_2(self, new_value):
        addr = 0x39
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_x_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_X_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_X_POW_3 as float; 
        """
        addr = 0x3A
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_X_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_x_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_x_pow_3, 

    @hidden_c_gyro_2_bias_x_pow_3.setter
    def hidden_c_gyro_2_bias_x_pow_3(self, new_value):
        addr = 0x3A
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_y_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_Y_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_Y_POW_0 as float; 
        """
        addr = 0x3B
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_Y_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_y_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_y_pow_0, 

    @hidden_c_gyro_2_bias_y_pow_0.setter
    def hidden_c_gyro_2_bias_y_pow_0(self, new_value):
        addr = 0x3B
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_y_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_Y_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_Y_POW_1 as float; 
        """
        addr = 0x3C
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_Y_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_y_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_y_pow_1, 

    @hidden_c_gyro_2_bias_y_pow_1.setter
    def hidden_c_gyro_2_bias_y_pow_1(self, new_value):
        addr = 0x3C
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_y_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_Y_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_Y_POW_2 as float; 
        """
        addr = 0x3D
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_Y_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_y_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_y_pow_2, 

    @hidden_c_gyro_2_bias_y_pow_2.setter
    def hidden_c_gyro_2_bias_y_pow_2(self, new_value):
        addr = 0x3D
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_y_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_Y_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_Y_POW_3 as float; 
        """
        addr = 0x3E
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_Y_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_y_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_y_pow_3, 

    @hidden_c_gyro_2_bias_y_pow_3.setter
    def hidden_c_gyro_2_bias_y_pow_3(self, new_value):
        addr = 0x3E
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_z_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_Z_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_Z_POW_0 as float; 
        """
        addr = 0x3F
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_Z_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_z_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_z_pow_0, 

    @hidden_c_gyro_2_bias_z_pow_0.setter
    def hidden_c_gyro_2_bias_z_pow_0(self, new_value):
        addr = 0x3F
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_z_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_Z_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_Z_POW_1 as float; 
        """
        addr = 0x40
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_Z_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_z_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_z_pow_1, 

    @hidden_c_gyro_2_bias_z_pow_1.setter
    def hidden_c_gyro_2_bias_z_pow_1(self, new_value):
        addr = 0x40
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_z_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_Z_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_Z_POW_2 as float; 
        """
        addr = 0x41
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_Z_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_z_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_z_pow_2, 

    @hidden_c_gyro_2_bias_z_pow_2.setter
    def hidden_c_gyro_2_bias_z_pow_2(self, new_value):
        addr = 0x41
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_bias_z_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_BIAS_Z_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_BIAS_Z_POW_3 as float; 
        """
        addr = 0x42
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_BIAS_Z_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_bias_z_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_bias_z_pow_3, 

    @hidden_c_gyro_2_bias_z_pow_3.setter
    def hidden_c_gyro_2_bias_z_pow_3(self, new_value):
        addr = 0x42
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_x_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_X_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_X_POW_0 as float; 
        """
        addr = 0x43
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_X_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_x_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_x_pow_0, 

    @hidden_c_gyro_2_scale_x_pow_0.setter
    def hidden_c_gyro_2_scale_x_pow_0(self, new_value):
        addr = 0x43
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_x_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_X_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_X_POW_1 as float; 
        """
        addr = 0x44
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_X_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_x_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_x_pow_1, 

    @hidden_c_gyro_2_scale_x_pow_1.setter
    def hidden_c_gyro_2_scale_x_pow_1(self, new_value):
        addr = 0x44
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_x_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_X_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_X_POW_2 as float; 
        """
        addr = 0x45
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_X_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_x_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_x_pow_2, 

    @hidden_c_gyro_2_scale_x_pow_2.setter
    def hidden_c_gyro_2_scale_x_pow_2(self, new_value):
        addr = 0x45
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_x_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_X_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_X_POW_3 as float; 
        """
        addr = 0x46
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_X_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_x_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_x_pow_3, 

    @hidden_c_gyro_2_scale_x_pow_3.setter
    def hidden_c_gyro_2_scale_x_pow_3(self, new_value):
        addr = 0x46
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_y_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_Y_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_Y_POW_0 as float; 
        """
        addr = 0x47
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_Y_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_y_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_y_pow_0, 

    @hidden_c_gyro_2_scale_y_pow_0.setter
    def hidden_c_gyro_2_scale_y_pow_0(self, new_value):
        addr = 0x47
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_y_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_Y_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_Y_POW_1 as float; 
        """
        addr = 0x48
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_Y_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_y_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_y_pow_1, 

    @hidden_c_gyro_2_scale_y_pow_1.setter
    def hidden_c_gyro_2_scale_y_pow_1(self, new_value):
        addr = 0x48
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_y_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_Y_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_Y_POW_2 as float; 
        """
        addr = 0x49
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_Y_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_y_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_y_pow_2, 

    @hidden_c_gyro_2_scale_y_pow_2.setter
    def hidden_c_gyro_2_scale_y_pow_2(self, new_value):
        addr = 0x49
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_y_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_Y_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_Y_POW_3 as float; 
        """
        addr = 0x4A
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_Y_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_y_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_y_pow_3, 

    @hidden_c_gyro_2_scale_y_pow_3.setter
    def hidden_c_gyro_2_scale_y_pow_3(self, new_value):
        addr = 0x4A
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_z_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_Z_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_Z_POW_0 as float; 
        """
        addr = 0x4B
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_Z_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_z_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_z_pow_0, 

    @hidden_c_gyro_2_scale_z_pow_0.setter
    def hidden_c_gyro_2_scale_z_pow_0(self, new_value):
        addr = 0x4B
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_z_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_Z_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_Z_POW_1 as float; 
        """
        addr = 0x4C
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_Z_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_z_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_z_pow_1, 

    @hidden_c_gyro_2_scale_z_pow_1.setter
    def hidden_c_gyro_2_scale_z_pow_1(self, new_value):
        addr = 0x4C
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_z_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_Z_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_Z_POW_2 as float; 
        """
        addr = 0x4D
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_Z_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_z_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_z_pow_2, 

    @hidden_c_gyro_2_scale_z_pow_2.setter
    def hidden_c_gyro_2_scale_z_pow_2(self, new_value):
        addr = 0x4D
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_gyro_2_scale_z_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_GYRO_2_SCALE_Z_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_GYRO_2_SCALE_Z_POW_3 as float; 
        """
        addr = 0x4E
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_GYRO_2_SCALE_Z_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_gyro_2_scale_z_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_gyro_2_scale_z_pow_3, 

    @hidden_c_gyro_2_scale_z_pow_3.setter
    def hidden_c_gyro_2_scale_z_pow_3(self, new_value):
        addr = 0x4E
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_2_alignment1_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_ALIGNMENT1_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_ALIGNMENT1_1 as float; 
        """
        addr = 0x4F
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_ALIGNMENT1_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_alignment1_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_alignment1_1, 

    @hidden_gyro_2_alignment1_1.setter
    def hidden_gyro_2_alignment1_1(self, new_value):
        addr = 0x4F
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_2_alignment1_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_ALIGNMENT1_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_ALIGNMENT1_2 as float; 
        """
        addr = 0x50
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_ALIGNMENT1_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_alignment1_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_alignment1_2, 

    @hidden_gyro_2_alignment1_2.setter
    def hidden_gyro_2_alignment1_2(self, new_value):
        addr = 0x50
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_2_alignment1_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_ALIGNMENT1_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_ALIGNMENT1_3 as float; 
        """
        addr = 0x51
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_ALIGNMENT1_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_alignment1_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_alignment1_3, 

    @hidden_gyro_2_alignment1_3.setter
    def hidden_gyro_2_alignment1_3(self, new_value):
        addr = 0x51
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_2_alignment2_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_ALIGNMENT2_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_ALIGNMENT2_1 as float; 
        """
        addr = 0x52
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_ALIGNMENT2_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_alignment2_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_alignment2_1, 

    @hidden_gyro_2_alignment2_1.setter
    def hidden_gyro_2_alignment2_1(self, new_value):
        addr = 0x52
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_2_alignment2_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_ALIGNMENT2_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_ALIGNMENT2_2 as float; 
        """
        addr = 0x53
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_ALIGNMENT2_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_alignment2_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_alignment2_2, 

    @hidden_gyro_2_alignment2_2.setter
    def hidden_gyro_2_alignment2_2(self, new_value):
        addr = 0x53
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_2_alignment2_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_ALIGNMENT2_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_ALIGNMENT2_3 as float; 
        """
        addr = 0x54
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_ALIGNMENT2_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_alignment2_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_alignment2_3, 

    @hidden_gyro_2_alignment2_3.setter
    def hidden_gyro_2_alignment2_3(self, new_value):
        addr = 0x54
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_2_alignment3_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_ALIGNMENT3_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_ALIGNMENT3_1 as float; 
        """
        addr = 0x55
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_ALIGNMENT3_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_alignment3_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_alignment3_1, 

    @hidden_gyro_2_alignment3_1.setter
    def hidden_gyro_2_alignment3_1(self, new_value):
        addr = 0x55
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_2_alignment3_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_ALIGNMENT3_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_ALIGNMENT3_2 as float; 
        """
        addr = 0x56
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_ALIGNMENT3_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_alignment3_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_alignment3_2, 

    @hidden_gyro_2_alignment3_2.setter
    def hidden_gyro_2_alignment3_2(self, new_value):
        addr = 0x56
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_2_alignment3_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_ALIGNMENT3_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_ALIGNMENT3_3 as float; 
        """
        addr = 0x57
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_ALIGNMENT3_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_alignment3_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_alignment3_3, 

    @hidden_gyro_2_alignment3_3.setter
    def hidden_gyro_2_alignment3_3(self, new_value):
        addr = 0x57
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_x_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_X_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_X_POW_0 as float; 
        """
        addr = 0x58
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_X_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_x_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_x_pow_0, 

    @hidden_c_accel_1_bias_x_pow_0.setter
    def hidden_c_accel_1_bias_x_pow_0(self, new_value):
        addr = 0x58
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_x_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_X_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_X_POW_1 as float; 
        """
        addr = 0x59
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_X_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_x_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_x_pow_1, 

    @hidden_c_accel_1_bias_x_pow_1.setter
    def hidden_c_accel_1_bias_x_pow_1(self, new_value):
        addr = 0x59
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_x_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_X_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_X_POW_2 as float; 
        """
        addr = 0x5A
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_X_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_x_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_x_pow_2, 

    @hidden_c_accel_1_bias_x_pow_2.setter
    def hidden_c_accel_1_bias_x_pow_2(self, new_value):
        addr = 0x5A
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_x_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_X_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_X_POW_3 as float; 
        """
        addr = 0x5B
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_X_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_x_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_x_pow_3, 

    @hidden_c_accel_1_bias_x_pow_3.setter
    def hidden_c_accel_1_bias_x_pow_3(self, new_value):
        addr = 0x5B
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_y_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_Y_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_Y_POW_0 as float; 
        """
        addr = 0x5C
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_Y_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_y_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_y_pow_0, 

    @hidden_c_accel_1_bias_y_pow_0.setter
    def hidden_c_accel_1_bias_y_pow_0(self, new_value):
        addr = 0x5C
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_y_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_Y_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_Y_POW_1 as float; 
        """
        addr = 0x5D
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_Y_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_y_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_y_pow_1, 

    @hidden_c_accel_1_bias_y_pow_1.setter
    def hidden_c_accel_1_bias_y_pow_1(self, new_value):
        addr = 0x5D
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_y_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_Y_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_Y_POW_2 as float; 
        """
        addr = 0x5E
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_Y_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_y_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_y_pow_2, 

    @hidden_c_accel_1_bias_y_pow_2.setter
    def hidden_c_accel_1_bias_y_pow_2(self, new_value):
        addr = 0x5E
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_y_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_Y_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_Y_POW_3 as float; 
        """
        addr = 0x5F
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_Y_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_y_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_y_pow_3, 

    @hidden_c_accel_1_bias_y_pow_3.setter
    def hidden_c_accel_1_bias_y_pow_3(self, new_value):
        addr = 0x5F
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_z_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_Z_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_Z_POW_0 as float; 
        """
        addr = 0x60
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_Z_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_z_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_z_pow_0, 

    @hidden_c_accel_1_bias_z_pow_0.setter
    def hidden_c_accel_1_bias_z_pow_0(self, new_value):
        addr = 0x60
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_z_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_Z_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_Z_POW_1 as float; 
        """
        addr = 0x61
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_Z_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_z_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_z_pow_1, 

    @hidden_c_accel_1_bias_z_pow_1.setter
    def hidden_c_accel_1_bias_z_pow_1(self, new_value):
        addr = 0x61
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_z_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_Z_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_Z_POW_2 as float; 
        """
        addr = 0x62
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_Z_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_z_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_z_pow_2, 

    @hidden_c_accel_1_bias_z_pow_2.setter
    def hidden_c_accel_1_bias_z_pow_2(self, new_value):
        addr = 0x62
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_bias_z_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_BIAS_Z_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_BIAS_Z_POW_3 as float; 
        """
        addr = 0x63
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_BIAS_Z_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_bias_z_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_bias_z_pow_3, 

    @hidden_c_accel_1_bias_z_pow_3.setter
    def hidden_c_accel_1_bias_z_pow_3(self, new_value):
        addr = 0x63
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_x_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_X_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_X_POW_0 as float; 
        """
        addr = 0x64
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_X_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_x_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_x_pow_0, 

    @hidden_c_accel_1_scale_x_pow_0.setter
    def hidden_c_accel_1_scale_x_pow_0(self, new_value):
        addr = 0x64
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_x_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_X_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_X_POW_1 as float; 
        """
        addr = 0x65
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_X_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_x_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_x_pow_1, 

    @hidden_c_accel_1_scale_x_pow_1.setter
    def hidden_c_accel_1_scale_x_pow_1(self, new_value):
        addr = 0x65
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_x_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_X_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_X_POW_2 as float; 
        """
        addr = 0x66
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_X_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_x_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_x_pow_2, 

    @hidden_c_accel_1_scale_x_pow_2.setter
    def hidden_c_accel_1_scale_x_pow_2(self, new_value):
        addr = 0x66
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_x_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_X_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_X_POW_3 as float; 
        """
        addr = 0x67
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_X_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_x_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_x_pow_3, 

    @hidden_c_accel_1_scale_x_pow_3.setter
    def hidden_c_accel_1_scale_x_pow_3(self, new_value):
        addr = 0x67
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_y_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_Y_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_Y_POW_0 as float; 
        """
        addr = 0x68
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_Y_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_y_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_y_pow_0, 

    @hidden_c_accel_1_scale_y_pow_0.setter
    def hidden_c_accel_1_scale_y_pow_0(self, new_value):
        addr = 0x68
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_y_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_Y_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_Y_POW_1 as float; 
        """
        addr = 0x69
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_Y_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_y_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_y_pow_1, 

    @hidden_c_accel_1_scale_y_pow_1.setter
    def hidden_c_accel_1_scale_y_pow_1(self, new_value):
        addr = 0x69
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_y_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_Y_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_Y_POW_2 as float; 
        """
        addr = 0x6A
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_Y_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_y_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_y_pow_2, 

    @hidden_c_accel_1_scale_y_pow_2.setter
    def hidden_c_accel_1_scale_y_pow_2(self, new_value):
        addr = 0x6A
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_y_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_Y_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_Y_POW_3 as float; 
        """
        addr = 0x6B
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_Y_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_y_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_y_pow_3, 

    @hidden_c_accel_1_scale_y_pow_3.setter
    def hidden_c_accel_1_scale_y_pow_3(self, new_value):
        addr = 0x6B
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_z_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_Z_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_Z_POW_0 as float; 
        """
        addr = 0x6C
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_Z_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_z_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_z_pow_0, 

    @hidden_c_accel_1_scale_z_pow_0.setter
    def hidden_c_accel_1_scale_z_pow_0(self, new_value):
        addr = 0x6C
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_z_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_Z_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_Z_POW_1 as float; 
        """
        addr = 0x6D
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_Z_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_z_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_z_pow_1, 

    @hidden_c_accel_1_scale_z_pow_1.setter
    def hidden_c_accel_1_scale_z_pow_1(self, new_value):
        addr = 0x6D
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_z_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_Z_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_Z_POW_2 as float; 
        """
        addr = 0x6E
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_Z_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_z_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_z_pow_2, 

    @hidden_c_accel_1_scale_z_pow_2.setter
    def hidden_c_accel_1_scale_z_pow_2(self, new_value):
        addr = 0x6E
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_accel_1_scale_z_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_ACCEL_1_SCALE_Z_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_ACCEL_1_SCALE_Z_POW_3 as float; 
        """
        addr = 0x6F
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_ACCEL_1_SCALE_Z_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_accel_1_scale_z_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_accel_1_scale_z_pow_3, 

    @hidden_c_accel_1_scale_z_pow_3.setter
    def hidden_c_accel_1_scale_z_pow_3(self, new_value):
        addr = 0x6F
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_accel_1_alignment1_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_ALIGNMENT1_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_ALIGNMENT1_1 as float; 
        """
        addr = 0x70
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_ALIGNMENT1_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_alignment1_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_alignment1_1, 

    @hidden_accel_1_alignment1_1.setter
    def hidden_accel_1_alignment1_1(self, new_value):
        addr = 0x70
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_accel_1_alignment1_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_ALIGNMENT1_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_ALIGNMENT1_2 as float; 
        """
        addr = 0x71
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_ALIGNMENT1_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_alignment1_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_alignment1_2, 

    @hidden_accel_1_alignment1_2.setter
    def hidden_accel_1_alignment1_2(self, new_value):
        addr = 0x71
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_accel_1_alignment1_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_ALIGNMENT1_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_ALIGNMENT1_3 as float; 
        """
        addr = 0x72
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_ALIGNMENT1_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_alignment1_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_alignment1_3, 

    @hidden_accel_1_alignment1_3.setter
    def hidden_accel_1_alignment1_3(self, new_value):
        addr = 0x72
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_accel_1_alignment2_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_ALIGNMENT2_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_ALIGNMENT2_1 as float; 
        """
        addr = 0x73
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_ALIGNMENT2_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_alignment2_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_alignment2_1, 

    @hidden_accel_1_alignment2_1.setter
    def hidden_accel_1_alignment2_1(self, new_value):
        addr = 0x73
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_accel_1_alignment2_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_ALIGNMENT2_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_ALIGNMENT2_2 as float; 
        """
        addr = 0x74
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_ALIGNMENT2_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_alignment2_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_alignment2_2, 

    @hidden_accel_1_alignment2_2.setter
    def hidden_accel_1_alignment2_2(self, new_value):
        addr = 0x74
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_accel_1_alignment2_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_ALIGNMENT2_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_ALIGNMENT2_3 as float; 
        """
        addr = 0x75
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_ALIGNMENT2_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_alignment2_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_alignment2_3, 

    @hidden_accel_1_alignment2_3.setter
    def hidden_accel_1_alignment2_3(self, new_value):
        addr = 0x75
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_accel_1_alignment3_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_ALIGNMENT3_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_ALIGNMENT3_1 as float; 
        """
        addr = 0x76
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_ALIGNMENT3_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_alignment3_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_alignment3_1, 

    @hidden_accel_1_alignment3_1.setter
    def hidden_accel_1_alignment3_1(self, new_value):
        addr = 0x76
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_accel_1_alignment3_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_ALIGNMENT3_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_ALIGNMENT3_2 as float; 
        """
        addr = 0x77
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_ALIGNMENT3_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_alignment3_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_alignment3_2, 

    @hidden_accel_1_alignment3_2.setter
    def hidden_accel_1_alignment3_2(self, new_value):
        addr = 0x77
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_accel_1_alignment3_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_ALIGNMENT3_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_ALIGNMENT3_3 as float; 
        """
        addr = 0x78
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_ALIGNMENT3_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_alignment3_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_alignment3_3, 

    @hidden_accel_1_alignment3_3.setter
    def hidden_accel_1_alignment3_3(self, new_value):
        addr = 0x78
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_x_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_X_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_X_POW_0 as float; 
        """
        addr = 0x79
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_X_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_x_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_x_pow_0, 

    @hidden_c_mag_1_bias_x_pow_0.setter
    def hidden_c_mag_1_bias_x_pow_0(self, new_value):
        addr = 0x79
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_x_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_X_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_X_POW_1 as float; 
        """
        addr = 0x7A
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_X_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_x_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_x_pow_1, 

    @hidden_c_mag_1_bias_x_pow_1.setter
    def hidden_c_mag_1_bias_x_pow_1(self, new_value):
        addr = 0x7A
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_x_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_X_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_X_POW_2 as float; 
        """
        addr = 0x7B
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_X_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_x_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_x_pow_2, 

    @hidden_c_mag_1_bias_x_pow_2.setter
    def hidden_c_mag_1_bias_x_pow_2(self, new_value):
        addr = 0x7B
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_x_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_X_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_X_POW_3 as float; 
        """
        addr = 0x7C
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_X_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_x_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_x_pow_3, 

    @hidden_c_mag_1_bias_x_pow_3.setter
    def hidden_c_mag_1_bias_x_pow_3(self, new_value):
        addr = 0x7C
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_y_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_Y_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_Y_POW_0 as float; 
        """
        addr = 0x7D
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_Y_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_y_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_y_pow_0, 

    @hidden_c_mag_1_bias_y_pow_0.setter
    def hidden_c_mag_1_bias_y_pow_0(self, new_value):
        addr = 0x7D
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_y_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_Y_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_Y_POW_1 as float; 
        """
        addr = 0x7E
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_Y_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_y_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_y_pow_1, 

    @hidden_c_mag_1_bias_y_pow_1.setter
    def hidden_c_mag_1_bias_y_pow_1(self, new_value):
        addr = 0x7E
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_y_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_Y_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_Y_POW_2 as float; 
        """
        addr = 0x7F
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_Y_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_y_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_y_pow_2, 

    @hidden_c_mag_1_bias_y_pow_2.setter
    def hidden_c_mag_1_bias_y_pow_2(self, new_value):
        addr = 0x7F
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_y_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_Y_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_Y_POW_3 as float; 
        """
        addr = 0x80
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_Y_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_y_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_y_pow_3, 

    @hidden_c_mag_1_bias_y_pow_3.setter
    def hidden_c_mag_1_bias_y_pow_3(self, new_value):
        addr = 0x80
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_z_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_Z_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_Z_POW_0 as float; 
        """
        addr = 0x81
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_Z_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_z_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_z_pow_0, 

    @hidden_c_mag_1_bias_z_pow_0.setter
    def hidden_c_mag_1_bias_z_pow_0(self, new_value):
        addr = 0x81
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_z_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_Z_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_Z_POW_1 as float; 
        """
        addr = 0x82
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_Z_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_z_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_z_pow_1, 

    @hidden_c_mag_1_bias_z_pow_1.setter
    def hidden_c_mag_1_bias_z_pow_1(self, new_value):
        addr = 0x82
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_z_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_Z_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_Z_POW_2 as float; 
        """
        addr = 0x83
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_Z_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_z_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_z_pow_2, 

    @hidden_c_mag_1_bias_z_pow_2.setter
    def hidden_c_mag_1_bias_z_pow_2(self, new_value):
        addr = 0x83
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_bias_z_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_BIAS_Z_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_BIAS_Z_POW_3 as float; 
        """
        addr = 0x84
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_BIAS_Z_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_bias_z_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_bias_z_pow_3, 

    @hidden_c_mag_1_bias_z_pow_3.setter
    def hidden_c_mag_1_bias_z_pow_3(self, new_value):
        addr = 0x84
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_x_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_X_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_X_POW_0 as float; 
        """
        addr = 0x85
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_X_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_x_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_x_pow_0, 

    @hidden_c_mag_1_scale_x_pow_0.setter
    def hidden_c_mag_1_scale_x_pow_0(self, new_value):
        addr = 0x85
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_x_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_X_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_X_POW_1 as float; 
        """
        addr = 0x86
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_X_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_x_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_x_pow_1, 

    @hidden_c_mag_1_scale_x_pow_1.setter
    def hidden_c_mag_1_scale_x_pow_1(self, new_value):
        addr = 0x86
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_x_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_X_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_X_POW_2 as float; 
        """
        addr = 0x87
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_X_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_x_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_x_pow_2, 

    @hidden_c_mag_1_scale_x_pow_2.setter
    def hidden_c_mag_1_scale_x_pow_2(self, new_value):
        addr = 0x87
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_x_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_X_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_X_POW_3 as float; 
        """
        addr = 0x88
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_X_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_x_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_x_pow_3, 

    @hidden_c_mag_1_scale_x_pow_3.setter
    def hidden_c_mag_1_scale_x_pow_3(self, new_value):
        addr = 0x88
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_y_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_Y_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_Y_POW_0 as float; 
        """
        addr = 0x89
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_Y_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_y_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_y_pow_0, 

    @hidden_c_mag_1_scale_y_pow_0.setter
    def hidden_c_mag_1_scale_y_pow_0(self, new_value):
        addr = 0x89
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_y_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_Y_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_Y_POW_1 as float; 
        """
        addr = 0x8A
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_Y_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_y_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_y_pow_1, 

    @hidden_c_mag_1_scale_y_pow_1.setter
    def hidden_c_mag_1_scale_y_pow_1(self, new_value):
        addr = 0x8A
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_y_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_Y_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_Y_POW_2 as float; 
        """
        addr = 0x8B
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_Y_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_y_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_y_pow_2, 

    @hidden_c_mag_1_scale_y_pow_2.setter
    def hidden_c_mag_1_scale_y_pow_2(self, new_value):
        addr = 0x8B
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_y_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_Y_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_Y_POW_3 as float; 
        """
        addr = 0x8C
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_Y_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_y_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_y_pow_3, 

    @hidden_c_mag_1_scale_y_pow_3.setter
    def hidden_c_mag_1_scale_y_pow_3(self, new_value):
        addr = 0x8C
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_z_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_Z_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_Z_POW_0 as float; 
        """
        addr = 0x8D
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_Z_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_z_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_z_pow_0, 

    @hidden_c_mag_1_scale_z_pow_0.setter
    def hidden_c_mag_1_scale_z_pow_0(self, new_value):
        addr = 0x8D
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_z_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_Z_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_Z_POW_1 as float; 
        """
        addr = 0x8E
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_Z_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_z_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_z_pow_1, 

    @hidden_c_mag_1_scale_z_pow_1.setter
    def hidden_c_mag_1_scale_z_pow_1(self, new_value):
        addr = 0x8E
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_z_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_Z_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_Z_POW_2 as float; 
        """
        addr = 0x8F
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_Z_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_z_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_z_pow_2, 

    @hidden_c_mag_1_scale_z_pow_2.setter
    def hidden_c_mag_1_scale_z_pow_2(self, new_value):
        addr = 0x8F
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_1_scale_z_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_1_SCALE_Z_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_1_SCALE_Z_POW_3 as float; 
        """
        addr = 0x90
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_1_SCALE_Z_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_1_scale_z_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_1_scale_z_pow_3, 

    @hidden_c_mag_1_scale_z_pow_3.setter
    def hidden_c_mag_1_scale_z_pow_3(self, new_value):
        addr = 0x90
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_alignment1_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_ALIGNMENT1_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_ALIGNMENT1_1 as float; 
        """
        addr = 0x91
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_ALIGNMENT1_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_alignment1_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_alignment1_1, 

    @hidden_mag_1_alignment1_1.setter
    def hidden_mag_1_alignment1_1(self, new_value):
        addr = 0x91
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_alignment1_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_ALIGNMENT1_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_ALIGNMENT1_2 as float; 
        """
        addr = 0x92
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_ALIGNMENT1_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_alignment1_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_alignment1_2, 

    @hidden_mag_1_alignment1_2.setter
    def hidden_mag_1_alignment1_2(self, new_value):
        addr = 0x92
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_alignment1_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_ALIGNMENT1_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_ALIGNMENT1_3 as float; 
        """
        addr = 0x93
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_ALIGNMENT1_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_alignment1_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_alignment1_3, 

    @hidden_mag_1_alignment1_3.setter
    def hidden_mag_1_alignment1_3(self, new_value):
        addr = 0x93
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_alignment2_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_ALIGNMENT2_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_ALIGNMENT2_1 as float; 
        """
        addr = 0x94
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_ALIGNMENT2_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_alignment2_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_alignment2_1, 

    @hidden_mag_1_alignment2_1.setter
    def hidden_mag_1_alignment2_1(self, new_value):
        addr = 0x94
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_alignment2_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_ALIGNMENT2_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_ALIGNMENT2_2 as float; 
        """
        addr = 0x95
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_ALIGNMENT2_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_alignment2_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_alignment2_2, 

    @hidden_mag_1_alignment2_2.setter
    def hidden_mag_1_alignment2_2(self, new_value):
        addr = 0x95
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_alignment2_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_ALIGNMENT2_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_ALIGNMENT2_3 as float; 
        """
        addr = 0x96
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_ALIGNMENT2_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_alignment2_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_alignment2_3, 

    @hidden_mag_1_alignment2_3.setter
    def hidden_mag_1_alignment2_3(self, new_value):
        addr = 0x96
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_alignment3_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_ALIGNMENT3_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_ALIGNMENT3_1 as float; 
        """
        addr = 0x97
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_ALIGNMENT3_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_alignment3_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_alignment3_1, 

    @hidden_mag_1_alignment3_1.setter
    def hidden_mag_1_alignment3_1(self, new_value):
        addr = 0x97
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_alignment3_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_ALIGNMENT3_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_ALIGNMENT3_2 as float; 
        """
        addr = 0x98
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_ALIGNMENT3_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_alignment3_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_alignment3_2, 

    @hidden_mag_1_alignment3_2.setter
    def hidden_mag_1_alignment3_2(self, new_value):
        addr = 0x98
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_alignment3_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_ALIGNMENT3_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_ALIGNMENT3_3 as float; 
        """
        addr = 0x99
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_ALIGNMENT3_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_alignment3_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_alignment3_3, 

    @hidden_mag_1_alignment3_3.setter
    def hidden_mag_1_alignment3_3(self, new_value):
        addr = 0x99
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_reference_x(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_REFERENCE_X -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_REFERENCE_X as float; 
        """
        addr = 0x9A
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_REFERENCE_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_reference_x,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_reference_x, 

    @hidden_mag_1_reference_x.setter
    def hidden_mag_1_reference_x(self, new_value):
        addr = 0x9A
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_reference_y(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_REFERENCE_Y -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_REFERENCE_Y as float; 
        """
        addr = 0x9B
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_REFERENCE_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_reference_y,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_reference_y, 

    @hidden_mag_1_reference_y.setter
    def hidden_mag_1_reference_y(self, new_value):
        addr = 0x9B
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_1_reference_z(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_REFERENCE_Z -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_REFERENCE_Z as float; 
        """
        addr = 0x9C
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_REFERENCE_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_reference_z,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_reference_z, 

    @hidden_mag_1_reference_z.setter
    def hidden_mag_1_reference_z(self, new_value):
        addr = 0x9C
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_x_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_X_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_X_POW_0 as float; 
        """
        addr = 0x9D
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_X_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_x_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_x_pow_0, 

    @hidden_c_mag_2_bias_x_pow_0.setter
    def hidden_c_mag_2_bias_x_pow_0(self, new_value):
        addr = 0x9D
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_x_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_X_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_X_POW_1 as float; 
        """
        addr = 0x9E
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_X_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_x_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_x_pow_1, 

    @hidden_c_mag_2_bias_x_pow_1.setter
    def hidden_c_mag_2_bias_x_pow_1(self, new_value):
        addr = 0x9E
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_x_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_X_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_X_POW_2 as float; 
        """
        addr = 0x9F
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_X_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_x_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_x_pow_2, 

    @hidden_c_mag_2_bias_x_pow_2.setter
    def hidden_c_mag_2_bias_x_pow_2(self, new_value):
        addr = 0x9F
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_x_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_X_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_X_POW_3 as float; 
        """
        addr = 0xA0
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_X_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_x_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_x_pow_3, 

    @hidden_c_mag_2_bias_x_pow_3.setter
    def hidden_c_mag_2_bias_x_pow_3(self, new_value):
        addr = 0xA0
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_y_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_Y_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_Y_POW_0 as float; 
        """
        addr = 0xA1
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_Y_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_y_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_y_pow_0, 

    @hidden_c_mag_2_bias_y_pow_0.setter
    def hidden_c_mag_2_bias_y_pow_0(self, new_value):
        addr = 0xA1
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_y_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_Y_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_Y_POW_1 as float; 
        """
        addr = 0xA2
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_Y_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_y_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_y_pow_1, 

    @hidden_c_mag_2_bias_y_pow_1.setter
    def hidden_c_mag_2_bias_y_pow_1(self, new_value):
        addr = 0xA2
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_y_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_Y_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_Y_POW_2 as float; 
        """
        addr = 0xA3
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_Y_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_y_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_y_pow_2, 

    @hidden_c_mag_2_bias_y_pow_2.setter
    def hidden_c_mag_2_bias_y_pow_2(self, new_value):
        addr = 0xA3
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_y_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_Y_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_Y_POW_3 as float; 
        """
        addr = 0xA4
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_Y_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_y_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_y_pow_3, 

    @hidden_c_mag_2_bias_y_pow_3.setter
    def hidden_c_mag_2_bias_y_pow_3(self, new_value):
        addr = 0xA4
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_z_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_Z_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_Z_POW_0 as float; 
        """
        addr = 0xA5
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_Z_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_z_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_z_pow_0, 

    @hidden_c_mag_2_bias_z_pow_0.setter
    def hidden_c_mag_2_bias_z_pow_0(self, new_value):
        addr = 0xA5
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_z_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_Z_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_Z_POW_1 as float; 
        """
        addr = 0xA6
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_Z_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_z_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_z_pow_1, 

    @hidden_c_mag_2_bias_z_pow_1.setter
    def hidden_c_mag_2_bias_z_pow_1(self, new_value):
        addr = 0xA6
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_z_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_Z_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_Z_POW_2 as float; 
        """
        addr = 0xA7
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_Z_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_z_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_z_pow_2, 

    @hidden_c_mag_2_bias_z_pow_2.setter
    def hidden_c_mag_2_bias_z_pow_2(self, new_value):
        addr = 0xA7
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_bias_z_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_BIAS_Z_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_BIAS_Z_POW_3 as float; 
        """
        addr = 0xA8
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_BIAS_Z_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_bias_z_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_bias_z_pow_3, 

    @hidden_c_mag_2_bias_z_pow_3.setter
    def hidden_c_mag_2_bias_z_pow_3(self, new_value):
        addr = 0xA8
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_x_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_X_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_X_POW_0 as float; 
        """
        addr = 0xA9
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_X_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_x_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_x_pow_0, 

    @hidden_c_mag_2_scale_x_pow_0.setter
    def hidden_c_mag_2_scale_x_pow_0(self, new_value):
        addr = 0xA9
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_x_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_X_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_X_POW_1 as float; 
        """
        addr = 0xAA
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_X_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_x_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_x_pow_1, 

    @hidden_c_mag_2_scale_x_pow_1.setter
    def hidden_c_mag_2_scale_x_pow_1(self, new_value):
        addr = 0xAA
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_x_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_X_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_X_POW_2 as float; 
        """
        addr = 0xAB
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_X_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_x_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_x_pow_2, 

    @hidden_c_mag_2_scale_x_pow_2.setter
    def hidden_c_mag_2_scale_x_pow_2(self, new_value):
        addr = 0xAB
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_x_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_X_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_X_POW_3 as float; 
        """
        addr = 0xAC
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_X_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_x_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_x_pow_3, 

    @hidden_c_mag_2_scale_x_pow_3.setter
    def hidden_c_mag_2_scale_x_pow_3(self, new_value):
        addr = 0xAC
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_y_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_Y_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_Y_POW_0 as float; 
        """
        addr = 0xAD
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_Y_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_y_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_y_pow_0, 

    @hidden_c_mag_2_scale_y_pow_0.setter
    def hidden_c_mag_2_scale_y_pow_0(self, new_value):
        addr = 0xAD
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_y_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_Y_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_Y_POW_1 as float; 
        """
        addr = 0xAE
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_Y_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_y_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_y_pow_1, 

    @hidden_c_mag_2_scale_y_pow_1.setter
    def hidden_c_mag_2_scale_y_pow_1(self, new_value):
        addr = 0xAE
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_y_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_Y_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_Y_POW_2 as float; 
        """
        addr = 0xAF
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_Y_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_y_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_y_pow_2, 

    @hidden_c_mag_2_scale_y_pow_2.setter
    def hidden_c_mag_2_scale_y_pow_2(self, new_value):
        addr = 0xAF
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_y_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_Y_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_Y_POW_3 as float; 
        """
        addr = 0xB0
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_Y_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_y_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_y_pow_3, 

    @hidden_c_mag_2_scale_y_pow_3.setter
    def hidden_c_mag_2_scale_y_pow_3(self, new_value):
        addr = 0xB0
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_z_pow_0(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_Z_POW_0 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_Z_POW_0 as float; 
        """
        addr = 0xB1
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_Z_POW_0')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_z_pow_0,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_z_pow_0, 

    @hidden_c_mag_2_scale_z_pow_0.setter
    def hidden_c_mag_2_scale_z_pow_0(self, new_value):
        addr = 0xB1
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_z_pow_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_Z_POW_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_Z_POW_1 as float; 
        """
        addr = 0xB2
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_Z_POW_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_z_pow_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_z_pow_1, 

    @hidden_c_mag_2_scale_z_pow_1.setter
    def hidden_c_mag_2_scale_z_pow_1(self, new_value):
        addr = 0xB2
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_z_pow_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_Z_POW_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_Z_POW_2 as float; 
        """
        addr = 0xB3
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_Z_POW_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_z_pow_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_z_pow_2, 

    @hidden_c_mag_2_scale_z_pow_2.setter
    def hidden_c_mag_2_scale_z_pow_2(self, new_value):
        addr = 0xB3
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_c_mag_2_scale_z_pow_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_C_MAG_2_SCALE_Z_POW_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_C_MAG_2_SCALE_Z_POW_3 as float; 
        """
        addr = 0xB4
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_C_MAG_2_SCALE_Z_POW_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_c_mag_2_scale_z_pow_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_c_mag_2_scale_z_pow_3, 

    @hidden_c_mag_2_scale_z_pow_3.setter
    def hidden_c_mag_2_scale_z_pow_3(self, new_value):
        addr = 0xB4
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_alignment1_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_ALIGNMENT1_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_ALIGNMENT1_1 as float; 
        """
        addr = 0xB5
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_ALIGNMENT1_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_alignment1_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_alignment1_1, 

    @hidden_mag_2_alignment1_1.setter
    def hidden_mag_2_alignment1_1(self, new_value):
        addr = 0xB5
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_alignment1_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_ALIGNMENT1_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_ALIGNMENT1_2 as float; 
        """
        addr = 0xB6
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_ALIGNMENT1_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_alignment1_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_alignment1_2, 

    @hidden_mag_2_alignment1_2.setter
    def hidden_mag_2_alignment1_2(self, new_value):
        addr = 0xB6
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_alignment1_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_ALIGNMENT1_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_ALIGNMENT1_3 as float; 
        """
        addr = 0xB7
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_ALIGNMENT1_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_alignment1_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_alignment1_3, 

    @hidden_mag_2_alignment1_3.setter
    def hidden_mag_2_alignment1_3(self, new_value):
        addr = 0xB7
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_alignment2_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_ALIGNMENT2_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_ALIGNMENT2_1 as float; 
        """
        addr = 0xB8
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_ALIGNMENT2_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_alignment2_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_alignment2_1, 

    @hidden_mag_2_alignment2_1.setter
    def hidden_mag_2_alignment2_1(self, new_value):
        addr = 0xB8
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_alignment2_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_ALIGNMENT2_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_ALIGNMENT2_2 as float; 
        """
        addr = 0xB9
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_ALIGNMENT2_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_alignment2_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_alignment2_2, 

    @hidden_mag_2_alignment2_2.setter
    def hidden_mag_2_alignment2_2(self, new_value):
        addr = 0xB9
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_alignment2_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_ALIGNMENT2_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_ALIGNMENT2_3 as float; 
        """
        addr = 0xBA
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_ALIGNMENT2_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_alignment2_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_alignment2_3, 

    @hidden_mag_2_alignment2_3.setter
    def hidden_mag_2_alignment2_3(self, new_value):
        addr = 0xBA
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_alignment3_1(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_ALIGNMENT3_1 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_ALIGNMENT3_1 as float; 
        """
        addr = 0xBB
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_ALIGNMENT3_1')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_alignment3_1,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_alignment3_1, 

    @hidden_mag_2_alignment3_1.setter
    def hidden_mag_2_alignment3_1(self, new_value):
        addr = 0xBB
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_alignment3_2(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_ALIGNMENT3_2 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_ALIGNMENT3_2 as float; 
        """
        addr = 0xBC
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_ALIGNMENT3_2')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_alignment3_2,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_alignment3_2, 

    @hidden_mag_2_alignment3_2.setter
    def hidden_mag_2_alignment3_2(self, new_value):
        addr = 0xBC
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_alignment3_3(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_ALIGNMENT3_3 -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_ALIGNMENT3_3 as float; 
        """
        addr = 0xBD
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_ALIGNMENT3_3')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_alignment3_3,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_alignment3_3, 

    @hidden_mag_2_alignment3_3.setter
    def hidden_mag_2_alignment3_3(self, new_value):
        addr = 0xBD
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_reference_x(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_REFERENCE_X -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_REFERENCE_X as float; 
        """
        addr = 0xBE
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_REFERENCE_X')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_reference_x,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_reference_x, 

    @hidden_mag_2_reference_x.setter
    def hidden_mag_2_reference_x(self, new_value):
        addr = 0xBE
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_reference_y(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_REFERENCE_Y -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_REFERENCE_Y as float; 
        """
        addr = 0xBF
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_REFERENCE_Y')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_reference_y,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_reference_y, 

    @hidden_mag_2_reference_y.setter
    def hidden_mag_2_reference_y(self, new_value):
        addr = 0xBF
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_mag_2_reference_z(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_REFERENCE_Z -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_REFERENCE_Z as float; 
        """
        addr = 0xC0
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_REFERENCE_Z')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_reference_z,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_reference_z, 

    @hidden_mag_2_reference_z.setter
    def hidden_mag_2_reference_z(self, new_value):
        addr = 0xC0
        self.write_register(addr, new_value, hidden=True)

    @property
    def hidden_gyro_1_conversion(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_1_CONVERSION -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_1_CONVERSION as float; 
        """
        addr = 0xC1
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_1_CONVERSION')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_1_conversion,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_1_conversion, 

    @property
    def hidden_gyro_2_conversion(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_GYRO_2_CONVERSION -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_GYRO_2_CONVERSION as float; 
        """
        addr = 0xC2
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_GYRO_2_CONVERSION')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_gyro_2_conversion,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_gyro_2_conversion, 

    @property
    def hidden_accel_1_conversion(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_ACCEL_1_CONVERSION -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_ACCEL_1_CONVERSION as float; 
        """
        addr = 0xC3
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_ACCEL_1_CONVERSION')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_accel_1_conversion,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_accel_1_conversion, 

    @property
    def hidden_mag_1_conversion(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_1_CONVERSION -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_1_CONVERSION as float; 
        """
        addr = 0xC4
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_1_CONVERSION')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_1_conversion,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_1_conversion, 

    @property
    def hidden_mag_2_conversion(self):
        """
        TODO: add description
        Payload structure:
        [31:0]  : HIDDEN_MAG_2_CONVERSION -- 32-bit IEEE 754 Floating Point Value
        :return:  HIDDEN_MAG_2_CONVERSION as float; 
        """
        addr = 0xC5
        ok, payload = self.read_register(addr, hidden=True)
        if ok:
            reg = self.svd_parser.find_hidden_register_by(name='HIDDEN_MAG_2_CONVERSION')
            reg.raw_value, = struct.unpack('>f', payload[0:4])
            hidden_mag_2_conversion,  = struct.unpack('>f', payload[0:4])
            return reg, hidden_mag_2_conversion, 


if __name__ == '__main__':
    pass
