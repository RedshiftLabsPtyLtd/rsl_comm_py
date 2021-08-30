# RSL Comm Python Driver

[![PyPI version](https://badge.fury.io/py/rsl-comm-py.svg)](https://badge.fury.io/py/rsl-comm-py)
![test and package](https://github.com/RedshiftLabsPtyLtd/rsl_comm_py/workflows/test%20and%20package/badge.svg)


**TL;DR:** *"Swiss army knife"* for using 
the [`UM7`](https://redshiftlabs.com.au/product/um7-orientation-sensor/), `UM8`,
and  `shearwater` orientation sensors with Python 3 (Python 3.7+).


`UM7` originally came with the 
[_"Serial Software Interface"_](https://redshiftlabs.com.au/support-services/serial-interface-software/)
for handling / communicating with the sensor, which is currently available for Windows only.

The `python3` driver provided here is designed to keep you up and running 
on different platforms (Linux, Windows, Mac).
If you have the `UM7`, `UM8`, or `shearwater` board and want to use it on Linux 
(e.g. Ubuntu, Debian, Raspbian, Yocto, Suse, etc.),
Windows, or Mac, this repo provides driver code to send / receive individual packets
and receive broadcasts, as well example code how to create a sensor communication object.

The driver has the following capabilities: 

* read / write single registers to/from `UM7`, `UM8`, `shearwater` over `SPI`;

* read / write single registers to/from `UM7`, `UM8`, `shearwater` over `UART`;

* receive broadcast packets from the `UM7`, `UM8`, `shearwater` sensor over `UART`;

* register map and interpretation of the sensor registers for `UM7`, `UM8`, `shearwater`.


## Checking out the repo with submodules:

This repo contains 
[git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules),
in particularly [rsl_xml_svd](https://github.com/RedshiftLabsPtyLtd/rsl_xml_svd)
project is included as a submodule. In order to check out the project, including
submodules use the following command:

```sh
git clone --recurse-submodules git@github.com:RedshiftLabsPtyLtd/rsl_comm_py.git
```

If the repo is already cloned without submodules, then in the existing repo:

```sh
git submodule update --recursive --init
```

If using GUI client like git kraken, the following
[post](https://support.gitkraken.com/working-with-repositories/submodules/)
might be useful.

After syncing the sub-modules, the [`rsl_xml_svd`](./rsl_comm_py/rsl_xml_svd) folder 
should appear inside the repo, pointing exactly to the commit specified in this repository.


## Repository structure

To get started, you need to know that communication with the `UM7`, `UM8`, and `shearwater`
is organized as follows. For each sensor, there is a file with register description, and 
separate files with UART and SPI communication. The register description code interprets the 
received payload, and sensor files handle constructing, transmitting and receiving packets.

E.g. for the UM7 the UART communication is coded in 
[`um7_serial.py`](./rsl_comm_py/um7_serial.py) file, 
where the `UM7Serial` class is defined. 
Information about UM7 registers comes to [`um7_serial.py`](./rsl_comm_py/um7_serial.py)
from the [`um7_registers.py`](./rsl_comm_py/um7_registers.py) file, where 
the accessing to the UM7 registers are stored.
Since it is possible to access the UM7 register map over UART and SPI,
the register data (e.g. addresses, fields, and their meaning) is stored in a separate file.
In the [`examples`](./rsl_comm_py/examples) folder we store the examples how to communicate with the 
sensor. 

The `UM7`, `UM8`, and `shearwater` register descriptions are stored in SVD files, 
([`um7.svd`](./rsl_comm_py/rsl_xml_svd/um7.svd), [`um8.svd`](./rsl_comm_py/rsl_xml_svd/um8.svd),
[`shearwater.svd`](./rsl_comm_py/rsl_xml_svd/shearwater.svd))
and is parsed by the [`rsl_svd_parser.py`](./rsl_comm_py/rsl_xml_svd/rsl_svd_parser.py).
The parser extracts the information from the XML file and fills in python data classes.


Below we outline the repo structure:

* [`rsl_comm_py`](./rsl_comm_py): top-level python package;
* [`rsl_comm_py/examples`](./rsl_comm_py/examples) package with example code for receiving broadcast / reading / writing `UM7`, `UM8` or `shearwater` registers;
* [`rsl_comm_py/rsl_xml_svd`](./rsl_comm_py/rsl_xml_svd) package stores `UM7`, `UM8`, and `shearwater` registers data in SVD (or **S**ystem **V**iew **D**escription) format and parsing code. For content description of the package, look at the [repo](https://github.com/RedshiftLabsPtyLtd/rsl_xml_svd);
* [`rsl_comm_py/test`](./rsl_comm_py/test)  [`pytest`](https://docs.pytest.org/en/latest/) tests for register map code generation;
* [`rsl_comm_py/rsl_generate_shearwater.py`](./rsl_comm_py/rsl_generate_shearwater.py): invoke `python` and `C/C++` code generation for `shearwater` and save generated results;
* [`rsl_comm_py/rsl_generate_um7.py`](./rsl_comm_py/rsl_generate_um7.py): invoke code generation for `UM7` and save generated results;
* [`rsl_comm_py/rsl_generator.py`](./rsl_comm_py/rsl_generator.py): code generation for [`um7_registers.py`](./rsl_comm_py/um7_registers.py) and [`shearwater_registers.py`](./rsl_comm_py/shearwater_registers.py) from the SVD file;
* [`rsl_comm_py/rsl_spi.py`](./rsl_comm_py/rsl_spi.py): generic SPI driver classes for [USB-ISS](https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm) or SPI-bus (Linux);
* [`rsl_comm_py/serve_um7_autodetect.py`](./rsl_comm_py/serve_um7_autodetect.py): copies the [`um7_autodetect.py`](./rsl_comm_py/um7_autodetect.py) script to the desired location;
* [`rsl_comm_py/um7_autodetect.py`](./rsl_comm_py/um7_autodetect.py): UM7 script for saving configuration for connection to the [USB Expansion Board](https://redshiftlabs.com.au/product/usb-expansion-board/);  
* [`rsl_comm_py/shearwater_broadcast_packets.py`](./rsl_comm_py/shearwater_broadcast_packets.py): [dataclasses](https://docs.python.org/3/library/dataclasses.html) for `shearwater` broadcast messages;
* [`rsl_comm_py/shearwater_registers.py`](./rsl_comm_py/shearwater_registers.py): `shearwater` register description file;
* [`rsl_comm_py/shearwater_serial.py`](./rsl_comm_py/shearwater_serial.py): `shearwater` UART driver;
* [`rsl_comm_py/shearwater_spi.py`](./rsl_comm_py/shearwater_spi.py): `shearwater` SPI driver for [USB-ISS](https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm) or SPI-bus (Linux);
* [`rsl_comm_py/um7_broadcast_packets.py`](./rsl_comm_py/um7_broadcast_packets.py): [dataclasses](https://docs.python.org/3/library/dataclasses.html) for `UM7` broadcast messages;
* [`rsl_comm_py/um7_registers.py`](./rsl_comm_py/um7_registers.py): `UM7` register description file;
* [`rsl_comm_py/um7_serial.py`](./rsl_comm_py/um7_serial.py): `UM7` UART driver;
* [`rsl_comm_py/um7_spi.py`](./rsl_comm_py/um7_spi.py): `UM7` SPI driver for [USB-ISS](https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm) or SPI-bus (Linux);


## HW Prerequisites

`UM7`, `UM8`, `shearwater` boards provide serial (UART) and SPI interfaces, hence the two main ways to access the sensor data
are UART (serial) or SPI. The differences in short: UART provides broadcast functionality, i.e.
when packets can transmitted by the board with a specified frequency (transmission frequencies are set up in 
configuration registers), and it is possible to issue sensor commands (i.e. accessing command registers).
SPI access the sensor register on demand (i.e. no broadcast functionality), and only
configuration and data registers can be accessed. Accessing commands is only supported
over UART.


### Serial connection (UART)

When using `UM7`, `UM8`, `shearwater` over serial, it is possible to connect to the target system (i.e. user's target):

* to the serial port directly (e.g. when serial pins are wired out as on the 
[Raspberry PI](https://www.raspberrypi.org/), 
[NVIDIA Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano-developer-kit), 
or other board computers with GPIO and UART pins wired out);

* to the USB port using the  [USB Expansion Board](https://redshiftlabs.com.au/product/usb-expansion-board/),
which performs USB to serial conversion.

### SPI connection

When using the `UM7`, `UM8`, `shearwater` over SPI, there are also a couple of possibilities:

* to the SPI pins directly (e.g. Raspberry PI, NVIDIA Jetson Nano), i.e.
the pins are wired to the [SoC](https://en.wikipedia.org/wiki/System_on_a_chip) directly;

* to the USB port using USB to SPI converter, e.g. [USB-ISS](https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm).

The difference between the two, that in the first case SoC pins support the SPI
directly (on the hardware level, which also mirrors in the OS level), then the OS is likely to have the SPI device
driver built-in (e.g. Raspberry PI). In the second case, using external converter (e.g. USB-ISS),
the device will be shown as a so-called [cdc_acm](https://www.keil.com/pack/doc/mw/USB/html/group__usbh__cdcacm_functions.html) (communication device class),
and low-level SPI communication will be done by the converter, yet to the OS the 
converter will be shown as Abstract Control Model (ACM) USB Device.

## Installation

```sh
pip install rsl-comm-py
```

## Python dependencies

**TL;DR:** install 
(i) `pyserial`, 
(ii) `pyudev` (for Linux),
(iii) `dataclasses` (included in standard library since `python3.7`, needs to be installed for `3.6`).

If you want to use SPI: if using on Linux and use SPI bus directly, install `spidev`,
otherwise if using USB-ISS install `usb_iss` python package.

Alternatively, one may use [`environment.yml`](./environment.yml)
to create conda environment with dependencies resolved.


## Python driver 101

The python driver for Redshift Labs Pty Ltd orientation sensors works as follows:
the `*.svd` file describes the register map, and the fields of registers.
From the `*.svd` file the `[sensor]_registers.py`
(e.g. `um7_registers.py` or `shearwater_registers.py`) is generated.
The files have generated methods for reading / writing single registers, 
and how to interpret the payload. In addition, the files
(e.g. `um7_registers.py` or `shearwater_registers.py`) provide
abstract methods `connect`, `read_register`, and `write_register`.

The `[sensor]_serial.py` files (e.g. `shearwater_serial.py` or `um7_serial.py`)
implement required functionality to read / write registers via the UART interface.
In addition to this the `[sensor]_serial.py` files also implement decoding of broadcast packets.
Connection to the UART might be done via 
[USB Expansion Board](https://redshiftlabs.com.au/product/usb-expansion-board/)
and for this the so-called `device` file might be used.
One can also connect to the port directly using the `port` argument.

The `[sensor]_spi.py` files (e.g. `shearwater_spi.py` or `um7_spi.py`)
implement required functionality to read / write registers via SPI interface.
In particularly two ways of connecting to SPI are supported:
either using [USB-ISS](https://www.robot-electronics.co.uk/htm/usb_iss_tech.htm)
adapter, and corresponding `usb_iss` library, or 
connecting to the SPI port directly, e.g. if Linux kernel have SPI functionality
activated, and the SPI interface is wired directly to the SoC (e.g. as for Raspberry PI).
This way the communication is done using the `spidev` python library.


## OS Prerequisites

1. When plugged in on a Linux system, 
the `UM7` sensor should appear 
as `/dev/ttyUSB*` device 
(this is only true when you are using
[USB Expansion Board](https://www.redshiftlabs.com.au/sensors/usb-expansion-board)
which in turn uses USB-to-serial [FTDI](https://www.ftdichip.com/)
chip.

2. Your Linux user must be a member of the
`dialout` group 
(e.g. see this [thread](https://unix.stackexchange.com/questions/14354/read-write-to-a-serial-port-without-root))
to be able to read/write `ttyUSB*` devices 
without root privileges.

3. `udev` is installed on the system.
We do autodetect the FTDI chip ID by relying on information from
`udev`.


## Device autodetect

To facilitate discovering `UM7` sensor among other
USB-to-serial devices (and store the configuration when 
re-plugging and/or adding other devices), we provide `um7_autodetect` method
and the `um7_autodetect.py` script (both are equivalent).

These methods create `um_[SERIAL_NUM].json` configuration file,
which is then used to match the USB-to-serial converter to which
the sensor is connected.

### Using `um7_autodetect` method

1. Launch `um7_autodetect` method:

```python
from um7py import um7_autodetect
um7_autodetect()
``` 

At this point, the `um7_[SERIAL_NUM].json` files is created 
in the current directory.

### Using `um7_autodetect.py` script

1. Obtain the `um7_autodetect.py` script from `um7py` package:

```python
from um7py import serve_autodetect_script
serve_autodetect_script()
``` 

2. Launch the script and follow instructions:

```sh
./um7_autodetect.py --help
```

At this point, the `um7_[SERIAL_NUM].json` files is created 
in the current directory.

**Important:** The created `um7_[SERIAL_NUM].json` configuration file 
should be used as a device file, when creating instance of
`UM7Communication` class:

```python
from um7py import ShearWaterSerial
shearwater_sensor = ShearWaterSerial(device='um7_[MY_SERIAL_NUM].json')
``` 


## Quick start

Read `shearwater` firmware build id:

```python
from um7py import ShearWaterSerial
shearwater = ShearWaterSerial(device='um7_A500CNHH.json')
print(f"get_fw_build_id : {shearwater.get_fw_build_id}")
```


## Maintainer

[Dr. Konstantin Selyunin](http://selyunin.com/), for
suggestions / questions / comments please contact: selyunin [dot] k [dot] v [at] gmail [dot] com