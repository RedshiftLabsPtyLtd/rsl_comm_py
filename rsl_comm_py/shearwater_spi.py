#!/usr/bin/env python3
# Author: Dr. Konstantin Selyunin
# Date: 12 June 2020
# Version: v0.1
# License: MIT

from rsl_comm_py.rsl_spi import RslSpiUsbIss, RslSpiLinuxPort
from rsl_comm_py.shearwater_registers import ShearWaterRegisters


class ShearWaterSpiLinuxPort(RslSpiLinuxPort, ShearWaterRegisters):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ShearWaterSpiUsbIss(RslSpiUsbIss, ShearWaterRegisters):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == '__main__':
    shearwater_spi_iss = ShearWaterSpiUsbIss()
    print(f"creg_com_settings             : {shearwater_spi_iss.creg_com_settings}")
    print(f"creg_com_rates1               : {shearwater_spi_iss.creg_com_rates1}")
    print(f"creg_com_rates2               : {shearwater_spi_iss.creg_com_rates2}")
    print(f"creg_com_rates3               : {shearwater_spi_iss.creg_com_rates3}")
    print(f"creg_com_rates4               : {shearwater_spi_iss.creg_com_rates4}")
    print(f"creg_com_rates5               : {shearwater_spi_iss.creg_com_rates5}")
    print(f"creg_com_rates6               : {shearwater_spi_iss.creg_com_rates6}")
    print(f"creg_com_rates7               : {shearwater_spi_iss.creg_com_rates7}")
