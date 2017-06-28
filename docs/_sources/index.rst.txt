.. Dunya-desktop documentation master file, created by
   sphinx-quickstart on Tue May 30 14:27:44 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Dunya-desktop Documentation
===========================

.. image:: ../../dunyadesktop_app/ui_files/icons/dunya-desktop-github.png
    :target: https://github.com/MTG/dunya-desktop
    :scale: 60 %
    :align: center

.. compound::
    **Dunya-desktop** is a desktop application, developed for accessing and
    visualizing music data such as music scores, audio recordings, extracted
    features and analysis  results. It is a modular and extendable desktop
    application that the users can customise according to their needs.

.. image:: ../../resources/dunya-desktop-demo.gif
    :align: center

.. compound::
    Dunya-desktop mainly uses
    `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/download5>`_
    Python bindings for `Qt5 <https://www.qt.io/developers/>`_ application
    framework, for the user interface design and
    `pycompmusic <https://github.com/MTG/pycompmusic>`_
    module for reaching the backend of the
    `Dunya-web <http://dunya.compmusic.upf.edu>`_.

.. toctree::
    :maxdepth: 2
    :caption: Contents:


------------------------------------------------------------------------------


Installation
============

The code is compatible with Python 2.7+ and Python 3. We highly recommend you
to use the code with Python 3 and with a virtual environment.

------------------------------------------------------------------------------

Installing dependencies on MacOS
--------------------------------
The given installation steps were tried on OS El Capitan (v10.11.06) and OS El
Sierra (v10.12.1).

* Install Xcode (can be installed via `Mac App Store <https://itunes.apple.com/en/app/xcode/id497799835?mt=12>`_. Then install command-line tools:

    .. code-block:: bash

        xcode-select --install
        sudo xcodebuild -license

    After the installation, make sure that you have agreed Apple's licence agreement.

* Install `Homebrew package manager <http://brew.sh/>`_:

    .. code-block:: bash

        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

------------------------------------------------------------------------------

On Mac OS for Python 3.6
~~~~~~~~~~~~~~~~~~~~~~~~

* Install Python 3.6+, Qt 5.7 and wget with Homebrew:

    .. code-block:: bash

        brew install python3 qt@5.7 ffmpeg wget

* Create a virtual environment (virtualenv) and install requirements.

    .. code-block:: bash

        pyvenv env
        source env/bin/activate

* Go to directory of where dunya-desktop is downloaded.

    **IMPORTANT:** Don't forget to change 'path/to/dunya-desktop' with the
        actual directory name.

    .. code-block:: bash

        cd path/to/dunya-desktop

    * Finally, install the package requirements.

    .. code-block:: bash

        pip3 install -r requirements
        pip3 install PyQt5


------------------------------------------------------------------------------


On Mac OS for Python 2.7
~~~~~~~~~~~~~~~~~~~~~~~~

* Install Python 2.x, Qt 5.7, ffmpeg and wget with Homebrew:

    .. code-block:: bash

        brew install python qt@5.7 ffmpeg wget

* Download PyQt 5.7.1 and SIP source packages:

    .. code-block:: bash

        wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19/sip-4.19.tar.gz
        wget https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.7.1/PyQt5_gpl-5.7.1.tar.gz

* Untar and compile PyQt 5.7.1 and SIP:

    .. code-block:: bash

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

    .. code-block:: bash

        pip install virtualenv
        virtualenv --system-site-packages env
        source env/bin/activate

* Go to directory of where dunya-desktop is downloaded.

    **IMPORTANT:** Don't forget to change 'path/to/dunya-desktop' with the
    actual directory name.

    .. code-block:: bash

        cd path/to/dunya-desktop

* Finally, install the package requirements.

    .. code-block:: bash

        pip install -r requirements


------------------------------------------------------------------------------

Installing dependencies on Ubuntu 16.04
---------------------------------------

The given installation steps were tried on Ubuntu 16.04.02 LTS (xenial).

* Install Qt 5.x and ffmpeg:

    .. code-block:: bash

        sudo add-apt-repository --yes ppa:ubuntu-sdk-team/ppa
        sudo apt-get update -qq
        sudo apt-get install -qq qtdeclarative5-dev libqt5svg5-dev qtmultimedia5-dev build-essential
        sudo apt-get install -qq ffmpeg
        export QMAKE=/usr/lib/x86_64-linux-gnu/qt5/bin/qmake


------------------------------------------------------------------------------

On Ubuntu for Python 3.6
~~~~~~~~~~~~~~~~~~~~~~~~

* Install Python 3.6

    .. code-block:: bash

        sudo apt-get install -qq python3-dev

* Create a virtual environment (virtualenv) and install requirements.

    .. code-block:: bash

        pyvenv env
        source env/bin/activate

* Go to directory of where dunya-desktop is downloaded.

    **IMPORTANT:** Don't forget to change 'path/to/dunya-desktop' with the actual directory name.

    .. code-block:: bash

        cd path/to/dunya-desktop


* Finally, install the package requirements.

    .. code-block:: bash

        pip3 install -r requirements
        pip3 install PyQt5

------------------------------------------------------------------------------

On Ubuntu for Python 2.7
~~~~~~~~~~~~~~~~~~~~~~~~
* Install Python 2.x

    .. code-block:: bash

        sudo apt-get install -qq python-dev


* Download PyQt 5.8 and SIP source packages:

    .. code-block:: bash

        wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.1/sip-4.19.1.tar.gz
        wget https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.8/PyQt5_gpl-5.8.tar.gz

* Untar and compile PyQt 5.8 and SIP:

    .. code-block:: bash

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

    .. code-block:: bash

        pip install virtualenv
        virtualenv --system-site-packages env
        source env/bin/activate

* Go to directory of where dunya-desktop is downloaded.

    **IMPORTANT:** Don't forget to change 'path/to/dunya-desktop' with the
    actual directory name.

    .. code-block:: bash

        cd path/to/dunya-desktop

* Finally, install the package requirements.

    .. code-block:: bash

        pip install -r requirements


------------------------------------------------------------------------------

Annotated Screenshots of The Software
=====================================

Main Window
-----------

.. image:: ../../resources/dunya-desktop-main-annotated.png
    :align: center

------------------------------------------------------------------------------

Collection Dialog
-----------------

.. image:: ../../resources/dunya-desktop-coll-dialog.png
    :align: center

------------------------------------------------------------------------------

Player Main Window
------------------

.. image:: ../../resources/dunya-desktop-playermain.png
    :align: center

------------------------------------------------------------------------------

Histogram Dialog
----------------

.. image:: ../../resources/dunya-desktop-histogram.png
    :align: center

------------------------------------------------------------------------------

Score Dialog
------------

.. image:: ../../resources/dunya-desktop-scoredialog.png
    :align: center

------------------------------------------------------------------------------


Metadata Dialog
---------------

.. image:: ../../resources/dunya-desktop-metadata.png
    :align: center

------------------------------------------------------------------------------

Main UI
-------
.. automodule:: mainui_makam
    :members:

------------------------------------------------------------------------------

Widgets
-------

Combobox
~~~~~~~~
.. automodule:: widgets.combobox
    :members:

------------------------------------------------------------------------------

Player Frame
~~~~~~~~~~~~
.. automodule:: widgets.playerframe
.. autoclass:: PlayerFrame
    :members:

------------------------------------------------------------------------------

Tab Widget
~~~~~~~~~~
.. automodule:: widgets.tabwidget
.. autoclass:: TabWidget
    :members:

------------------------------------------------------------------------------

Time Series Widget
~~~~~~~~~~~~~~~~~~
.. automodule:: widgets.timeserieswidget
.. autoclass:: TimeSeriesWidget
    :members:

------------------------------------------------------------------------------

Waveform Widget
~~~~~~~~~~~~~~~
.. automodule:: widgets.waveformwidget
.. autoclass:: WaveformWidget
    :members:

------------------------------------------------------------------------------

Widget Utilities
~~~~~~~~~~~~~~~~
.. automodule:: widgets.widgetutilities
   :members:

------------------------------------------------------------------------------



Extensions
----------
Adaptive Synthesis for SymbTr Score Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


License
=======
The source code hosted in this repository is licenced under the terms of the
GNU Affero General Public License (v3 or later). Any data (the audio
recordings, music scores, features, figures, outputs etc.) are licenced under
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.


Acknowledgements
================
Dunya-desktop is supported by the European Research Council under the European
Union’s Seventh Framework Program, as part of the CompMusic project (ERC grant
agreement 267583).


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
