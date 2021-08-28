# Author: Dr. Konstantin Selyunin
# Date: 09 March 2021
# Version: v0.4
# Copyright (C) 2021 RedshiftLabs Pty Ltd. All rights reserved

# start from official ubuntu image
FROM ubuntu
# perform apt update
RUN apt-get update
# install wget for downloading files
# install curl for uploading build artifacts to the bitbucket cloud
RUN apt-get install wget curl make git -y
# installing pip3 gives python, c++, make, and others --> enough for our needs
RUN apt-get install python3.9 python3.9-dev zip -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN apt-get download python3-distutils
RUN dpkg-deb -x `realpath python3-distutils*.deb` /
RUN python3.9 get-pip.py
RUN pip install -U sphinx sphinx_rtd_theme jinja2 pytest pyserial
WORKDIR /code
