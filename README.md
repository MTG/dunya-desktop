<p align="center">
    <img src="https://github.com/MTG/dunya-desktop/blob/master/dunyadesktop_app/ui_files/icons/dunya-desktop-github.png" width="200">
</p>

<p align="center">
    <a target="_blank" href='https://travis-ci.org/MTG/dunya-desktop'>
		<img alt="travis" src="https://travis-ci.org/MTG/dunya-desktop.svg?branch=master"/>
	</a>
	<a target="_blank" href='https://codeclimate.com/github/MTG/dunya-desktop'>
		<img alt="code-climate" src="https://codeclimate.com/github/MTG/dunya-desktop/badges/gpa.svg"/>
	</a>
	<a target="_blank" href='https://codecov.io/gh/MTG/dunya-desktop'>
		<img alt="codecov" src="https://codecov.io/gh/MTG/dunya-desktop/branch/master/graph/badge.svg"/>
	</a>
	<a target="_blank" href='https://www.gnu.org/licenses/agpl-3.0.html'>
		<img alt="AGPL" src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg"/>
	</a>
	<a target="_blank" href='https://creativecommons.org/licenses/by-nc/4.0/legalcode'>
		<img alt="CCBYNC" src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg"/>
	</a>
</p>

**Dunya-desktop** is a desktop application, developed for accessing  and visualizing music data such as music scores, audio recordings, extracted features and analysis  results. It is a modular and extendable desktop application that the users can customise according to their needs.

<p align="center">
    <img src="https://github.com/MTG/dunya-desktop/blob/master/resources/dunya-desktop-demo.gif">
</p>

Dunya-desktop mainly uses [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5), Python bindings for [Qt5](https://www.qt.io/developers/) application framework, for the user interface design and [pycompmusic](https://github.com/MTG/pycompmusic) module for reaching the backend of the [Dunya](http://dunya.compmusic.upf.edu).

Running
=======

First, ensure that you have installed the relevant dependencies (see the
Installation section below).

To configure Dunya-desktop, copy the file `dunyadesktop_app/cultures/config.cfg.in` to `dunyadesktop_app/cultures/config.cfg`, for example:

    cp dunyadesktop_app/cultures/config.cfg.in dunyadesktop_app/cultures/config.cfg

Edit this file and replace the value `DUNYA_TOKEN` with your Dunya access token.
You can retrieve this token after signing in to the Dunya website and visiting
https://dunya.compmusic.upf.edu/user/profile/

Run Dunya-desktop by executing in the main directory:

    ./dunya-desktop


Installation
============
The code is compatible with Python 2.7+ and Python 3. We highly recommend you
to use the code with Python 3 and with a virtual environment.


Installing dependencies on Mac OS
---------------------------------

The given installation steps were tried on OS X El Capitan (v10.11.06) and OS X
El Sierra (v10.12.1).

* Install Xcode (can be installed via [Mac App Store](https://itunes.apple.com/en/app/xcode/id497799835?mt=12)).
Then install command-line tools:

        xcode-select --install
        sudo xcodebuild -license

    After the installation, make sure that you have agreed Apple's licence agreement.

* Install [Homebrew package manager](http://brew.sh/):

        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"


### On Mac OS for Python 3.6

* Install Python 3.6+, Qt 5.7 and wget with Homebrew:

        brew install python3 qt@5.7 ffmpeg wget

* Create a virtual environment (virtualenv) and install requirements.

        pyvenv env
        source env/bin/activate

* Go to directory of where dunya-desktop is downloaded.

    __IMPORTANT:__ Don't forget to change 'path/to/dunya-desktop' with the actual directory name.

        cd path/to/dunya-desktop

* Finally, install the package requirements.

        pip3 install -r requirements
        pip3 install PyQt5


### On Mac OS for Python 2.7

* Install Python 2.x, Qt 5.7 and wget with Homebrew:

        brew install python qt@5.7 ffmpeg wget

* Download PyQt 5.7.1 and SIP source packages:

        wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19/sip-4.19.tar.gz
        wget https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.7.1/PyQt5_gpl-5.7.1.tar.gz

* Untar and compile PyQt 5.7.1 and SIP:

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

* Create a virtual environment (virtualenv) and install requirements.

        pip install virtualenv
        virtualenv --system-site-packages env
        source env/bin/activate

* Go to directory of where dunya-desktop is downloaded.

    __IMPORTANT:__ Don't forget to change 'path/to/dunya-desktop' with the actual directory name.

        cd path/to/dunya-desktop

* Finally, install the package requirements.

        pip install -r requirements


Installing dependencies on Ubuntu 16.04
---------------------------------------

The given installation steps were tried on Ubuntu 16.04.02 LTS (xenial).

* Install Qt 5.x and ffmpeg:

        sudo add-apt-repository --yes ppa:ubuntu-sdk-team/ppa
        sudo apt-get update -qq
        sudo apt-get install -qq qtdeclarative5-dev libqt5svg5-dev qtmultimedia5-dev build-essential
        sudo apt-get install -qq ffmpeg
        export QMAKE=/usr/lib/x86_64-linux-gnu/qt5/bin/qmake


### On Ubuntu for Python 3.6

* Install Python 3.6

        sudo apt-get install -qq python3-dev

* Create a virtual environment (virtualenv) and install requirements.

        pyvenv env
        source env/bin/activate

* Go to directory of where dunya-desktop is downloaded.

    __IMPORTANT:__ Don't forget to change 'path/to/dunya-desktop' with the actual directory name.

        cd path/to/dunya-desktop

* Finally, install the package requirements.

        pip3 install -r requirements
        pip3 install PyQt5


### On Ubuntu for Python 2.7

* Install Python 2.x

        sudo apt-get install -qq python-dev

* Download PyQt 5.8 and SIP source packages:

        wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.1/sip-4.19.1.tar.gz
        wget https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.8/PyQt5_gpl-5.8.tar.gz

* Untar and compile PyQt 5.8 and SIP:

        # compile sip
        tar -xzf sip-4.19.1.tar.gz
        cd sip-4.19.1/
        python configure.py
        make
        sudo make install
        cd ..

        # compile PyQt5
        tar -xzf PyQt5_gpl-5.8.tar.gz
        cd PyQt5_gpl-5.8/
        python configure.py --confirm-license --qmake=/usr/lib/x86_64-linux-gnu/qt5/bin/qmake
        make
        sudo make install

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
Dunya-desktop is supported by the European Research Council under the European Union’s Seventh Framework Program, as part of the CompMusic project (ERC grant agreement 267583).
