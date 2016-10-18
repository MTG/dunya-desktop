import tempfile
import os
import glob
import time

from PyQt4 import QtGui, QtCore
from essentia.standard import MonoLoader

from dunyadesktop_app.widgets.waveformwidget import WaveformWidget
from dunyadesktop_app.widgets.melodywidget import MelodyWidget
from dunyadesktop_app.widgets.playerframe import PlayerFrame
from dunyadesktop_app.utilities.playback import AudioPlaybackThread
from dunyadesktop_app.utilities.timer import TimerThread
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
        self.hopsize = self.pitch_data['hopSize']
        self.sample_rate = self.pitch_data['sampleRate']
        self.raw_audio = MonoLoader(filename=self.audio_path)()
        self.waveform_widget.plot_waveform(self.raw_audio)
        self.time_stamps, self.pitch, self.salince = \
            self.melody_widget.plot_melody(self.pitch_data,
                                           len(self.raw_audio),
                                           self.sample_rate)
        self.melody_widget.plot_histogram(self.pd, self.pitch)
        self.playback_thread = AudioPlaybackThread()
        self.playback_thread.playback.set_source(self.audio_path)
        self._set_slider()

        self.timers = TimerThread()
        self.playback_pos = 0
        self.playback_pos_pyglet = 0
        self.frame_player.toolbutton_pause.setDisabled(True)

        # signals
        #self.timers.time_out_wf.connect(self.update_wf_pos)
        self.timers.time_out.connect(self._keep_position)
        self.timers.time_out.connect(self.update_vlines)
        self.waveform_widget.region_wf.sigRegionChangeFinished.connect(
            self.wf_region_changed)
        self.waveform_widget.region_wf_hor.sigRegionChangeFinished.connect(
            self.wf_hor_region_changed)
        self.frame_player.toolbutton_play.clicked.connect(self.playback_play)
        self.frame_player.toolbutton_pause.clicked.connect(self.playback_pause)

    def update_wf_pos(self):
        self.waveform_widget.vline_wf.setPos(
            [self.playback_pos * self.sample_rate, 0])

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

    def playback_play(self):
        self.frame_player.toolbutton_play.setDisabled(True)
        self.frame_player.toolbutton_pause.setEnabled(True)
        self.timers.start()
        self.playback_thread.start()

    def playback_pause(self):
        self.frame_player.toolbutton_play.setEnabled(True)
        self.frame_player.toolbutton_pause.setDisabled(True)
        self.playback_thread.stop()
        self.timers.stop()

    def _keep_position(self):
        if self.playback_pos_pyglet != self.playback_thread.playback.get_pos_seconds():
            self.playback_pos_pyglet = self.playback_thread.playback.get_pos_seconds()
            self.playback_pos = self.playback_thread.playback.get_pos_seconds()

    def _set_slider(self):
        self.frame_player.slider.setMinimum(0)
        self.frame_player.slider.setMaximum(len(self.raw_audio))
        self.frame_player.slider.setTickInterval(10)
        self.frame_player.slider.setSingleStep(1)

    def update_vlines(self):
        if self.playback_pos_pyglet == self.playback_thread.playback.get_pos_seconds():
            self.playback_pos += 0.02
        else:
            self.playback_pos = self.playback_pos_pyglet

        self.melody_widget.vline.setPos([self.playback_pos, 0])
        self.melody_widget.arrow.setPos(self.playback_pos, self.pitch
                  [int(self.playback_pos * self.sample_rate / self.hopsize)])

        self.melody_widget.hline_histogram.setPos(
            pos=[0, self.pitch[int(self.playback_pos * self.sample_rate / self.hopsize)]])
        self.frame_player.slider.setValue(self.playback_pos*self.sample_rate)
        # self.waveform_widget.vline_wf.setPos(
        # [self.playback_pos * self.sample_rate, 0])
