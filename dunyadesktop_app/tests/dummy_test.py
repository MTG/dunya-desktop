import os
import sys

SOURCE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, SOURCE_PATH)


import logging
import cultures.dunya.conn
import cultures.dunya.makam as makam

DUNYA_TOKEN = os.environ['DUNYA_TOKEN']
cultures.dunya.conn.set_token(DUNYA_TOKEN)

logging.basicConfig()  # removes
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_dunya_api():
    makams = makam.get_makams()
    logger.info(makams)
    assert makams
