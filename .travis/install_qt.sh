#!/usr/bin/env bash

# Install Qt
sudo add-apt-repository --yes ppa:ubuntu-sdk-team/ppa
sudo apt-get update -qq
sudo apt-get install -qq qtdeclarative5-dev libqt5svg5-dev qtmultimedia5-dev
export QMAKE=/usr/lib/x86_64-linux-gnu/qt5/bin/qmake
