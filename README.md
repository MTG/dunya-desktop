# dunya-desktop
[![Build Status](https://travis-ci.org/MTG/dunya-desktop.svg?branch=master)](https://travis-ci.org/MTG/dunya-desktop) [![Code Climate](https://codeclimate.com/github/MTG/dunya-desktop/badges/gpa.svg)](https://codeclimate.com/github/MTG/dunya-desktop) [![codecov](https://codecov.io/gh/MTG/dunya-desktop/branch/master/graph/badge.svg)](https://codecov.io/gh/MTG/dunya-desktop) [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](http://www.gnu.org/licenses/agpl-3.0) [![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

**Dunya-desktop** is a desktop application, developed for accessing  and visualizing music data such as music scores, audio recordings, extracted features and analysis  results. It is a modular and extendable desktop application that the users can customise according to their needs.

![dunya-desktop-gif](https://github.com/MTG/dunya-desktop/blob/master/resources/dunya-desktop-demo.gif)

Dunya-desktop mainly uses [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5), Python bindings for [Qt5](https://www.qt.io/developers/) application framework, for the user interface design and [pycompmusic](https://github.com/MTG/pycompmusic) module for reaching the backend of the [Dunya](http://dunya.compmusic.upf.edu).

Installation
============
Installing dependencies on Mac OS X
-------

The given installation steps were tried on OS X El Capitan (v10.11.06) and OS X El Sierra (v10.12.1).

* Install [Homebrew package manager](http://brew.sh/):

        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
        
* Install Python 2.x, Qt5.7 and wget with Homebrew:
        
        brew install python qt@5.7 wget

* Install Xcode (can be installed via [Mac App Store](https://itunes.apple.com/en/app/xcode/id497799835?mt=12)).
Then install command-line tools:

        xcode-select --install
        sudo xcodebuild -license
    After the installation, make sure that you have agreed Apple's licence agreement.

* Download PyQt5.7.1 and SIP source packages:

        wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19/sip-4.19.tar.gz
        wget https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.7.1/PyQt5_gpl-5.7.1.tar.gz

* Untar and compile PyQt5.7.1 and SIP:
        
        # compile sip
        tar -xvf sip-4.19.tar.gz
        cd sip-4.19
        python configure.py -d /usr/local/lib/python2.7/site-packages/
        make
        sudo make install
        
        # compile PyQt5
        cd ..
        tar -xvf PyQt5_gpl-5.7.1.tar.gz
        cd PyQt5_gpl-5.7.1
        python configure.py --confirm-license -d /usr/local/lib/python2.7/site-packages/ --qmake=/usr/local/Cellar/qt\@5.7/5.7.1/bin/qmake --sip=../sip-4.19/sipgen/sip --sip-incdir=../sip-4.19/siplib
        make
        sudo make install

* __dunya-desktop__ uses some modules in Essentia. Follow the [instructions](essentia.upf.edu/documentation/installing.html) to install the library.


* Create a virtual environment (virtualenv) and install requirements.
        
        pip install virtualenv
        virtualenv --system-site-packages env
        source env/bin/activate
        
* Go to directory of where dunya-desktop is downloaded. 

    __IMPORTANT:__ Don't forget to change 'path/to/dunya-desktop' with the actual directory name.        
        
        cd path/to/dunya-desktop

* Finally, install the package requirements.

        pip install -r requirements

License
=======
The source code hosted in this repository is licenced under the terms of the GNU Affero General Public License (v3 or later). Any data (the audio recordings, music scores, features, figures, outputs etc.) are licenced under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

Contact
=========
Hasan Sercan Atlı	hsercanatli	AT	gmail	DOT	com

Acknowledgements
================
Dunya-desktop is partially supported by the European Research Council under the European Union’s Seventh Framework Program, as part of the CompMusic project (ERC grant agreement 267583).
