import compmusic.dunya.conn
import compmusic.dunya.makam as makam

compmusic.dunya.conn.set_token('asdadasdsa')


def test_dunya_api():
    makams = makam.get_makams()
    assert makams