import logging
logger = logging.getLogger("dunya")
logger.setLevel(logging.INFO)

from .conn import set_hostname, set_token, HTTPError
from .docserver import *
from . import carnatic
from . import hindustani
from . import makam
