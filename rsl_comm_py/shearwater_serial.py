#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# Date: 2 March 2020
# Version: v0.1
# License: MIT

import json
import logging
import os
import os.path
import serial
import struct
import sys

from time import monotonic
from serial.tools import list_ports
from typing import Tuple, List, Dict, Any, Union, Callable

from rsl_comm_py.shearwater_broadcast_packets import ShearWaterAllRawPacket, ShearWaterAllProcPacket, ShearWaterQuaternionPacket
from rsl_comm_py.shearwater_broadcast_packets import ShearWaterEulerPacket, ShearWaterHealthPacket
from rsl_comm_py.shearwater_broadcast_packets import ShearWaterRawAccel1Packet, ShearWaterRawGyro1Packet, ShearWaterRawGyro2Packet
from rsl_comm_py.shearwater_broadcast_packets import ShearWaterRawMag1Packet, ShearWaterRawMag2Packet
from rsl_comm_py.shearwater_broadcast_packets import ShearWaterProcAccel1Packet, ShearWaterProcGyro1Packet, ShearWaterProcGyro2Packet
from rsl_comm_py.shearwater_broadcast_packets import ShearWaterProcMag1Packet, ShearWaterProcMag2Packet
from rsl_comm_py.shearwater_broadcast_packets import ShearWaterGyro1BiasPacket, ShearWaterGyro2BiasPacket

from rsl_comm_py.shearwater_registers import ShearWaterRegisters
from rsl_comm_py.um7_serial import RslException


class ShearWaterSerial(ShearWaterRegisters):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device_file = kwargs.get('device')
        self.device_dict = None
        self.port = serial.Serial()
        self.port_name = None
        self.port_config = None
        self.buffer = bytes()
        self.buffer_size = 384
        self.firmware_version = None
        self.uid_32_bit = None
        if kwargs.get('port_name') is not None:
            self.port_name = kwargs.get('port_name')
        else:
            port_found = self.find_port()
            if not port_found:
                raise RslException("Device specified in the config is not connected!")
        self.init_connection()

    def init_connection(self):
        self.port = serial.Serial(port=self.port_name)
        self.port.port = self.port_name
        self.port.baudrate = 115200
        if not self.port.is_open:
            self.port.open()

    def connect(self, *args, **kwargs):
        self.init_connection()

    def autodetect(self):
        device_list = list_ports.comports()
        for device in device_list:
            json_config = {}
            # go through device list and check each FTDI device for a match
            if device.manufacturer == "FTDI":
                json_config['ID_VENDOR'] = device.manufacturer
                json_config['ID_SERIAL_SHORT'] = device.serial_number
                # don't know what the model should look like so were making it "pid:vid".
                # This matches the windows section of the autodetect script
                json_config['ID_MODEL'] = '{0:04x}:{1:04x}'.format(device.vid, device.pid)
                if self.device_dict == json_config:
                    self.port_name = device.device  # set serial port ("COM4", for example)
                    return True
        else:
            return False

    def find_port(self):
        if not self.device_file:
            raise RslException("No configuration file specified!")
        if not os.path.isfile(self.device_file):
            src_path = os.path.dirname(__file__)
            guessing_file_path = os.path.join(src_path, self.device_file)
            if not os.path.isfile(guessing_file_path):
                raise RslException(f"Specify absolute path to the `device` json file, cannot find {self.device_file}")
            else:
                self.device_file = guessing_file_path
        with open(self.device_file) as fp:
            self.device_dict = json.load(fp)
        # go through each device and match vendor, then key
        return self.autodetect()

    def get_preamble(self):
        preamble = bytes('snp', encoding='ascii')
        return preamble

    def compute_checksum(self, partial_packet: bytes) -> bytes:
        checksum = 0
        for byte in partial_packet:
            checksum += byte
        checksum_bytes = int.to_bytes(checksum, length=2, byteorder='big', signed=False)
        return checksum_bytes

    def construct_packet_type(self, has_data: bool = False, data_length: int = 0,
                              hidden: bool = False, command_failed: bool = False) -> int:
        if data_length > 31:
            raise RslException(f"Batch size for command should not exceed 31, but got {data_length}")
        packet_type = has_data << 7 | data_length << 2 | hidden << 1 | command_failed
        return packet_type

    def get_packet_type(self, extracted_packet_type: int) -> Tuple[bool, int, bool, bool]:
        has_data = bool(extracted_packet_type >> 7 & 1)
        batch_length = extracted_packet_type >> 2 & 0x0F
        hidden = bool(extracted_packet_type >> 1 & 1)
        error_happened = bool(extracted_packet_type & 1)
        return has_data, batch_length, hidden, error_happened

    def construct_packet(self, packet_type: int, address: int, payload: bytes = bytes()) -> bytes:
        preamble = self.get_preamble()
        packet_type_byte = int.to_bytes(packet_type, length=1, byteorder='big')
        address_byte = int.to_bytes(address, length=1, byteorder='big')
        partial_packet = preamble + packet_type_byte + address_byte + payload
        checksum = self.compute_checksum(partial_packet)
        packet = partial_packet + checksum
        return packet

    def send(self, packet: bytes) -> bool:
        bytes_written = self.port.write(packet)
        self.port.flush()
        return bytes_written == len(packet)

    def recv(self) -> Tuple[bool, bytes]:
        ok = False
        while not ok:
            # read until we get something in the buffer
            in_waiting = self.port.in_waiting
            logging.info(f"waiting buffer: {in_waiting}")
            # self.buffer += self.port.read(self.buffer_size)
            self.buffer += self.port.read(in_waiting)
            logging.info(f"buffer size: {len(self.buffer)}")
            # self.__buffer = self.__port.read(self.__port.inWaiting()) # causes too long of a delay
            ok = len(self.buffer) > 0
        return True, self.buffer

    def send_recv(self, packet: bytes) -> bytes:
        send_ok = self.send(packet)
        if not send_ok:
            raise RslException("Sending packet failed!")
        recv_ok, _ = self.recv()
        if not recv_ok:
            raise RslException("Receiving packet failed!")
        return self.buffer

    def find_packet(self, sensor_response: bytes) -> Tuple[bytes, bytes]:
        preamble = self.get_preamble()
        packet_start_idx = sensor_response.find(preamble)

        if packet_start_idx == -1:
            # preamble of packet not found, exit
            return bytes(), bytes()

        next_packet_rel_idx = sensor_response[packet_start_idx+3:].find(preamble)
        next_packet_start_idx = packet_start_idx + 3 + next_packet_rel_idx

        if next_packet_start_idx == -1:
            # preamble of next packet not found, exit
            return bytes(), bytes()

        # complete packet found in data
        packet = sensor_response[packet_start_idx:next_packet_start_idx]
        remainder = sensor_response[next_packet_start_idx:]
        return packet, remainder

    def find_response(self, reg_addr: int, hidden: bool = False, expected_length: int = 7) -> Tuple[bool, bytes]:
        while len(self.buffer) > 0:
            packet, self.buffer = self.find_packet(self.buffer)
            if len(packet) < 7:
                return False, bytes()
            logging.debug(f"{packet}")
            logging.debug(f"addr: {packet[4]}")
            packet_type = packet[3]
            is_packet_hidden = bool((packet_type >> 1) & 0x01)
            response_addr = packet[4]
            if response_addr == reg_addr and hidden == is_packet_hidden and len(packet) == expected_length:
                # required packet found
                return True, packet
        else:
            return False, bytes()

    def verify_checksum(self, packet: bytes) -> bool:
        computed_checksum = 0
        for byte in packet[:-2]:
            computed_checksum += byte
        received_checksum = int.from_bytes(packet[-2:], byteorder='big', signed=False)
        return computed_checksum == received_checksum

    def get_payload(self, packet: bytes) -> Tuple[bool, bytes]:
        ok = self.verify_checksum(packet)
        if not ok:
            raise RslException("Packet checksum INVALID!")
        return True, packet[5:-2]

    def check_packet(self, packet: bytes) -> bool:
        packet_type = packet[3]
        has_data = bool(packet_type & (1 << 7))
        data_len = (packet_type >> 2) & 0x1F
        error = packet_type & 0x01
        if error:
            logging.error(f"Error bit set for packet: {packet}!")
            return False
        elif not has_data and len(packet) != 7:
            logging.error(f"Packet without data (has_data = 0) shall have 7 bytes, got {len(packet)}")
            return False
        elif has_data and data_len == 0 and len(packet) != 11:
            logging.error(f"Single packet has 4 bytes payload, in total 11 bytes, got {len(packet)}")
            return False
        elif has_data and data_len > 0 and len(packet) != 7 + 4 * data_len:
            logging.error(f"Batch packet with data_len {data_len} shall be {7 + 4 * data_len} bytes, got {len(packet)}")
            return False
        else:
            # all the checks pass then
            return True

    def read_register(self, reg_addr: int, hidden: bool = False) -> Tuple[bool, bytes]:
        packet_type = self.construct_packet_type(hidden=hidden)
        packet_to_send = self.construct_packet(packet_type, reg_addr)
        logging.debug(f"packet sent: {packet_to_send}")
        self.send_recv(packet_to_send)
        t = monotonic()
        ok, sensor_reply = self.find_response(reg_addr, hidden, 11)
        if ok:
            logging.debug(f"packet: {sensor_reply}")
            self.check_packet(sensor_reply)
            ok, payload = self.get_payload(sensor_reply)
            return ok, payload
        else:
            while monotonic() - t < 0.15:
                # try to send <-> receive packets for a pre-defined time out time
                self.send_recv(packet_to_send)
                ok, sensor_reply = self.find_response(reg_addr, hidden, 11)
                if ok:
                    logging.debug(f"packet: {sensor_reply}")
                    self.check_packet(sensor_reply)
                    ok, payload = self.get_payload(sensor_reply)
                    return ok, payload
            return False, bytes()

    def write_register(self, reg_addr: int, reg_value: Union[int, bytes, float, str], hidden: bool = False) -> bool:
        packet_type = self.construct_packet_type(has_data=True, hidden=hidden)
        if type(reg_value) == int:
            payload = int.to_bytes(reg_value, byteorder='big', length=4)
        elif type(reg_value) == bytes:
            payload = reg_value

        elif type(reg_value) == float:
            payload = struct.pack('>f', reg_value)
        elif type(reg_value) == str:
            payload = bytes(reg_value, encoding='utf-8')
        else:
            raise RslException(f"writing register {reg_addr} with payload of type {type(reg_value)}"
                               " but only `int`, `bytes`, `float`, `str` are supported!")
        if len(payload) % 4 != 0:
            logging.warning(f"Payload length is {len(payload)}, not divisible by 4, you are doing smth. wrong!")
        packet_to_send = self.construct_packet(packet_type, reg_addr, payload)
        logging.debug(f"packet sent: {packet_to_send}")
        self.send_recv(packet_to_send)
        ok, sensor_reply = self.find_response(reg_addr)
        if ok:
            logging.debug(f"packet: {sensor_reply}")
            self.check_packet(sensor_reply)
            ok, payload = self.get_payload(sensor_reply)
            return ok

    def recv_broadcast_packet(self, packet_target_addr: int, expected_packet_length: int,
                              decode_callback: Callable, num_packets: int = -1):
        received_packets = 0
        while num_packets == -1 or received_packets < num_packets:
            ok, _ = self.recv()
            while len(self.buffer) > 0:
                packet, self.buffer = self.find_packet(self.buffer)
                # logging.info(f"buffer length: {len(self.buffer)}")
                if len(packet) > 7:
                    recv_packet_addr = packet[4]
                    if recv_packet_addr == packet_target_addr:
                        packet_correct_length = len(packet) == expected_packet_length
                        if not packet_correct_length:
                            logging.error(f"Invalid packet length for addr: {packet_target_addr}, "
                                          f"expected: {expected_packet_length}, got: {len(packet)}, packet: {packet}")
                        checksum_ok = self.verify_checksum(packet)
                        if not checksum_ok:
                            logging.error(f"Checksum failed for broadcast packet with addr: {packet_target_addr}")
                        packet_type_check_ok = self.check_packet(packet)
                        if not packet_type_check_ok:
                            logging.error(f"Checking packet type failed for broadcast with addr: {packet_target_addr}!")
                        if packet_correct_length and checksum_ok and packet_type_check_ok:
                            yield decode_callback(packet)
                            received_packets += 1

    def recv_all_raw_broadcast(self, num_packets: int = -1):
        all_raw_start_addr = self.svd_parser.find_register_by(name='DREG_GYRO_1_RAW_XY').address
        broadcast_packet_length = 79
        return self.recv_broadcast_packet(all_raw_start_addr, broadcast_packet_length,
                                          self.decode_all_raw_broadcast, num_packets)

    def recv_all_proc_broadcast(self, num_packets: int = -1):
        all_proc_start_addr = self.svd_parser.find_register_by(name='DREG_GYRO_1_PROC_X').address
        broadcast_packet_length = 95
        return self.recv_broadcast_packet(all_proc_start_addr, broadcast_packet_length,
                                          self.decode_all_proc_broadcast, num_packets)

    def recv_euler_broadcast(self, num_packets: int = -1):
        euler_start_addr = self.svd_parser.find_register_by(name='DREG_EULER_PHI_THETA').address
        broadcast_packet_length = 27
        return self.recv_broadcast_packet(euler_start_addr, broadcast_packet_length,
                                          self.decode_euler_broadcast, num_packets)

    def recv_quaternion_broadcast(self, num_packets: int = -1):
        quat_start_addr = self.svd_parser.find_register_by(name='DREG_QUAT_AB').address
        broadcast_packet_length = 19
        return self.recv_broadcast_packet(quat_start_addr, broadcast_packet_length,
                                          self.decode_quaternion_broadcast, num_packets)

    def recv_health_broadcast(self, num_packets: int = -1):
        health_start_addr = self.svd_parser.find_register_by(name='DREG_HEALTH').address
        broadcast_packet_length = 11
        return self.recv_broadcast_packet(health_start_addr, broadcast_packet_length,
                                          self.decode_health_broadcast, num_packets)

    def recv_raw_accel_1_packet(self, num_packets: int = -1):
        raw_accel_1_addr = self.svd_parser.find_register_by(name='DREG_ACCEL_1_RAW_XY').address
        broadcast_packet_length = 19
        return self.recv_broadcast_packet(raw_accel_1_addr, broadcast_packet_length,
                                          self.decode_raw_accel_1_broadcast, num_packets)

    def recv_raw_gyro_1_packet(self, num_packets: int = -1):
        raw_gyro_1_addr = self.svd_parser.find_register_by(name='DREG_GYRO_1_RAW_XY').address
        broadcast_packet_length = 19
        return self.recv_broadcast_packet(raw_gyro_1_addr, broadcast_packet_length,
                                          self.decode_raw_gyro_1_broadcast, num_packets)

    def recv_raw_gyro_2_packet(self, num_packets: int = -1):
        raw_gyro_2_addr = self.svd_parser.find_register_by(name='DREG_GYRO_2_RAW_XY').address
        broadcast_packet_length = 19
        return self.recv_broadcast_packet(raw_gyro_2_addr, broadcast_packet_length,
                                          self.decode_raw_gyro_2_broadcast, num_packets)

    def recv_raw_mag_1_packet(self, num_packets: int = -1):
        raw_mag_1_addr = self.svd_parser.find_register_by(name='DREG_MAG_1_RAW_XY').address
        broadcast_packet_length = 23
        return self.recv_broadcast_packet(raw_mag_1_addr, broadcast_packet_length,
                                          self.decode_raw_mag_1_broadcast, num_packets)

    def recv_raw_mag_2_packet(self, num_packets: int = -1):
        raw_mag_2_addr = self.svd_parser.find_register_by(name='DREG_MAG_2_RAW_XY').address
        broadcast_packet_length = 19
        return self.recv_broadcast_packet(raw_mag_2_addr, broadcast_packet_length,
                                          self.decode_raw_mag_2_broadcast, num_packets)

    def recv_proc_accel_1_packet(self, num_packets: int = -1):
        proc_accel_1_addr = self.svd_parser.find_register_by(name='DREG_ACCEL_1_PROC_X').address
        broadcast_packet_length = 23
        return self.recv_broadcast_packet(proc_accel_1_addr, broadcast_packet_length,
                                          self.decode_proc_accel_1_broadcast, num_packets)

    def recv_proc_gyro_1_packet(self, num_packets: int = -1):
        proc_gyro_1_addr = self.svd_parser.find_register_by(name='DREG_GYRO_1_PROC_X').address
        broadcast_packet_length = 23
        return self.recv_broadcast_packet(proc_gyro_1_addr, broadcast_packet_length,
                                          self.decode_proc_gyro_1_broadcast, num_packets)

    def recv_proc_gyro_2_packet(self, num_packets: int = -1):
        proc_gyro_2_addr = self.svd_parser.find_register_by(name='DREG_GYRO_2_PROC_X').address
        broadcast_packet_length = 23
        return self.recv_broadcast_packet(proc_gyro_2_addr, broadcast_packet_length,
                                          self.decode_proc_gyro_2_broadcast, num_packets)

    def recv_proc_mag_1_packet(self, num_packets: int = -1):
        proc_mag_1_addr = self.svd_parser.find_register_by(name='DREG_MAG_1_PROC_X').address
        broadcast_packet_length = 27
        return self.recv_broadcast_packet(proc_mag_1_addr, broadcast_packet_length,
                                          self.decode_proc_mag_1_broadcast, num_packets)

    def recv_proc_mag_2_packet(self, num_packets: int = -1):
        proc_mag_2_addr = self.svd_parser.find_register_by(name='DREG_MAG_2_PROC_X').address
        broadcast_packet_length = 27
        return self.recv_broadcast_packet(proc_mag_2_addr, broadcast_packet_length,
                                          self.decode_proc_mag_2_broadcast, num_packets)

    def recv_broadcast(self,  num_packets: int = -1):
        received_packets = 0
        while num_packets == -1 or received_packets < num_packets:
            ok, _ = self.recv()
            while len(self.buffer) > 0:
                packet, self.buffer = self.find_packet(self.buffer)
                if len(packet) > 7:
                    packet_addr = packet[4]
                    start_reg = self.svd_parser.find_register_by(address=packet_addr)
                    checksum_ok = self.verify_checksum(packet)
                    if not checksum_ok:
                        logging.error(f"Checksum failed for broadcast packet with start_reg: {start_reg}")
                    packet_type_check_ok = self.check_packet(packet)
                    if not packet_type_check_ok:
                        logging.error(f"Checking packet type failed for broadcast with start_reg: {start_reg}!")
                    health_start_addr = self.svd_parser.find_register_by(name='DREG_HEALTH').address
                    euler_start_addr = self.svd_parser.find_register_by(name='DREG_EULER_PHI_THETA').address
                    all_proc_start_addr = self.svd_parser.find_register_by(name='DREG_GYRO_1_PROC_X').address
                    gyro_2_proc_start_addr = self.svd_parser.find_register_by(name='DREG_GYRO_2_PROC_X').address
                    accel_1_proc_start_addr = self.svd_parser.find_register_by(name='DREG_ACCEL_1_PROC_X').address
                    mag_1_proc_start_addr = self.svd_parser.find_register_by(name='DREG_MAG_1_PROC_X').address
                    mag_2_proc_start_addr = self.svd_parser.find_register_by(name='DREG_MAG_2_PROC_X').address
                    all_raw_start_addr = self.svd_parser.find_register_by(name='DREG_GYRO_1_RAW_XY').address
                    gyro_2_raw_start_addr = self.svd_parser.find_register_by(name='DREG_GYRO_2_RAW_XY').address
                    accel_1_raw_start_addr = self.svd_parser.find_register_by(name='DREG_ACCEL_1_RAW_XY').address
                    mag_1_raw_start_addr = self.svd_parser.find_register_by(name='DREG_MAG_1_RAW_X').address
                    mag_2_raw_start_addr = self.svd_parser.find_register_by(name='DREG_MAG_2_RAW_XY').address
                    gyro_1_bias_start_addr = self.svd_parser.find_register_by(name='DREG_GYRO_1_BIAS_X').address
                    gyro_2_bias_start_addr = self.svd_parser.find_register_by(name='DREG_GYRO_2_BIAS_X').address
                    quat_addr = self.svd_parser.find_register_by(name='DREG_QUAT_AB').address

                    if packet_addr == health_start_addr:
                        if len(packet) == 11:
                            logging.info(f"[HEALTH]: broadcast packet found!")
                            yield self.decode_health_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[HEALTH]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == euler_start_addr:
                        if len(packet) == 27:
                            logging.info(f"[EULER]: broadcast packet found!")
                            yield self.decode_euler_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[EULER]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == all_proc_start_addr:
                        if len(packet) == 95:
                            logging.info(f"[ALL_PROC]: broadcast packet found!")
                            yield self.decode_all_proc_broadcast(packet)
                            received_packets += 1
                        elif len(packet) == 23:
                            logging.info(f"[GYRO_1_PROC]: broadcast packet found!")
                            yield self.decode_proc_gyro_1_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[GYRO_1_PROC]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == gyro_2_proc_start_addr:
                        if len(packet) == 23:
                            logging.info(f"[GYRO_2_PROC]: broadcast packet found!")
                            yield self.decode_proc_gyro_2_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[GYRO_2_PROC]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == accel_1_proc_start_addr:
                        if len(packet) == 23:
                            logging.info(f"[ACCEL_1_PROC]: broadcast packet found!")
                            yield self.decode_proc_accel_1_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[ACCEL_1_PROC]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == mag_1_proc_start_addr:
                        if len(packet) == 27:
                            logging.info(f"[MAG_1_PROC]: broadcast packet found!")
                            yield self.decode_proc_mag_1_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[MAG_1_PROC]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == mag_2_proc_start_addr:
                        if len(packet) == 27:
                            logging.info(f"[MAG_2_PROC]: broadcast packet found!")
                            yield self.decode_proc_mag_2_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[MAG_2_PROC]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == all_raw_start_addr:
                        if len(packet) == 79:
                            logging.info(f"[ALL_RAW]: broadcast packet found!")
                            yield self.decode_all_raw_broadcast(packet)
                            received_packets += 1
                        elif len(packet) == 19:
                            logging.info(f"[GYRO_1_RAW]: broadcast packet found!")
                            yield self.decode_raw_gyro_1_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[GYRO_1_RAW]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == gyro_2_raw_start_addr:
                        if len(packet) == 19:
                            logging.info(f"[GYRO_2_RAW]: broadcast packet found!")
                            yield self.decode_raw_gyro_2_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[GYRO_2_PROC]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == accel_1_raw_start_addr:
                        if len(packet) == 19:
                            logging.info(f"[ACCEL_1_RAW]: broadcast packet found!")
                            yield self.decode_raw_accel_1_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[ACCEL_1_RAW]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == mag_1_raw_start_addr:
                        if len(packet) == 23:
                            logging.info(f"[MAG_1_RAW]: broadcast packet found!")
                            yield self.decode_raw_mag_1_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[MAG_1_RAW]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == mag_2_raw_start_addr:
                        if len(packet) == 19:
                            logging.info(f"[MAG_2_RAW]: broadcast packet found!")
                            yield self.decode_raw_mag_2_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[MAG_2_RAW]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == quat_addr:
                        if len(packet) == 19:
                            logging.info(f"[QUAT]: quaternion broadcast packet found!")
                            yield self.decode_quaternion_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[QUAT]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == gyro_1_bias_start_addr:
                        if len(packet) == 19:
                            logging.info(f"[GYRO_1_BIAS]: broadcast packet found!")
                            yield self.decode_gyro_1_bias_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[GYRO_1_BIAS]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    elif packet_addr == gyro_2_bias_start_addr:
                        if len(packet) == 19:
                            logging.info(f"[GYRO_2_BIAS]: quaternion broadcast packet found!")
                            yield self.decode_gyro_2_bias_broadcast(packet)
                            received_packets += 1
                        else:
                            logging.error(f"[GYRO_2_BIAS]: invalid packet length, got {len(packet)}, packet: {packet}!")
                    else:
                        logging.error(f"[BROADCAST ERROR]: packet with addr {packet_addr}, reg: {start_reg.name} found "
                                      f"of length: {len(packet)} bytes, "
                                      f"no decoding is implemented for this!! Packet: {packet}")

    def decode_all_raw_broadcast(self, packet) -> ShearWaterAllRawPacket:
        payload = packet[5:-2]
        g_1_x, g_1_y, g_1_z, g_1_time = struct.unpack('>hhh2xf', payload[0:12])
        g_2_x, g_2_y, g_2_z, g_2_time = struct.unpack('>hhh2xf', payload[12:24])
        a_1_x, a_1_y, a_1_z, a_1_time = struct.unpack('>hhh2xf', payload[24:36])
        m_1_x, m_1_y, m_1_z, m_1_time = struct.unpack('>iiif',   payload[36:52])
        m_2_x, m_2_y, m_2_z, m_2_time = struct.unpack('>hhh2xf', payload[52:64])
        T, T_t = struct.unpack('>ff', payload[64:72])
        return ShearWaterAllRawPacket(
            gyro_1_raw_x=g_1_x, gyro_1_raw_y=g_1_y, gyro_1_raw_z=g_1_z, gyro_1_raw_time=g_1_time,
            gyro_2_raw_x=g_2_x, gyro_2_raw_y=g_2_y, gyro_2_raw_z=g_2_z, gyro_2_raw_time=g_2_time,
            accel_1_raw_x=a_1_x, accel_1_raw_y=a_1_y, accel_1_raw_z=a_1_z, accel_1_raw_time=a_1_time,
            mag_1_raw_x=m_1_x, mag_1_raw_y=m_1_y, mag_1_raw_z=m_1_z, mag_1_raw_time=m_1_time,
            mag_2_raw_x=m_2_x, mag_2_raw_y=m_2_y, mag_2_raw_z=m_2_z, mag_2_raw_time=m_2_time,
            temperature=T, temperature_time=T_t)

    def decode_all_proc_broadcast(self, packet) -> ShearWaterAllProcPacket:
        payload = packet[5:-2]
        g_1_x, g_1_y, g_1_z, g_1_time = struct.unpack('>ffff', payload[0:16])
        g_2_x, g_2_y, g_2_z, g_2_time = struct.unpack('>ffff', payload[16:32])
        a_1_x, a_1_y, a_1_z, a_1_time = struct.unpack('>ffff', payload[32:48])
        m_1_x, m_1_y, m_1_z, m_1_norm, m_1_time = struct.unpack('>fffff', payload[48:68])
        m_2_x, m_2_y, m_2_z, m_2_norm, m_2_time = struct.unpack('>fffff', payload[68:88])
        return ShearWaterAllProcPacket(
            gyro_1_proc_x=g_1_x, gyro_1_proc_y=g_1_y, gyro_1_proc_z=g_1_z, gyro_1_proc_time=g_1_time,
            gyro_2_proc_x=g_2_x, gyro_2_proc_y=g_2_y, gyro_2_proc_z=g_2_z, gyro_2_proc_time=g_2_time,
            accel_1_proc_x=a_1_x, accel_1_proc_y=a_1_y, accel_1_proc_z=a_1_z, accel_1_proc_time=a_1_time,
            mag_1_proc_x=m_1_x, mag_1_proc_y=m_1_y, mag_1_proc_z=m_1_z, mag_1_norm=m_1_norm, mag_1_proc_time=m_1_time,
            mag_2_proc_x=m_2_x, mag_2_proc_y=m_2_y, mag_2_proc_z=m_2_z, mag_2_norm=m_2_norm, mag_2_proc_time=m_2_time)

    def decode_euler_broadcast(self, packet) -> ShearWaterEulerPacket:
        payload = packet[5:-2]
        roll, pitch, yaw = struct.unpack('>hhh2x', payload[0:8])
        roll_rate, pitch_rate, yaw_rate, time_stamp = struct.unpack('>hhh2xf', payload[8:20])
        return ShearWaterEulerPacket(
            roll=roll/91.02222, pitch=pitch/91.02222, yaw=yaw/91.02222,
            roll_rate=roll_rate/91.02222, pitch_rate=pitch_rate/91.02222, yaw_rate=yaw_rate/91.02222,
            time_stamp=time_stamp
        )

    def decode_quaternion_broadcast(self, packet) -> ShearWaterQuaternionPacket:
        payload = packet[5:-2]
        q_w, q_x, q_y, q_z, q_time = struct.unpack('>hhhhf', payload[0:12])
        return ShearWaterQuaternionPacket(
            q_w=q_w/29789.09091, q_x=q_x/29789.09091, q_y=q_y/29789.09091, q_z=q_z/29789.09091, q_time=q_time
        )

    def decode_raw_accel_1_broadcast(self, packet) -> ShearWaterRawAccel1Packet:
        payload = packet[5:-2]
        a_1_x, a_1_y, a_1_z, a_1_time = struct.unpack('>hhh2xf', payload[0:12])
        return ShearWaterRawAccel1Packet(accel_1_raw_x=a_1_x, accel_1_raw_y=a_1_y, accel_1_raw_z=a_1_z,
                                         accel_1_raw_time=a_1_time)

    def decode_raw_gyro_1_broadcast(self, packet) -> ShearWaterRawGyro1Packet:
        payload = packet[5:-2]
        g_1_x, g_1_y, g_1_z, g_1_time = struct.unpack('>hhh2xf', payload[0:12])
        return ShearWaterRawGyro1Packet(gyro_1_raw_x=g_1_x, gyro_1_raw_y=g_1_y, gyro_1_raw_z=g_1_z,
                                        gyro_1_raw_time=g_1_time)

    def decode_raw_gyro_2_broadcast(self, packet) -> ShearWaterRawGyro2Packet:
        payload = packet[5:-2]
        g_2_x, g_2_y, g_2_z, g_2_time = struct.unpack('>hhh2xf', payload[0:12])
        return ShearWaterRawGyro2Packet(gyro_2_raw_x=g_2_x, gyro_2_raw_y=g_2_y, gyro_2_raw_z=g_2_z,
                                        gyro_2_raw_time=g_2_time)

    def decode_raw_mag_1_broadcast(self, packet) -> ShearWaterRawMag1Packet:
        payload = packet[5:-2]
        m_1_x, m_1_y, m_1_z, m_1_time = struct.unpack('>iiif', payload[0:16])
        return ShearWaterRawMag1Packet(mag_1_raw_x=m_1_x, mag_1_raw_y=m_1_y, mag_1_raw_z=m_1_z,
                                       mag_1_raw_time=m_1_time)

    def decode_raw_mag_2_broadcast(self, packet) -> ShearWaterRawMag2Packet:
        payload = packet[5:-2]
        m_2_x, m_2_y, m_2_z, m_2_time = struct.unpack('>hhh2xf', payload[0:12])
        return ShearWaterRawMag2Packet(mag_2_raw_x=m_2_x, mag_2_raw_y=m_2_y, mag_2_raw_z=m_2_z,
                                       mag_2_raw_time=m_2_time)

    def decode_proc_accel_1_broadcast(self, packet) -> ShearWaterProcAccel1Packet:
        payload = packet[5:-2]
        a_1_x, a_1_y, a_1_z, a_1_time = struct.unpack('>ffff', payload[0:16])
        return ShearWaterProcAccel1Packet(accel_1_proc_x=a_1_x, accel_1_proc_y=a_1_y, accel_1_proc_z=a_1_z,
                                          accel_1_proc_time=a_1_time)

    def decode_proc_gyro_1_broadcast(self, packet) -> ShearWaterProcGyro1Packet:
        payload = packet[5:-2]
        g_1_x, g_1_y, g_1_z, g_1_time = struct.unpack('>ffff', payload[0:16])
        return ShearWaterProcGyro1Packet(gyro_1_proc_x=g_1_x, gyro_1_proc_y=g_1_y, gyro_1_proc_z=g_1_z,
                                         gyro_1_proc_time=g_1_time)

    def decode_proc_gyro_2_broadcast(self, packet) -> ShearWaterProcGyro2Packet:
        payload = packet[5:-2]
        g_2_x, g_2_y, g_2_z, g_2_time = struct.unpack('>ffff', payload[0:16])
        return ShearWaterProcGyro2Packet(gyro_2_proc_x=g_2_x, gyro_2_proc_y=g_2_y, gyro_2_proc_z=g_2_z,
                                         gyro_2_proc_time=g_2_time)

    def decode_proc_mag_1_broadcast(self, packet) -> ShearWaterProcMag1Packet:
        payload = packet[5:-2]
        m_1_x, m_1_y, m_1_z, m_1_norm, m_1_time = struct.unpack('>fffff', payload[0:20])
        return ShearWaterProcMag1Packet(mag_1_proc_x=m_1_x, mag_1_proc_y=m_1_y, mag_1_proc_z=m_1_z,
                                        mag_1_proc_norm=m_1_norm, mag_1_proc_time=m_1_time)

    def decode_proc_mag_2_broadcast(self, packet) -> ShearWaterProcMag2Packet:
        payload = packet[5:-2]
        m_2_x, m_2_y, m_2_z, m_2_norm, m_2_time = struct.unpack('>fffff', payload[0:20])
        return ShearWaterProcMag2Packet(mag_2_proc_x=m_2_x, mag_2_proc_y=m_2_y, mag_2_proc_z=m_2_z,
                                        mag_2_proc_norm=m_2_norm, mag_2_proc_time=m_2_time)

    def decode_gyro_1_bias_broadcast(self, packet) -> ShearWaterGyro1BiasPacket:
        payload = packet[5:-2]
        gyro_1_bias_x, gyro_1_bias_y, gyro_1_bias_z, = struct.unpack('>fff', payload[0:12])
        return ShearWaterGyro1BiasPacket(gyro_1_bias_x=gyro_1_bias_x, gyro_1_bias_y=gyro_1_bias_y,
                                         gyro_1_bias_z=gyro_1_bias_z)

    def decode_gyro_2_bias_broadcast(self, packet) -> ShearWaterGyro2BiasPacket:
        payload = packet[5:-2]
        gyro_2_bias_x, gyro_2_bias_y, gyro_2_bias_z, = struct.unpack('>fff', payload[0:12])
        return ShearWaterGyro2BiasPacket(gyro_2_bias_x=gyro_2_bias_x, gyro_2_bias_y=gyro_2_bias_y,
                                         gyro_2_bias_z=gyro_2_bias_z)

    def decode_health_broadcast(self, packet) -> ShearWaterHealthPacket:
        payload = packet[5:-2]
        health, = struct.unpack('>I', payload[0:4])
        return ShearWaterHealthPacket(health=health)

    def hidden_regs_values(self) -> List[Dict]:
        hidden_regs_as_json = []
        for reg in self.svd_parser.hidden_regs:
            name = reg.name.lower()
            reg, *_ = getattr(self, name)
            hidden_regs_as_json.append(reg.as_dict())
        return hidden_regs_as_json

    def creg_regs_values(self) -> List[Dict]:
        config_regs_as_json = []
        for reg in self.svd_parser.cregs:
            name = reg.name.lower()
            reg, *_ = getattr(self, name)
            config_regs_as_json.append(reg.as_dict())
        return config_regs_as_json

