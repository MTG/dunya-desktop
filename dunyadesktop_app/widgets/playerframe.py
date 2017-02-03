import json

import os

import numpy as np
import pyqtgraph.dockarea as pgdock
from PyQt5.QtCore import QSize, QMetaObject
from PyQt5.QtWidgets import QVBoxLayout, QFrame

from playbackframe import PlaybackFrame
from timeserieswidget import TimeSeriesWidget
from utilities.playback import Playback
from waveformwidget import WaveformWidget
from cultures.makam.featureparsers import (read_raw_audio, load_pitch, load_pd,
                                           load_tonic, get_feature_paths,
                                           load_notes)


DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')


class PlayerFrame(QFrame):
    samplerate = 44100.

    def __init__(self, recid, parent=None):
        QFrame.__init__(self, parent=parent)
        self.recid = recid
        self.__set_design()

        self.feature_paths = get_feature_paths(recid)
        self.__set_waveform()

        # initializing playback class
        self.playback = Playback()
        self.playback.set_source(self.feature_paths['audio_path'])

        # signals
        self.playback.positionChanged.connect(self.player_pos_changed)

        self.waveform_widget.region_wf.sigRegionChangeFinished.connect(
            self.wf_region_changed)
        self.waveform_widget.region_wf.clicked.connect(
            self.wf_region_item_clicked)

        self.frame_playback.toolbutton_play.clicked.connect(self.playback_play)
        self.frame_playback.toolbutton_pause.clicked.connect(
            self.playback_pause)

    def __set_design(self):
        self.setWindowTitle('Player')
        self.resize(1200, 550)
        self.setMinimumSize(QSize(850, 500))
        self.setStyleSheet("background-color: rgb(30, 30, 30);")

        self.dock_area = pgdock.DockArea()

        # dock fixed waveform
        self.dock_fixed_waveform = pgdock.Dock("Waveform", area='Top',
                                               hideTitle=True, closable=False,
                                               autoOrientation=False)
        self.dock_fixed_waveform.setFixedHeight(60)

        # initializing waveform widget
        self.waveform_widget = WaveformWidget()
        self.waveform_widget.setMinimumHeight(60)

        self.dock_fixed_waveform.addWidget(self.waveform_widget)
        self.dock_fixed_waveform.allowedAreas = ['top']
        self.dock_fixed_waveform.setAcceptDrops(False)
        self.dock_area.addDock(self.dock_fixed_waveform, position='top')

        self.dock_playback = pgdock.Dock(name='Playback', area='bottom',
                                         closable=False, autoOrientation=False)
        self.frame_playback = PlaybackFrame(self)
        self.frame_playback.toolbutton_pause.setDisabled(True)
        self.dock_playback.addWidget(self.frame_playback)
        self.dock_playback.setFixedHeight(60)
        self.dock_playback.setAcceptDrops(False)
        self.dock_area.addDock(self.dock_playback, position='bottom')

        layout = QVBoxLayout(self)
        layout.addWidget(self.dock_area)

        QMetaObject.connectSlotsByName(self)

    def __set_slider(self, len_audio):
        self.frame_playback.slider.setMinimum(0)
        self.frame_playback.slider.setMaximum(len_audio)
        self.frame_playback.slider.setTickInterval(10)
        self.frame_playback.slider.setSingleStep(1)

    def __set_waveform(self):
        (raw_audio, len_audio, min_audio,
         max_audio) = read_raw_audio(self.feature_paths['audio_path'])
        self.min_raw_audio = np.min(raw_audio)
        self.__set_slider(len_audio)
        self.waveform_widget.plot_waveform(raw_audio)

    def wf_region_item_clicked(self):
        self.playback_pause()

    def closeEvent(self, QCloseEvent):
        super(QFrame, self).closeEvent(QCloseEvent)
        if hasattr(self, 'waveform_widget'):
            self.waveform_widget.clear()
            self.waveform_widget.close()
        if hasattr(self, 'ts_widget'):
            self.ts_widget.clear()
            self.ts_widget.close()
        if hasattr(self, 'playback'):
            self.playback.pause()
        self.close()

    def __set_ts_widget(self):
        self.ts_widget = TimeSeriesWidget(self)
        self.ts_widget.add_1d_view()
        self.dock_ts = pgdock.Dock(name='Time Series', area='bottom',
                                   closable=True)
        self.dock_ts.addWidget(self.ts_widget)
        self.dock_area.addDock(self.dock_ts)

    def plot_1d_data(self, f_type, feature):
        if not hasattr(self, 'ts_widget'):
            self.__set_ts_widget()

        ftr = f_type + '--' + feature + '.json'
        feature_path = os.path.join(DOCS_PATH, self.recid, ftr)

        if feature == 'pitch' or feature == 'pitch_filtered':
            (time_stamps, pitch_plot, max_pitch, min_pitch, samplerate,
             hopsize) = load_pitch(feature_path)
            self.hop_size = hopsize
            x_min, x_max = self.waveform_widget.get_waveform_region
            if hasattr(self.ts_widget, 'zoom_selection'):
                self.ts_widget.hopsize = hopsize
                self.ts_widget.samplerate = samplerate
                self.ts_widget.plot_pitch(pitch_plot=pitch_plot,
                                          x_start=x_min,
                                          x_end=x_max,
                                          hop_size=hopsize)
                self.is_pitch_plotted = True

                histogram = \
                    os.path.join(DOCS_PATH, self.recid,
                                 'audioanalysis--pitch_distribution.json')
                vals, bins = load_pd(histogram)
                self.ts_widget.plot_histogram_raxis(vals, bins)

        if feature == 'tonic':
            tonic_values = load_tonic(feature_path)
            self.ts_widget.add_tonic(tonic_values)

    def playback_play(self):
        self.frame_playback.toolbutton_play.setDisabled(True)
        self.frame_playback.toolbutton_pause.setEnabled(True)
        self.playback.play()

    def playback_pause(self):
        self.frame_playback.toolbutton_play.setEnabled(True)
        self.frame_playback.toolbutton_pause.setDisabled(True)
        self.playback.pause()

    def wf_region_changed(self):
        pos = self.playback.position() / 1000.
        x_min, x_max = self.waveform_widget.get_waveform_region
        if x_min < pos < x_max:
            if hasattr(self, 'ts_widget'):
                if hasattr(self.ts_widget, 'zoom_selection'):
                    if self.ts_widget.is_pitch_plotted:
                        self.ts_widget.update_plot(start=x_min, stop=x_max,
                                                   hop_size=self.hop_size)
                    if self.ts_widget.is_notes_added:
                        self.ts_widget.update_notes(x_min, x_max)
        else:
            self.playback_pause()
            pos = x_min * 1000.
            self.playback.setPosition(pos)
            self.__update_vlines(pos)
            if hasattr(self, 'ts_widget'):
                if hasattr(self.ts_widget, 'zoom_selection'):
                    if self.ts_widget.is_pitch_plotted:
                        self.ts_widget.update_plot(start=x_min, stop=x_max,
                                                   hop_size=self.hop_size)
                    if self.ts_widget.is_notes_added:
                        self.ts_widget.update_notes(x_min, x_max)

    def __update_vlines(self, playback_pos):
        playback_pos_sec = playback_pos / 1000.
        playback_pos_sample = (playback_pos_sec * self.samplerate) + 10

        self.frame_playback.slider.setValue(playback_pos_sample)
        self.waveform_widget.vline_wf.setPos(
            [playback_pos_sample / self.waveform_widget.ratio,
             self.min_raw_audio])

    def player_pos_changed(self, playback_pos):
        self.__update_vlines(playback_pos)
        playback_pos_sec = playback_pos / 1000.

        xmin, xmax = self.waveform_widget.get_waveform_region
        diff = (xmax - xmin) * 0.1
        if not playback_pos_sec <= xmax - diff:
            x_start = xmax - diff
            x_end = x_start + (xmax - xmin)

            self.waveform_widget.change_wf_region(x_start, x_end)

        if hasattr(self, 'ts_widget'):
            if hasattr(self.ts_widget, 'vline'):
                self.ts_widget.vline.setPos([playback_pos_sec, 0])
            if hasattr(self.ts_widget, 'hline_histogram'):
                if self.ts_widget.pitch_plot is not None:
                    self.ts_widget.set_hist_cursor_pos(playback_pos_sec)

    def add_1d_roi_items(self, f_type, item):
        if not hasattr(self, 'ts_widget'):
            self.__set_ts_widget()

        if item == 'notes':
            ftr = f_type + '--' + item + '.json'
            feature_path = os.path.join(DOCS_PATH, self.recid, ftr)
            notes_dict = load_notes(feature_path)

        notes = []
        print notes_dict.keys()
        for key in notes_dict.keys():
            for dic in notes_dict[key]:
                interval = dic['interval']
                pitch = dic['performed_pitch']['value']
                notes.append([interval[0], interval[1], pitch])

        self.ts_widget.notes = np.array(notes)
        self.ts_widget.notes_start = self.ts_widget.notes[:, 0]
        self.ts_widget.notes_end = self.ts_widget.notes[:, 1]

        x_min, x_max = self.waveform_widget.get_waveform_region
        self.ts_widget.update_notes(x_min, x_max)
        self.ts_widget.is_notes_added = True
