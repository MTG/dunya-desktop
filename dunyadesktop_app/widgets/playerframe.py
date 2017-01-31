import os
import json
import copy

from PyQt5.QtWidgets import QVBoxLayout, QFrame
from PyQt5.QtCore import QSize, QMetaObject
from essentia.standard import MonoLoader
import pyqtgraph.dockarea as pgdock
import numpy as np

from waveformwidget import WaveformWidget
from timeserieswidget import TimeSeriesWidget
from playbackframe import PlaybackFrame
from utilities.playback import Playback
from cultures.makam import utilities
import ui_files.resources_rc

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')


def read_audio(audio_path):
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


def load_tonic(tonic_path):
    tnc = json.load(open(tonic_path))
    try:
        return [tnc['value']]
    except KeyError:
        return [work['value'] for work in tnc.values()]


def get_feature_paths(recid):
    doc_folder = os.path.join(DOCS_PATH, recid)
    (full_names, folders, names) = \
        utilities.get_filenames_in_dir(dir_name=doc_folder, keyword='*.json')

    paths = {'audio_path': os.path.join(doc_folder, recid + '.mp3')}
    for xx, name in enumerate(names):
        paths[name.split('.json')[0]] = full_names[xx]
    return paths


def load_notes(notes_path):
    notes = json.load(open(notes_path))
    return notes


class PlayerFrame(QFrame):
    samplerate = 44100.

    def __init__(self, recid, parent=None):
        QFrame.__init__(self, parent=parent)
        self.recid = recid
        self.__set_design()

        self.feature_paths = get_feature_paths(recid)

        (self.raw_audio, len_audio,
         min_audio, max_audio) = read_audio(self.feature_paths['audio_path'])
        self.__set_slider(len_audio)
        self.waveform_widget.plot_waveform(self.raw_audio)

        self.playback = Playback()
        self.playback.set_source(self.feature_paths['audio_path'])

        self.playback.player.positionChanged.connect(self.player_pos_changed)
        self.waveform_widget.region_wf.sigRegionChangeFinished.connect(
            self.wf_region_changed)
        self.waveform_widget.region_wf.clicked.connect(self.wf_region_item_clicked)
        self.frame_playback.toolbutton_play.clicked.connect(self.playback_play)
        self.frame_playback.toolbutton_pause.clicked.connect(
            self.playback_pause)

    def wf_region_item_clicked(self):
        self.playback_pause()

    def closeEvent(self, QCloseEvent):
        super(QFrame, self).closeEvent(QCloseEvent)
        if hasattr(self, 'waveform_widget'):
            self.waveform_widget.clear()
        if hasattr(self, 'melody_widget'):
            self.ts_widget.clear()
        if hasattr(self, 'playback'):
            self.playback.pause()

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

    def _set_ts_widget(self):
        self.ts_widget = TimeSeriesWidget(self)
        self.ts_widget.add_1d_view()
        self.dock_ts = pgdock.Dock(name='Time Series', area='bottom',
                                   closable=True)
        self.dock_ts.addWidget(self.ts_widget)
        self.dock_area.addDock(self.dock_ts)

    def plot_1d_data(self, f_type, feature):
        if not hasattr(self, 'ts_widget'):
            self._set_ts_widget()

        ftr = f_type + '--' + feature + '.json'
        feature_path = os.path.join(DOCS_PATH, self.recid, ftr)

        if feature == 'pitch' or feature == 'pitch_filtered':
            (time_stamps, pitch_plot, max_pitch, min_pitch, samplerate,
             hopsize) = load_pitch(feature_path)
            x_min, x_max = self.waveform_widget.get_waveform_region()
            if hasattr(self.ts_widget, 'zoom_selection'):
                self.ts_widget.hopsize = hopsize
                self.ts_widget.samplerate = samplerate
                self.ts_widget.plot_pitch(pitch_plot, x_min, x_max)
                self.is_pitch_plotted = True

                histogram = \
                    os.path.join(DOCS_PATH, self.recid,
                                 'audioanalysis--pitch_distribution.json')
                vals, bins = load_pd(histogram)
                self.ts_widget.plot_histogram(vals, bins)

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
        pos = self.playback.player.position() / 1000.
        x_min, x_max = self.waveform_widget.get_waveform_region()
        #self._update_vlines(pos)
        if x_min < pos < x_max:
            if hasattr(self, 'ts_widget'):
                if hasattr(self.ts_widget, 'zoom_selection'):
                    if self.ts_widget.is_pitch_plotted:
                        self.ts_widget.update_plot(x_min, x_max)
                    if self.ts_widget.is_notes_added:
                        self.ts_widget.update_notes(x_min, x_max)
        else:
            self.playback_pause()
            pos = x_min * 1000.
            self.playback.player.setPosition(pos)
            self._update_vlines(pos)
            if hasattr(self, 'ts_widget'):
                if hasattr(self.ts_widget, 'zoom_selection'):
                    if self.ts_widget.is_pitch_plotted:
                        self.ts_widget.update_plot(x_min, x_max)
                    if self.ts_widget.is_notes_added:
                        self.ts_widget.update_notes(x_min, x_max)

    def _update_vlines(self, playback_pos):
        ratio = len(self.raw_audio) / len(self.waveform_widget.visible)
        playback_pos_sec = playback_pos / 1000.
        playback_pos_sample = (playback_pos_sec * self.samplerate) + 10

        self.frame_playback.slider.setValue(playback_pos_sample)
        self.waveform_widget.vline_wf.setPos([playback_pos_sample / ratio,
                                              np.min(self.raw_audio)])

    def player_pos_changed(self, playback_pos):
        self._update_vlines(playback_pos)
        playback_pos_sec = playback_pos / 1000.

        xmin, xmax = self.waveform_widget.get_waveform_region()
        diff = (xmax - xmin) * 0.1
        if not playback_pos_sec <= xmax - diff:
            x_start = xmax - diff
            x_end = x_start + (xmax - xmin)

            self.waveform_widget.change_wf_region(x_start, x_end)

        if hasattr(self, 'ts_widget'):
            if hasattr(self.ts_widget, 'vline'):
                self.ts_widget.vline.setPos([playback_pos_sec, 0])
            if hasattr(self.ts_widget, 'hline_histogram') \
                    and self.ts_widget.pitch_plot is not None:
                self.ts_widget.set_hline_pos(playback_pos_sec)

    def add_1d_roi_items(self, f_type, item):
        if not hasattr(self, 'ts_widget'):
            self._set_ts_widget()

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

        x_min, x_max = self.waveform_widget.get_waveform_region()
        self.ts_widget.update_notes(x_min, x_max)
        self.ts_widget.is_notes_added = True
        print len(self.ts_widget.notes)