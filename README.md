# RSL Comm Python Driver

[![PyPI version](https://badge.fury.io/py/rsl_comm_py.svg)](https://badge.fury.io/py/rsl_comm_py)
![test and package](https://github.com/RedshiftLabsPtyLtd/rsl_comm_py/workflows/test%20and%20package/badge.svg)


**TL;DR:** *"Swiss army knife"* for using 
the [`UM7`](https://redshiftlabs.com.au/product/um7-orientation-sensor/), `UM8`,
and  `shearwater` orientation sensors with Python 3 (Python 3.7+).


Given `UM7`, `UM8`, and/or `shearwater` orientation sensor,
an optional 
[USB Expansion Board](https://redshiftlabs.com.au/product/usb-expansion-board/), 
this repo provides you with `python 3` driver,
which allows communicating with the orientation sensors
from Redshift Labs Pty Ltd under Linux
(Ubuntu, Raspbian, Suse, Yocto, etc.), and
Windows. 
Mac will be also supported in future (in fact it should work on Mac, 
but this is not tested yet).

The driver has the following capabilities: 

* read / write single `UM7`, `UM8`, `shearwater` registers over `SPI`;

* read / write single `UM7`, `UM8`, `shearwater` registers over `UART`;

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

After syncing the sub-modules, the `rsl_xml_svd` folder should appear inside
the repo, pointing exactly to the commit specified in this repository.


## Repository structure

High-level overview of folders and files in the repo:

* [`examples`](rsl_comm_py/examples) package with example code for receiving broadcast / reading / writing `shearwater` or `UM7` registers;
* [`rsl_xml_svd`](rsl_comm_py/rsl_xml_svd) package that stores `UM7` and `shearwater` registers data in SVD (or **S**ystem **V**iew **D**escription) format and parsing code. For content description of the package, look at the [repo](https://bitbucket.org/kselyunin/rsl_xml_svd/src/master/);
* [`test`](rsl_comm_py/test)  [`pytest`](https://docs.pytest.org/en/latest/) tests for register map code generation;
* [`rsl_comm_py`](rsl_comm_py/rsl_comm_py) top-level python package:
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


## Supported Python versions

**python v3.7+**

You are advised to use `python3.7+` if you are free to select the version,
the reason for this that the dataclasses are part of `3.7` standard library.
There exist a back-port of `dataclasses` package back to `3.6`, so it is also possible
to use `3.6` if needed.

## Python dependencies

**TL;DR:** install 
(i) `pyserial`, 
(ii) `pyudev`,
or use 
[`environment.yml`](./environment.yml)
to create conda environment
with dependencies resolved.

For further details regarding creating `conda` environment 
read [**this**](./CONDA_HOWTO.md) guide.

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