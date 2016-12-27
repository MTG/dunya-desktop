import os
import json
import copy

from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtCore import QSize, QMetaObject, QTimer
from essentia.standard import MonoLoader
import pyqtgraph.dockarea as pgdock
import numpy as np
from pyqtgraph.ptime import time

from dunyadesktop_app.widgets.waveformwidget import WaveformWidget
from dunyadesktop_app.widgets.melodywidget import MelodyWidget
from dunyadesktop_app.widgets.playerframe import PlayerFrame
from dunyadesktop_app.utilities.playback import Player
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


class PlayerDialog(QDialog):
    fps = None
    last_time = time()

    def __init__(self, recid):

        QDialog.__init__(self)
        self._set_design()

        # paths
        doc_folder, audio_path, pitch_path, pd_path = get_paths(recid)

        # loading features and audio
        raw_audio, len_audio, min_audio, max_audio = load_audio(audio_path)
        (time_stamps, self.pitch_plot, max_pitch, min_pitch,
         self.samplerate, self.hopsize) = load_pitch(pitch_path)
        vals, bins = load_pd(pd_path)

        # plotting features
        self.waveform_widget.plot_waveform(raw_audio, len_audio, min_audio,
                                           max_audio)
        self.melody_widget.plot_melody(time_stamps, self.pitch_plot, len_audio,
                                       self.samplerate, max_pitch)
        self.melody_widget.plot_histogram(vals, bins, max_pitch)

        # slider and playback thread
        self.playback_thread = Player()
        self.playback_thread.set_source(audio_path)
        self._set_slider(len_audio)

        self.frame_player.toolbutton_pause.setDisabled(True)

        self.playback_pos = 0.
        self.timer = QTimer()
        self.timer.setInterval(50)

        # signals
        # self.playback_thread.play_clicked.connect(self.start_timer)
        # self.playback_thread.pause_clicked.connect(self.stop_timer)
        # self.timer.timeout.connect(self.update_playback_pos)
        self.playback_thread.player.positionChanged.connect(self.update_vlines)
        self.waveform_widget.region_wf.sigRegionChangeFinished.connect(
            self.wf_region_changed)
        self.frame_player.toolbutton_play.clicked.connect(self.playback_play)
        self.frame_player.toolbutton_pause.clicked.connect(self.playback_pause)

    def start_timer(self):
        self.timer.start()

    def stop_timer(self):
        self.timer.stop()

    def closeEvent(self, QCloseEvent):
        self.waveform_widget.clear()
        self.melody_widget.clear()
        self.playback_thread.pause()

    def update_wf_pos(self, samplerate):
        self.waveform_widget.vline_wf.setPos(
            [self.playback_pos * samplerate, 0])

    def _set_design(self):
        self.setWindowTitle('Player')
        self.resize(1050, 550)
        self.setMinimumSize(QSize(850, 500))
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.verticalLayout = QVBoxLayout(self)

        area = pgdock.DockArea()
        d1 = pgdock.Dock("Waveform", area='Top', autoOrientation=False,
                         closable=True)
        # d1.allowedAreas = ['top']
        self.waveform_widget = WaveformWidget()
        d1.addWidget(self.waveform_widget)
        area.addDock(d1, 'top')

        d2 = pgdock.Dock('Pitch')
        self.melody_widget = MelodyWidget()
        d2.addWidget(self.melody_widget)
        area.addDock(d2, 'bottom')

        # self.verticalLayout.addWidget(self.waveform_widget)

        # self.melody_widget = MelodyWidget()
        # self.verticalLayout.addWidget(self.melody_widget)

        self.frame_player = PlayerFrame(self)
        self.verticalLayout.addWidget(self.frame_player)
        self.verticalLayout.addWidget(area)
        QMetaObject.connectSlotsByName(self)

    def playback_play(self):
        self.frame_player.toolbutton_play.setDisabled(True)
        self.frame_player.toolbutton_pause.setEnabled(True)
        self.playback_thread.play()

    def playback_pause(self):
        self.frame_player.toolbutton_play.setEnabled(True)
        self.frame_player.toolbutton_pause.setDisabled(True)
        self.playback_thread.pause()

    def _set_slider(self, len_audio):
        self.frame_player.slider.setMinimum(0)
        self.frame_player.slider.setMaximum(len_audio)
        self.frame_player.slider.setTickInterval(10)
        self.frame_player.slider.setSingleStep(1)

    def wf_region_changed(self):
        pos_wf_x_min, pos_wf_x_max = self.waveform_widget.region_wf.getRegion()
        self.melody_widget.set_zoom_selection_area(pos_wf_x_min, pos_wf_x_max,
                                                   self.samplerate,
                                                   self.hopsize)

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
        playback_pos_sec = playback_pos / 1000.
        playback_pos_sample = playback_pos_sec * self.samplerate
        self.melody_widget.vline.setPos([playback_pos_sec, 0])
        self.melody_widget.hline_histogram.setPos(
            pos=[0,
                 self.pitch_plot[np.int(playback_pos_sample / self.hopsize)]])
        self.frame_player.slider.setValue(playback_pos_sample)
        self.waveform_widget.vline_wf.setPos([playback_pos_sample, 0])

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
