import tempfile
import os
import glob

from PyQt4 import QtGui, QtCore
from essentia.standard import MonoLoader

from dunyadesktop_app.widgets.waveformwidget import WaveformWidget
from dunyadesktop_app.widgets.melodywidget import MelodyWidget
from dunyadesktop_app.widgets.playerframe import PlayerFrame
import dunyadesktop_app.ui_files.resources_rc


class PlayerDialog(QtGui.QDialog):
    def __init__(self, recid, pitch_data, pd):
        QtGui.QDialog.__init__(self)
        self._set_design()

        self.recid = recid
        self.rec_folder = os.path.join(tempfile.gettempdir(), self.recid)
        self.audio_path = glob.glob(self.rec_folder + '/*.mp3')[0]
        self.pitch_data = pitch_data
        self.pd = pd

        self.sample_rate = self.pitch_data['sampleRate']

        self.raw_audio = MonoLoader(filename=self.audio_path)()
        self.waveform_widget.plot_waveform(self.raw_audio)
        self.time_stamps, self.pitch, self.salince = \
            self.melody_widget.plot_melody(self.pitch_data, self.pd,
                                       len(self.raw_audio), self.sample_rate)

        # signals
        self.waveform_widget.region_wf.sigRegionChangeFinished.connect(
            self.wf_region_changed)
        self.waveform_widget.region_wf_hor.sigRegionChangeFinished.connect(
            self.wf_hor_region_changed)

    def _set_design(self):
        self.setWindowTitle('Player')
        self.resize(850, 550)
        self.setMinimumSize(QtCore.QSize(850, 500))
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.verticalLayout = QtGui.QVBoxLayout(self)

        self.waveform_widget = WaveformWidget()
        self.verticalLayout.addWidget(self.waveform_widget)

        self.melody_widget = MelodyWidget()
        self.verticalLayout.addWidget(self.melody_widget)

        self.frame_player = PlayerFrame(self)
        self.verticalLayout.addWidget(self.frame_player)
        QtCore.QMetaObject.connectSlotsByName(self)

    def wf_region_changed(self):
        pos_wf_x_min, pos_wf_x_max = self.waveform_widget.region_wf.getRegion()
        self.melody_widget.set_zoom_selection_area(pos_wf_x_min, pos_wf_x_max,
                                                   self.sample_rate)

    def wf_hor_region_changed(self):
        pos_wf_ymin, pos_wf_ymax = self.waveform_widget.region_wf_hor.getRegion()
        step = (max(self.raw_audio) + abs(min(self.raw_audio))) / max(self.pitch)

        min_freq = abs(pos_wf_ymin-min(self.raw_audio)) / step
        max_freq = abs(pos_wf_ymax-min(self.raw_audio)) / step
        self.melody_widget.set_zoom_selection_area_hor(min_freq, max_freq)
