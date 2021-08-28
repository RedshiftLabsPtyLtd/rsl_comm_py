name = 'um7py'
version = '0.4.1'

from um7py.um7_autodetect import um7_autodetect
from um7py.serve_um7_autodetect import serve_autodetect_script
from um7py.shearwater_serial import ShearWaterSerial
from um7py.shearwater_spi import ShearWaterSpiUsbIss, ShearWaterSpiLinuxPort
from um7py.um7_serial import UM7Serial
from um7py.um7_spi import UM7SpiUsbIss, UM7SpiLinuxPort
