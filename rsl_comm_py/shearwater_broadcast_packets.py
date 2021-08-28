#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# License: MIT
# Date: 3 May 2020
# Modified: 26 September 2020


from dataclasses import dataclass


@dataclass
class ShearWaterAllRawPacket:
    gyro_1_raw_x: int
    gyro_1_raw_y: int
    gyro_1_raw_z: int
    gyro_1_raw_time: float
    gyro_2_raw_x: int
    gyro_2_raw_y: int
    gyro_2_raw_z: int
    gyro_2_raw_time: float
    accel_1_raw_x: int
    accel_1_raw_y: int
    accel_1_raw_z: int
    accel_1_raw_time: float
    mag_1_raw_x: int
    mag_1_raw_y: int
    mag_1_raw_z: int
    mag_1_raw_time: float
    mag_2_raw_x: int
    mag_2_raw_y: int
    mag_2_raw_z: int
    mag_2_raw_time: float
    temperature: float
    temperature_time: float

    def __repr__(self):
        return f"RawPacket("\
               f"gyro_1=[{self.gyro_1_raw_x:>+5d}, {self.gyro_1_raw_y:>+5d}, {self.gyro_1_raw_z:>+5d}], "\
               f"gyro_1_t={self.gyro_1_raw_time:>6.3f}; " \
               f"gyro_2=[{self.gyro_2_raw_x:>+5d}, {self.gyro_2_raw_y:>+5d}, {self.gyro_2_raw_z:>+5d}], " \
               f"gyro_2_t={self.gyro_2_raw_time:>6.3f}; " \
               f"accel_1=[{self.accel_1_raw_x:>+5d}, {self.accel_1_raw_y:>+5d}, {self.accel_1_raw_z:>+5d}], " \
               f"accel_1_t={self.accel_1_raw_time:>6.3f}; " \
               f"mag_1=[{self.mag_1_raw_x:>+8d}, {self.mag_1_raw_y:>+8d}, {self.mag_1_raw_z:>+8d}], " \
               f"mag_1_t={self.mag_1_raw_time:>6.3f}; " \
               f"mag_2=[{self.mag_2_raw_x:>+5d}, {self.mag_2_raw_y:>+5d}, {self.mag_2_raw_z:>+5d}], " \
               f"mag_2_t={self.mag_2_raw_time:>6.3f}; " \
               f"T={self.temperature:>+3.2f}, " \
               f"T_t={self.temperature_time:>6.3f})"

    def to_csv(self):
        return f"{self.gyro_1_raw_x:>+5d};{self.gyro_1_raw_y:>+5d};{self.gyro_1_raw_z:>+5d};" \
               f"{self.gyro_1_raw_time:>6.5f};" \
               f"{self.gyro_2_raw_x:>+5d};{self.gyro_2_raw_y:>+5d};{self.gyro_2_raw_z:>+5d};" \
               f"{self.gyro_2_raw_time:>6.5f};" \
               f"{self.accel_1_raw_x:>+5d};{self.accel_1_raw_y:>+5d};{self.accel_1_raw_z:>+5d};" \
               f"{self.accel_1_raw_time:>6.5f};" \
               f"{self.mag_1_raw_x:>+8d};{self.mag_1_raw_y:>+8d};{self.mag_1_raw_z:>+8d};" \
               f"{self.mag_1_raw_time:>6.5f};" \
               f"{self.mag_2_raw_x:>+5d};{self.mag_2_raw_y:>+5d};{self.mag_2_raw_z:>+5d};" \
               f"{self.mag_2_raw_time:>6.5f};" \
               f"{self.temperature:>+3.2f};" \
               f"{self.temperature_time:>6.5f};\n"

    @staticmethod
    def csv_header():
        return "gyro_1_raw_x;gyro_1_raw_y;gyro_1_raw_z;gyro_1_raw_time;" \
               "gyro_2_raw_x;gyro_2_raw_y;gyro_2_raw_z;gyro_2_raw_time;" \
               "accel_1_raw_x;accel_1_raw_y;accel_1_raw_z;accel_1_raw_time;" \
               "mag_1_raw_x;mag_1_raw_y;mag_1_raw_z;mag_1_raw_time;" \
               "mag_2_raw_x;mag_2_raw_y;mag_2_raw_z;mag_2_raw_time;" \
               "temperature;temperature_time;\n"


@dataclass
class ShearWaterAllProcPacket:
    gyro_1_proc_x: float
    gyro_1_proc_y: float
    gyro_1_proc_z: float
    gyro_1_proc_time: float
    gyro_2_proc_x: float
    gyro_2_proc_y: float
    gyro_2_proc_z: float
    gyro_2_proc_time: float
    accel_1_proc_x: float
    accel_1_proc_y: float
    accel_1_proc_z: float
    accel_1_proc_time: float
    mag_1_proc_x: float
    mag_1_proc_y: float
    mag_1_proc_z: float
    mag_1_norm: float
    mag_1_proc_time: float
    mag_2_proc_x: float
    mag_2_proc_y: float
    mag_2_proc_z: float
    mag_2_norm: float
    mag_2_proc_time: float

    def __repr__(self):
        return f"ProcPacket("\
               f"gyro_1=[{self.gyro_1_proc_x:>+8.3f}, {self.gyro_1_proc_y:>+8.3f}, {self.gyro_1_proc_z:>+8.3f}], "\
               f"gyro_1_t={self.gyro_1_proc_time:>6.3f}; " \
               f"gyro_2=[{self.gyro_2_proc_x:>+8.3f}, {self.gyro_2_proc_y:>+8.3f}, {self.gyro_2_proc_z:>+8.3f}], " \
               f"gyro_2_t={self.gyro_2_proc_time:>6.3f}; " \
               f"accel_1=[{self.accel_1_proc_x:>+8.3f}, {self.accel_1_proc_y:>+8.3f}, {self.accel_1_proc_z:>+8.3f}], " \
               f"accel_1_t={self.accel_1_proc_time:>6.3f}; " \
               f"mag_1=[{self.mag_1_proc_x:>+8.6f}, {self.mag_1_proc_y:>+8.6f}, {self.mag_1_proc_z:>+8.6f}], " \
               f"mag_1_norm={self.mag_1_norm:>+8.6f}, " \
               f"mag_1_t={self.mag_1_proc_time:>6.3f}; " \
               f"mag_2=[{self.mag_2_proc_x:>+8.3f}, {self.mag_2_proc_y:>+8.3f}, {self.mag_2_proc_z:>+8.3f}], " \
               f"mag_2_norm={self.mag_2_norm:>+8.3f}, " \
               f"mag_2_t={self.mag_2_proc_time:>6.3f})"

    def to_csv(self):
        return f"{self.gyro_1_proc_x:>+8.3f};{self.gyro_1_proc_y:>+8.3f};{self.gyro_1_proc_z:>+8.3f};" \
               f"{self.gyro_1_proc_time:>6.5f};" \
               f"{self.gyro_2_proc_x:>+8.3f};{self.gyro_2_proc_y:>+8.3f};{self.gyro_2_proc_z:>+8.3f};" \
               f"{self.gyro_2_proc_time:>6.5f};" \
               f"{self.accel_1_proc_x:>+8.3f};{self.accel_1_proc_y:>+8.3f};{self.accel_1_proc_z:>+8.3f};" \
               f"{self.accel_1_proc_time:>6.5f};" \
               f"{self.mag_1_proc_x:>+8.6f};{self.mag_1_proc_y:>+8.6f};{self.mag_1_proc_z:>+8.6f};" \
               f"{self.mag_1_norm:>+8.6f};" \
               f"{self.mag_1_proc_time:>6.5f};" \
               f"{self.mag_2_proc_x:>+8.3f};{self.mag_2_proc_y:>+8.3f};{self.mag_2_proc_z:>+8.3f};" \
               f"{self.mag_2_norm:>+8.3f};" \
               f"{self.mag_2_proc_time:>6.5f};\n"

    @staticmethod
    def csv_header():
        return "gyro_1_proc_x;gyro_1_proc_y;gyro_1_proc_z;gyro_1_proc_time;" \
               "gyro_2_proc_x;gyro_2_proc_y;gyro_2_proc_z;gyro_2_proc_time;" \
               "accel_1_proc_x;accel_1_proc_y;accel_1_proc_z;accel_1_proc_time;" \
               "mag_1_proc_x;mag_1_proc_y;mag_1_proc_z;mag_1_norm;mag_1_proc_time;" \
               "mag_2_proc_x;mag_2_proc_y;mag_2_proc_z;mag_1_norm;mag_2_proc_time;\n"


@dataclass
class ShearWaterEulerPacket:
    roll: float
    pitch: float
    yaw: float
    roll_rate: float
    pitch_rate: float
    yaw_rate: float
    time_stamp: float

    def __repr__(self):
        return f"EulerPacket("\
               f"roll={self.roll:>+8.3f}; pitch={self.pitch:>+8.3f}; yaw={self.yaw:>+8.3f}; "\
               f"roll_rate={self.roll_rate:>+8.3f}; pitch_rate={self.pitch_rate:>+8.3f}; yaw_rate={self.yaw_rate:>+8.3f}; " \
               f"time_stamp={self.time_stamp:>6.3f})"

    def to_csv(self):
        return f"{self.roll:>+8.3f};{self.pitch:>+8.3f};{self.yaw:>+8.3f};" \
               f"{self.roll_rate:>+8.3f};{self.pitch_rate:>+8.3f};{self.yaw_rate:>+8.3f};" \
               f"{self.time_stamp:>6.5f};\n"

    @staticmethod
    def csv_header():
        return "roll;pitch;yaw;roll_rate;pitch_rate;yaw_rate;time_stamp;\n"


@dataclass
class ShearWaterHealthPacket:
    health: int

    def __repr__(self):
        return f"HealthPacket("\
               f"raw_value=0x{self.health:04X}; " \
               f"OVF={bool((self.health >> 8) & 0x01)}, " \
               f"ACC1_N={bool((self.health >> 7) & 0x01)}, " \
               f"MAG1_N={bool((self.health >> 6) & 0x01)}, " \
               f"MAG2_N={bool((self.health >> 5) & 0x01)}, " \
               f"ACCEL1={bool((self.health >> 4) & 0x01)}, "\
               f"GYRO1={bool((self.health >> 3) & 0x01)}, " \
               f"GYRO2={bool((self.health >> 2) & 0x01)}, " \
               f"MAG1={bool((self.health >> 1) & 0x01)}, " \
               f"MAG2={bool((self.health >> 0) & 0x01)})"


@dataclass
class ShearWaterRawAccel1Packet:
    accel_1_raw_x: int
    accel_1_raw_y: int
    accel_1_raw_z: int
    accel_1_raw_time: float


@dataclass
class ShearWaterRawGyro1Packet:
    gyro_1_raw_x: int
    gyro_1_raw_y: int
    gyro_1_raw_z: int
    gyro_1_raw_time: float


@dataclass
class ShearWaterRawGyro2Packet:
    gyro_2_raw_x: int
    gyro_2_raw_y: int
    gyro_2_raw_z: int
    gyro_2_raw_time: float


@dataclass
class ShearWaterRawMag1Packet:
    mag_1_raw_x: int
    mag_1_raw_y: int
    mag_1_raw_z: int
    mag_1_raw_time: float


@dataclass
class ShearWaterRawMag2Packet:
    mag_2_raw_x: int
    mag_2_raw_y: int
    mag_2_raw_z: int
    mag_2_raw_time: float


@dataclass
class ShearWaterTemperaturePacket:
    temperature: float
    temperature_time: float


@dataclass
class ShearWaterProcAccel1Packet:
    accel_1_proc_x: float
    accel_1_proc_y: float
    accel_1_proc_z: float
    accel_1_proc_time: float


@dataclass
class ShearWaterProcGyro1Packet:
    gyro_1_proc_x: float
    gyro_1_proc_y: float
    gyro_1_proc_z: float
    gyro_1_proc_time: float


@dataclass
class ShearWaterProcGyro2Packet:
    gyro_2_proc_x: float
    gyro_2_proc_y: float
    gyro_2_proc_z: float
    gyro_2_proc_time: float


@dataclass
class ShearWaterProcMag1Packet:
    mag_1_proc_x: float
    mag_1_proc_y: float
    mag_1_proc_z: float
    mag_1_proc_norm: float
    mag_1_proc_time: float


@dataclass
class ShearWaterProcMag2Packet:
    mag_2_proc_x: float
    mag_2_proc_y: float
    mag_2_proc_z: float
    mag_2_proc_norm: float
    mag_2_proc_time: float


@dataclass
class ShearWaterQuaternionPacket:
    q_w: float
    q_x: float
    q_y: float
    q_z: float
    q_time: float

    def __repr__(self):
        return f"QuaternionPacket("\
               f"q_w={self.q_w:>+3.5f}; q_x={self.q_x:>+3.5f}; q_y={self.q_y:>+3.5f}; q_z={self.q_z:>+3.5f};"\
               f" time_stamp={self.q_time:>6.5f})"

    def to_csv(self):
        return f"{self.q_w:>+3.5f};{self.q_x:>+3.5f};{self.q_y:>+3.5f};{self.q_z:>+3.5f};" \
               f"{self.q_time:>6.5f};\n"

    @staticmethod
    def csv_header():
        return "q_w;q_x;q_y;q_z;q_time;\n"


@dataclass
class ShearWaterEulerPosePacket:
    roll: float
    pitch: float
    yaw: float
    roll_rate: float
    pitch_rate: float
    yaw_rate: float
    euler_time: float
    position_north: float
    position_east: float
    position_up: float
    position_time: float


@dataclass
class ShearWaterPosePacket:
    position_north: float
    position_east: float
    position_up: float
    position_time: float


@dataclass
class ShearWaterVelocityPacket:
    velocity_north: float
    velocity_east: float
    velocity_up: float
    velocity_time: float


@dataclass
class ShearWaterGyro1BiasPacket:
    gyro_1_bias_x: float
    gyro_1_bias_y: float
    gyro_1_bias_z: float


@dataclass
class ShearWaterGyro2BiasPacket:
    gyro_2_bias_x: float
    gyro_2_bias_y: float
    gyro_2_bias_z: float
