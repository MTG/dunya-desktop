#!/usr/bin/env bash

sudo add-apt-repository --yes ppa:ubuntu-sdk-team/ppa
sudo apt-get update -qq
sudo apt-get install -qq qtdeclarative5-dev libqt5webkit5-dev
export QMAKE=/usr/bin/qmake-qt5

PYQT_VERSION=5.7.1
SIP_VERSION=4.19

# Install sip
wget --retry-connrefused https://sourceforge.net/projects/pyqt/files/sip/sip-$SIP_VERSION/sip-$SIP_VERSION.tar.gz
tar -xzf sip-$SIP_VERSION.tar.gz
cd sip-$SIP_VERSION
python configure.py
make
sudo make install
cd ..

# Install PyQt5
wget --retry-connrefused https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-$PYQT_VERSION/PyQt5_gpl-$PYQT_VERSION.tar.gz
tar -xzf PyQt5_gpl-$PYQT_VERSION.tar.gz
cd PyQt5_gpl-$PYQT_VERSION
python configure.py --confirm-license --qmake=/usr/bin/qmake-qt5 -e QtCore -e QtGui -e QtWidgets -e QtTest -e QtOpenGL -e QtSvg
make
sudo make install

# test
python -c 'from PyQt5 import QtWidgets'
python -c 'from PyQt5 import QtCore'
python -c 'from PyQt5 import QtTest'
python -c 'from PyQt5 import QtGui'
python -c 'from PyQt5 import Qt'
python -c 'from PyQt5 import QtSvg'
