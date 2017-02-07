# dunya-desktop
[![Build Status](https://travis-ci.org/MTG/dunya-desktop.svg?branch=master)](https://travis-ci.org/MTG/dunya-desktop) [![Code Climate](https://codeclimate.com/github/MTG/dunya-desktop/badges/gpa.svg)](https://codeclimate.com/github/MTG/dunya-desktop) [![codecov](https://codecov.io/gh/MTG/dunya-desktop/branch/master/graph/badge.svg)](https://codecov.io/gh/MTG/dunya-desktop)


**Dunya-desktop** is a desktop application that has been developed for accessing 
and visualizing the music information sources, the features and the analysis 
results that are part of the [CompMusic](http://compmusic.upf.edu) Project. 
It is a modular and extensive desktop application that the users can customise 
according to their needs.

Dunya-desktop mainly uses [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5), 
python bindings for [Qt5](https://www.qt.io/developers/) application framework, 
for the user interface design and [pycompmusic](https://github.com/MTG/pycompmusic) 
module for reaching the backend of the [Dunya](http://dunya.compmusic.upf.edu).


Installation
============
Installing dependencies on Mac OS X
-------
* Install [Homebrew package manager](http://brew.sh/).

        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
        
* Install Python 2.x, Qt5 and wget with Homebrew.
        
        brew install python qt5 wget

* Install Xcode (can be installed via [Mac App Store](https://itunes.apple.com/en/app/xcode/id497799835?mt=12)).
Then install command-line tools.

        xcode-select --install
        sudo xcodebuild -license
    After the installation, make sure that you have agreed Apple's licence agreement.

* Download PyQt5 and sip source.

        wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19/sip-4.19.tar.gz
        wget https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.7.1/PyQt5_gpl-5.7.1.tar.gz

* Untar and compile.

        tar -xvf sip-4.19.tar.gz
        cd sip-4.19
        python configure.py -d /usr/local/lib/python2.7/site-packages/
        make
        sudo make install
        
        cd ..
        tar -xvf PyQt-gpl-5.7.1.tar.gz
        cd PyQt-gpl-5.7.1
        python configure.py -d /usr/local/lib/python2.7/site-packages/ --qmake=/usr/local/Cellar/qt5/5.7.1_1/bin/qmake --sip=../sip-4.19/sipgen/sip --sip-incdir=../sip-4.19/siplib
        make
        sudo make install

* Create a virtualenv and install requirements.
        
        pip install virtualenv
        virtualenv --system-site-packages env
        source env/bin/activate
        pip install -r requirements
        

License
=======
The source code hosted in this repository is licenced under the terms of the 
GNU Affero General Public License (v3 or later). Any data (the audio recordings, 
music scores, features, figures, outputs etc.) are licenced under Creative 
Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
