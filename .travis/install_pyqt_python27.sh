#!/usr/bin/env bash

PYQT_VERSION=5.7.1
SIP_VERSION=4.19

# Install sip and PyQt5 for Python 2.7
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
python configure.py --confirm-license --qmake=/usr/lib/x86_64-linux-gnu/qt5/bin/qmake
make
sudo make install

# test
python -c 'from PyQt5 import QtWidgets'
python -c 'from PyQt5 import QtCore'
python -c 'from PyQt5 import QtTest'
python -c 'from PyQt5 import QtGui'
python -c 'from PyQt5 import Qt'
python -c 'from PyQt5 import QtSvg'
python -c 'from PyQt5 import QtMultimedia'
