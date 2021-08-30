#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# Date: 30 August 2021
# Version: v0.1
# License: MIT

from rsl_comm_py.rsl_spi import RslSpiUsbIss, RslSpiLinuxPort
from rsl_comm_py.um8_registers import UM8Registers


class UM8SpiLinuxPort(RslSpiLinuxPort, UM8Registers):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UM8SpiUsbIss(RslSpiUsbIss, UM8Registers):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == '__main__':
    um8_spi_iss = UM8SpiUsbIss()
    print(f"creg_com_settings             : {um8_spi_iss.creg_com_settings}")
    print(f"creg_com_rates1               : {um8_spi_iss.creg_com_rates1}")
    print(f"creg_com_rates2               : {um8_spi_iss.creg_com_rates2}")
    print(f"creg_com_rates3               : {um8_spi_iss.creg_com_rates3}")
    print(f"creg_com_rates4               : {um8_spi_iss.creg_com_rates4}")
    print(f"creg_com_rates5               : {um8_spi_iss.creg_com_rates5}")
    print(f"creg_com_rates6               : {um8_spi_iss.creg_com_rates6}")
    print(f"creg_com_rates7               : {um8_spi_iss.creg_com_rates7}")
