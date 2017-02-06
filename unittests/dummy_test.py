import logging
import compmusic.dunya.conn
import compmusic.dunya.makam as makam
import os

DUNYA_TOKEN = os.environ['DUNYA_TOKEN']
compmusic.dunya.conn.set_token(DUNYA_TOKEN)

logging.basicConfig()  # removes
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_dunya_api():
    makams = makam.get_makams()
    print makams
    logger.info(makams)
    assert makams