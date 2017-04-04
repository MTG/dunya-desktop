import sys
import os.path

if sys.version_info[0] == 2:
    import ConfigParser as configparser
else:
    import configparser

import cultures.dunya.conn


def _get_option(option):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.cfg'))
    return config.get('dunya', option)


def set_token():
    DUNYA_TOKEN = _get_option('token')
    cultures.dunya.conn.set_token(DUNYA_TOKEN)


def set_hostname():
    DUNYA_HOSTNAME = _get_option('hostname')
    cultures.dunya.conn.set_hostname(DUNYA_HOSTNAME)
