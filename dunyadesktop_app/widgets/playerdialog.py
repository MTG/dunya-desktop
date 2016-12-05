import tempfile
import os
import glob
import time
import json
import copy

from PyQt4 import QtGui, QtCore
from essentia.standard import MonoLoader
import numpy as np

from dunyadesktop_app.widgets.waveformwidget import WaveformWidget
from dunyadesktop_app.widgets.melodywidget import MelodyWidget
from dunyadesktop_app.widgets.playerframe import PlayerFrame
from dunyadesktop_app.utilities.playback import AudioPlaybackThread
import dunyadesktop_app.ui_files.resources_rc


DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')


def load_audio(audio_path):
    raw_audio = np.array(MonoLoader(filename=audio_path)())
    len_audio = len(raw_audio)
    min_audio = np.min(raw_audio)
    max_audio = np.min(raw_audio)
    return raw_audio, len_audio, min_audio, max_audio


def load_pitch(pitch_path):
    pitch_data = json.load(open(pitch_path))
    pp = np.array(pitch_data['pitch'])

    time_stamps = pp[:, 0]
    pitch_curve = pp[:, 1]
    pitch_plot = copy.copy(pitch_curve)
    pitch_plot[pitch_plot < 20] = np.nan

    samplerate = pitch_data['sampleRate']
    hopsize = pitch_data['hopSize']

    max_pitch = np.max(pitch_curve)
    min_pitch = np.min(pitch_curve)

    return time_stamps, pitch_plot, max_pitch, min_pitch, samplerate, hopsize


def load_pd(pd_path):
    pd = json.load(open(pd_path))
    vals = pd["vals"]
    bins = pd["bins"]
    return vals, bins


def get_paths(recid):
    doc_folder = os.path.join(DOCS_PATH, recid)
    audio_path = os.path.join(doc_folder, recid + '.mp3')
    pitch_path = os.path.join(doc_folder,
                              'audioanalysis--pitch_filtered.json')
    pd_path = os.path.join(doc_folder,
                           'audioanalysis--pitch_distribution.json')
    return doc_folder, audio_path, pitch_path, pd_path


class PlayerDialog(QtGui.QDialog):
    def __init__(self, recid):
        now = time.time()
        QtGui.QDialog.__init__(self)
        self._set_design()

        # paths
        doc_folder, audio_path, pitch_path, pd_path = get_paths(recid)

        # loading features and audio
        raw_audio, len_audio, min_audio, max_audio = load_audio(audio_path)
        time_stamps, pitch_plot, max_pitch, min_pitch, samplerate, hopsize = \
            load_pitch(pitch_path)
        vals, bins = load_pd(pd_path)

        # plotting features
        self.waveform_widget.plot_waveform(raw_audio, len_audio, min_audio,
                                           max_audio)
        self.melody_widget.plot_melody(time_stamps, pitch_plot, len_audio,
                                       samplerate, max_pitch)

        self.melody_widget.plot_histogram(vals, bins, max_pitch)
        print(time.time()-now)

        self.playback_thread = AudioPlaybackThread(timer_pitch=60,
                                                   timer_wf=250)
        self.playback_thread.playback.set_source(audio_path)
        #self._set_slider(len_audio)

        #self.playback_pos = 0
        #self.playback_pos_pyglet = 0

        #self.frame_player.toolbutton_pause.setDisabled(True)

        # signals
        #self.playback_thread.time_out_wf.connect(
        #    lambda: self.update_wf_pos(samplerate))
        self.playback_thread.time_out.connect(lambda:
                                              self.update_vlines(hopsize,
                                                                 samplerate,
                                                                 pitch_plot))

        self.waveform_widget.region_wf.sigRegionChangeFinished.connect(
            lambda: self.wf_region_changed(samplerate, hopsize))
        #self.waveform_widget.region_wf_hor.sigRegionChangeFinished.connect(
        #    lambda: self.wf_hor_region_changed(max_audio, min_audio,
        #                                       max_pitch))

        self.frame_player.toolbutton_play.clicked.connect(self.playback_play)
        self.frame_player.toolbutton_pause.clicked.connect(self.playback_pause)

    def closeEvent(self, QCloseEvent):
        self.waveform_widget.clear()
        self.melody_widget.clear()

    def update_wf_pos(self, samplerate):
        self.waveform_widget.vline_wf.setPos(
            [self.playback_pos * samplerate, 0])

    def _set_design(self):
        self.setWindowTitle('Player')
        self.resize(1050, 550)
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

    def wf_region_changed(self, samplerate, hopsize):
        pos_wf_x_min, pos_wf_x_max = self.waveform_widget.region_wf.getRegion()
        self.melody_widget.set_zoom_selection_area(pos_wf_x_min, pos_wf_x_max,
                                                   samplerate, hopsize)

    def wf_hor_region_changed(self, max_audio, min_audio, max_pitch):
        pos_wf_ymin, pos_wf_ymax = \
            self.waveform_widget.region_wf_hor.getRegion()
        step = (max_audio + abs(min_audio) / max_pitch)

        min_freq = abs(pos_wf_ymin - min_audio) / step
        max_freq = abs(pos_wf_ymax - min_audio) / step
        self.melody_widget.set_zoom_selection_area_hor(min_freq, max_freq)

    def playback_play(self):
        self.frame_player.toolbutton_play.setDisabled(True)
        self.frame_player.toolbutton_pause.setEnabled(True)
        self.playback_thread.start()

    def playback_pause(self):
        self.frame_player.toolbutton_play.setEnabled(True)
        self.frame_player.toolbutton_pause.setDisabled(True)
        self.playback_thread.pause()

    def _set_slider(self, len_audio):
        self.frame_player.slider.setMinimum(0)
        self.frame_player.slider.setMaximum(len_audio)
        self.frame_player.slider.setTickInterval(10)
        self.frame_player.slider.setSingleStep(1)

    def update_vlines(self, hopsize, samplerate, pitch):
        #if self.playback_thread.playback.is_playing():
            #if self.playback_pos_pyglet == \
            #        self.playback_thread.playback.get_pos_seconds():
            #    self.playback_pos += 0.05
            #else:
            #    self.playback_pos = \
            #        self.playback_thread.playback.get_pos_seconds()
            #    self.playback_pos_pyglet = \
            #        self.playback_thread.playback.get_pos_seconds()

        self.playback_pos = self.playback_thread.playback.get_pos_seconds()
        self.melody_widget.vline.setPos([self.playback_pos, 0])
        self.melody_widget.hline_histogram.setPos(
                pos=[0, pitch[np.int(self.playback_thread.playback.get_pos_sample()/ hopsize)]])
        #self.frame_player.slider.setValue(self.playback_pos * samplerate)

            #pos_vline = self.melody_widget.vline.pos()[0]
            #pos_xmin, pos_xmax = \
            #    self.melody_widget.zoom_selection.viewRange()[0]
            #dist = pos_xmax - pos_xmin

            #if pos_xmax * 0.98 <= pos_vline <= pos_xmax * 1.02:
            #    self.waveform_widget.region_wf.setRegion(
            #        [pos_xmax*samplerate+(hopsize/samplerate),
            #         (pos_xmax+dist)*samplerate])
            #    self.melody_widget.zoom_selection.setXRange(
            #        pos_xmax+(hopsize/samplerate), pos_xmax+dist, padding=0)


            #elif pos_vline < pos_xmin * 0.99 or pos_vline > pos_xmax:
            #    self.playback_pause()
            #    pos_xmin, pos_xmax = self.waveform_widget.region_wf.getRegion()
            #    pos = pos_xmin/samplerate

            #    self.playback_pos = pos
            #    self.playback_pos_pyglet = pos
            #    self.playback_thread.playback.seek(pos)

            #    self.waveform_widget.vline_wf.setPos(pos_xmin)
            #    self.melody_widget.vline.setPos(pos_xmin / samplerate)
            #    self.melody_widget.hline_histogram.setPos(
            #        pos=[0,
            #             pitch[int(self.playback_pos*samplerate/hopsize)]])
            #    self.frame_player.slider.setValue(pos_xmin)

            #    self.melody_widget.zoom_selection.setXRange(
            #        pos_xmin/samplerate, pos_xmax/samplerate, padding=0)
            #else:
            #pass
            # else for now playing option

