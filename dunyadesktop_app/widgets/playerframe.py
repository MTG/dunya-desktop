import os
import json
import copy

from PyQt5.QtWidgets import QVBoxLayout, QFrame
from PyQt5.QtCore import QSize, QMetaObject, QTimer
from essentia.standard import MonoLoader
import pyqtgraph.dockarea as pgdock
import numpy as np
from pyqtgraph.ptime import time

from waveformwidget import WaveformWidget
from melodywidget import MelodyWidget
from playbackframe import PlaybackFrame
from utilities.playback import Player
from cultures.makam import utilities
import ui_files.resources_rc


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
    full_names, folders, names = utilities.get_filenames_in_dir(
        dir_name=doc_folder, keyword='*.json')

    paths = {}
    paths['audio_path'] = os.path.join(doc_folder, recid + '.mp3')
    for xx, name in enumerate(names):
        paths[name.split('.json')[0]] = full_names[xx]
    return paths


class PlayerFrame(QFrame):
    fps = None
    last_time = time()

    def __init__(self, recid, parent=None):
        QFrame.__init__(self, parent=parent)
        self._set_design()
        # paths
        self.paths = get_paths(recid)

        # loading features and audio
        self.raw_audio, len_audio, min_audio, max_audio = \
            load_audio(self.paths['audio_path'])
        (time_stamps, self.pitch_plot, max_pitch, min_pitch,
         self.samplerate, self.hopsize) = load_pitch(
            self.paths['audioanalysis--pitch_filtered'])
        vals, bins = \
            load_pd(self.paths['audioanalysis--pitch_distribution'])

        # plotting features
        self.waveform_widget.plot_waveform(self.raw_audio, len_audio,
                                           min_audio, max_audio)
        self.melody_widget.plot_melody(time_stamps, self.pitch_plot, len_audio,
                                       self.samplerate, max_pitch)
        self.melody_widget.plot_histogram(vals, bins, max_pitch)

        # slider and playback thread
        self.playback = Player()
        self.playback.set_source(self.paths['audio_path'])
        self._set_slider(len_audio)

        self.frame_player.toolbutton_pause.setDisabled(True)

        self.playback_pos = 0.
        self.timer = QTimer()
        self.timer.setInterval(50)

        self.playback.player.positionChanged.connect(self.update_vlines)
        self.waveform_widget.region_wf.sigRegionChangeFinished.connect(
            self.wf_region_changed)
        self.frame_player.toolbutton_play.clicked.connect(self.playback_play)
        self.frame_player.toolbutton_pause.clicked.connect(self.playback_pause)

    def closeEvent(self, QCloseEvent):
        self.waveform_widget.clear()
        self.melody_widget.clear()
        self.playback.pause()

    def update_wf_pos(self, samplerate):
        self.waveform_widget.vline_wf.setPos(
            [self.playback_pos * samplerate, 0])

    def _set_design(self):
        self.setWindowTitle('Player')
        self.resize(1200, 550)
        self.setMinimumSize(QSize(850, 500))
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.verticalLayout = QVBoxLayout(self)

        area = pgdock.DockArea()
        d1 = pgdock.Dock("Waveform", area='Top', closable=False,
                         autoOrientation=False)
        #d1.setMinimumHeight(150)
        # d1.allowedAreas = ['top']
        self.waveform_widget = WaveformWidget()
        #self.waveform_widget.setMinimumHeight(100)

        d1.addWidget(self.waveform_widget)
        area.addDock(d1, 'top')

        d2 = pgdock.Dock('Pitch')
        self.melody_widget = MelodyWidget()
        d2.addWidget(self.melody_widget)
        area.addDock(d2, 'bottom')

        # self.verticalLayout.addWidget(self.waveform_widget)

        # self.melody_widget = MelodyWidget()
        # self.verticalLayout.addWidget(self.melody_widget)

        self.frame_player = PlaybackFrame(self)
        self.verticalLayout.addWidget(self.frame_player)
        self.verticalLayout.addWidget(area)
        QMetaObject.connectSlotsByName(self)

    def playback_play(self):
        self.frame_player.toolbutton_play.setDisabled(True)
        self.frame_player.toolbutton_pause.setEnabled(True)
        self.playback.play()

    def playback_pause(self):
        self.frame_player.toolbutton_play.setEnabled(True)
        self.frame_player.toolbutton_pause.setDisabled(True)
        self.playback.pause()

    def _set_slider(self, len_audio):
        self.frame_player.slider.setMinimum(0)
        self.frame_player.slider.setMaximum(len_audio)
        self.frame_player.slider.setTickInterval(10)
        self.frame_player.slider.setSingleStep(1)

    def wf_region_changed(self):
        pos_wf_x_min, pos_wf_x_max = self.waveform_widget.region_wf.getRegion()

        ratio = len(self.raw_audio) / len(self.waveform_widget.visible)
        x_min = (pos_wf_x_min * ratio) / self.samplerate
        x_max = (pos_wf_x_max * ratio) / self.samplerate
        self.melody_widget.updateHDF5Plot(x_min, x_max)
        #self.melody_widget.set_zoom_selection_area(pos_wf_x_min * ratio,
        #                                           pos_wf_x_max * ratio,
        #                                           self.samplerate,
        #                                           self.hopsize)

    def update_vlines(self, playback_pos):
        # print(playback_pos)
        # if self.playback_thread.playback.is_playing():
        # if self.playback_pos_pyglet == \
        #        self.playback_thread.playback.get_pos_seconds():
        #    self.playback_pos += 0.05
        # else:
        #    self.playback_pos = \
        #        self.playback_thread.playback.get_pos_seconds()
        #    self.playback_pos_pyglet = \
        #        self.playback_thread.playback.get_pos_seconds()

        # self.playback_pos = self.playback_thread.playback.get_pos_seconds()
        ratio = len(self.raw_audio) / len(self.waveform_widget.visible)
        playback_pos_sec = playback_pos / 1000.
        playback_pos_sample = playback_pos_sec * self.samplerate
        self.melody_widget.vline.setPos([playback_pos_sec, 0])
        self.melody_widget.hline_histogram.setPos(
            pos=[0,
                 self.pitch_plot[np.int(playback_pos_sample / self.hopsize)]])
        self.frame_player.slider.setValue(playback_pos_sample)
        self.waveform_widget.vline_wf.setPos([playback_pos_sample/ratio,
                                              np.min(self.raw_audio)])

        now = time()

        dt = now - self.last_time
        self.last_time = now
        if self.fps is None:
            self.fps = 1.0 / dt
        else:
            s = np.clip(dt * 3., 0, 1)
            self.fps = self.fps * (1 - s) + (1.0 / dt) * s
        self.melody_widget.zoom_selection.setTitle('%0.2f fps' % self.fps)

        # pos_vline = self.melody_widget.vline.pos()[0]
        # pos_xmin, pos_xmax = \
        #    self.melody_widget.zoom_selection.viewRange()[0]
        # dist = pos_xmax - pos_xmin

        # if pos_xmax * 0.98 <= pos_vline <= pos_xmax * 1.02:
        #    self.waveform_widget.region_wf.setRegion(
        #        [pos_xmax*samplerate+(hopsize/samplerate),
        #         (pos_xmax+dist)*samplerate])
        #    self.melody_widget.zoom_selection.setXRange(
        #        pos_xmax+(hopsize/samplerate), pos_xmax+dist, padding=0)


        # elif pos_vline < pos_xmin * 0.99 or pos_vline > pos_xmax:
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
        # else:
        # pass
        # else for now playing option
