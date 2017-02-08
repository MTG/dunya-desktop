import sys
import os
import unittest

SOURCE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           '..', '..'))
sys.path.insert(0, SOURCE_PATH)

import numpy as np
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
        audio_file = mbid + '.mp3'
        audio_path = os.path.join(TESTDATA_PATH, audio_file)
        raw_audio, len_audio, min_audio, max_audio = read_raw_audio(audio_path)

        self.waveform.plot_waveform(raw_audio)
        self.max_length = np.size(raw_audio)
        self.duration = len_audio / self.waveform.samplerate


class WaveFormRegionTest(WaveformWidgetTest):
    def test_change_region_to_max(self):
        self.waveform.change_wf_region(self.duration + 10, self.duration + 20)
        x_min, x_max = self.waveform.get_waveform_region
        self.assertAlmostEqual(x_min, self.duration, 1)

    def test_change_region_to_min(self):
        self.waveform.change_wf_region(-25., -10.)
        x_min, x_max = self.waveform.get_waveform_region
        self.assertAlmostEqual(x_min, 0)


class WaveformVlineTest(WaveformWidgetTest):
    def test_change_cursor_min(self):
        self.waveform.update_wf_vline(-5000)
        pos = self.waveform.vline_wf.pos().x()
        self.assertAlmostEqual(pos, 0, 1)

    def test_change_cursor_max(self):
        self.waveform.update_wf_vline(self.max_length + 5000)
        pos = self.waveform.vline_wf.pos().x()
        self.assertAlmostEqual(pos, np.size(self.waveform.visible), 1)
