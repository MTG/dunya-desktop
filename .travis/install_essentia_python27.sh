#!/usr/bin/env bash

sudo apt-get install build-essential libyaml-dev libfftw3-dev libavcodec-dev libavformat-dev libavutil-dev libavresample-dev python-dev libsamplerate0-dev libtag1-dev
sudo apt-get install python-numpy-dev python-numpy python-yaml

wget https://github.com/MTG/essentia/archive/v2.1_beta2.tar.gz

tar -xzf v2.1_beta2.tar.gz
cd essentia-2.1_beta2
./waf configure --mode=release --with-python
./waf
sudo ./waf install

python -c 'import essentia'
