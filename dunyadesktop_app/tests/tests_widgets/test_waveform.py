import sys
import os
import unittest

SOURCE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           '..', '..'))
sys.path.insert(0, SOURCE_PATH)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest

from cultures.makam.featureparsers import read_raw_audio
from widgets.waveformwidget import WaveformWidget

mbid = 'f970f1e0-0be9-4914-8302-709a0eac088e'
TESTDATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'test_data', mbid))

app = QApplication(sys.argv)


class WaveformWidgetTest(unittest.TestCase):
    def setUp(self):
        self.waveform = WaveformWidget()

    def test_defaults(self):
        audio_file = mbid + '.mp3'
        audio_path = os.path.join(TESTDATA_PATH, audio_file)
        raw_audio, len_audio, min_audio, max_audio = read_raw_audio(audio_path)

        self.waveform.plot_waveform(raw_audio)
