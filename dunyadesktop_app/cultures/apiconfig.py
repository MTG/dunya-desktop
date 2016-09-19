from __future__ import absolute_import
import os.path
import ConfigParser

import compmusic.dunya.makam


def set_token():
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.cfg'))
    DUNYA_TOKEN = config.get('dunya', 'token')

    compmusic.dunya.conn.set_token(DUNYA_TOKEN)


def set_hostname():
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.cfg'))
    DUNYA_HOSTNAME = config.get('dunya', 'hostname')

    compmusic.dunya.conn.set_hostname(DUNYA_HOSTNAME)
