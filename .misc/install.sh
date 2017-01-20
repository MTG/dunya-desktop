#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install tar build-essential qt5-default qt5-qmake libqt5webkit5-dev

PYQT_VERSION=5.7.1
SIP_VERSION=4.19

# Install sip
wget --retry-connrefused https://sourceforge.net/projects/pyqt/files/sip/sip-$SIP_VERSION/sip-$SIP_VERSION.tar.gz
tar -xzvf sip-$SIP_VERSION.tar.gz
cd sip-$SIP_VERSION
python configure.py
make
sudo make install
cd ..

# Install PyQt5
wget --retry-connrefused https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-$PYQT_VERSION/PyQt5_gpl-$PYQT_VERSION.tar.gz
tar -xzvf PyQt5_gpl-$PYQT_VERSION.tar.gz
cd PyQt5_gpl-$PYQT_VERSION
python configure.py --confirm-license
make
sudo make install