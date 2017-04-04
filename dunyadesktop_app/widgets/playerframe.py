import os
import json

import numpy as np
import pyqtgraph.dockarea as pgdock
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QVBoxLayout, QFrame

from .playbackframe import PlaybackFrame
from .timeserieswidget import TimeSeriesWidget
from .waveformwidget import WaveformWidget
from .scoredialog import ScoreDialog
from utilities.playback import Playback
from cultures.makam.featureparsers import (read_raw_audio, load_pitch, load_pd,
                                           load_tonic, get_feature_paths,
                                           load_notes, get_sections,
                                           generate_score_map,
                                           mp3_to_wav_converter)


DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')
COLORS_RGB = [(77, 157, 224, 70), (255, 217, 79, 70), (224, 76, 114, 70),
              (250, 240, 202, 70), (255, 89, 100, 70), (255, 196, 165, 70),
              (102, 0, 17, 70), (201, 149, 18, 70), (58, 1, 92, 70),
              (117, 112, 201, 70)]


class DockAreaWidget(pgdock.DockArea):
    def __init__(self, temporary=False, home=None):
        pgdock.DockArea.__init__(self, temporary=temporary, home=home)

    def floatDock(self, dock):
        pass


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
        self.playback.set_source(self.feature_paths['audio_path_wav'])

        # flags
        self.score_visible = False
        self.index = 0

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
        """
        Sets general settings of frame widget, adds dock area and dock widgets.
        """
        self.setWindowTitle('Player')
        self.resize(1200, 550)
        self.setMinimumSize(QSize(850, 500))
        self.setStyleSheet("background-color: rgb(30, 30, 30);")

        self.dock_area = DockAreaWidget()

        # dock fixed waveform
        dock_waveform = pgdock.Dock(name="Waveform", area='Top',
                                    hideTitle=True, closable=False,
                                    autoOrientation=False)
        dock_waveform.setFixedHeight(100)

        # initializing waveform widget
        self.waveform_widget = WaveformWidget()
        self.waveform_widget.setMinimumHeight(100)

        # adding waveform widget to waveform dock
        dock_waveform.addWidget(self.waveform_widget)
        dock_waveform.allowedAreas = ['top']
        dock_waveform.setAcceptDrops(False)
        # adding waveform dock to dock area
        self.dock_area.addDock(dock_waveform, position='top')

        # dock playback
        dock_playback = pgdock.Dock(name='Playback', area='bottom',
                                    closable=False, autoOrientation=False)
        # initializing playback frame
        self.frame_playback = PlaybackFrame(self)
        self.frame_playback.toolbutton_pause.setDisabled(True)

        # adding playback frame to playback dock
        dock_playback.addWidget(self.frame_playback)
        dock_playback.setFixedHeight(60)
        dock_playback.setAcceptDrops(False)

        # adding playback dock to dock area
        self.dock_area.addDock(dock_playback, position='bottom')

        # adding dock area to frame
        layout = QVBoxLayout(self)
        layout.addWidget(self.dock_area)

    def __set_slider(self, len_audio):
        """
        Sets the slider according to the given audio recording.
        :param len_audio:
        """
        self.frame_playback.slider.setMinimum(0)
        self.frame_playback.slider.setMaximum(len_audio)
        self.frame_playback.slider.setTickInterval(10)
        self.frame_playback.slider.setSingleStep(1)

    def __set_waveform(self):
        """
        Reads the audio and plots the waveform.
        """
        if not os.path.exists(self.feature_paths['audio_path_wav']):
            mp3_to_wav_converter(self.feature_paths['audio_path_mp3'])
        (raw_audio, len_audio, min_audio,
         max_audio) = read_raw_audio(self.feature_paths['audio_path_wav'])
        self.waveform_widget.min_raw_audio = min_audio
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

    def __add_ts_widget(self):
        self.ts_widget = TimeSeriesWidget(self)
        self.ts_widget.add_1d_view()
        dock_ts = pgdock.Dock(name='Time Series', area='bottom', closable=True)
        dock_ts.addWidget(self.ts_widget)
        self.dock_area.addDock(dock_ts)

        # signals
        self.ts_widget.wheel_event.connect(self.waveform_widget.wheelEvent)

    def plot_1d_data(self, f_type, feature):

        """
        Plots 1D data.
        :param f_type:
        :param feature:
        """
        if not hasattr(self, 'ts_widget'):
            self.__add_ts_widget()

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
                self.ts_widget.pitch_plot = pitch_plot
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
        """
        Updates the plots according to the change in waveform region item.
        """
        pos = self.playback.position() / 1000.  # playback pos in seconds
        x_min, x_max = self.waveform_widget.get_waveform_region

        if not x_min < pos < x_max:
            self.playback_pause()
            pos_ms = x_min * 1000.
            pos_sample = x_min * self.samplerate
            self.playback.setPosition(pos_ms)
            self.frame_playback.slider.setValue(pos_sample)
            self.waveform_widget.update_wf_vline(pos_sample)

        if hasattr(self, 'ts_widget'):
            if hasattr(self.ts_widget, 'zoom_selection'):
                if self.ts_widget.is_pitch_plotted:
                    self.ts_widget.update_plot(start=x_min, stop=x_max,
                                               hop_size=self.hop_size)
                    self.ts_widget.vline.setPos([x_min, 0])
                if self.ts_widget.is_notes_added:
                    self.ts_widget.update_notes(x_min, x_max)

    def player_pos_changed(self, playback_pos):
        """
        Updates the positions of cursors when playback position is changed.
        Changes the waveform region item according to the position of playback.
        :param playback_pos: (int) Position of player in milliseconds.
        """
        if self.playback.state() == 1:
            playback_pos_sec = playback_pos / 1000.
            playback_pos_sample = playback_pos_sec * self.samplerate

            self.waveform_widget.update_wf_vline(playback_pos_sample)
            self.frame_playback.slider.setValue(playback_pos_sample)

            # checks the position of linear region item. If the position of
            # waveform cursor is
            xmin, xmax = self.waveform_widget.get_waveform_region
            diff = (xmax - xmin) * 0.1
            if not playback_pos_sec <= xmax - diff:
                x_start = xmax - diff
                x_end = x_start + (xmax - xmin)
                self.waveform_widget.change_wf_region(x_start, x_end)

            # checks if time series widget is initialized or not
            if hasattr(self, 'ts_widget'):
                self.ts_widget.vline.setPos([playback_pos_sec, 0])
                # checks if horizontal line of y-axis exists
                if hasattr(self.ts_widget, 'hline_histogram'):
                    if self.ts_widget.pitch_plot is not None:
                        self.ts_widget.set_hist_cursor_pos(playback_pos_sec)
            if self.score_visible:
                self.__update_score(playback_pos_sec)

    def __update_score(self, playback_pos_sec):
        index = self.find_current_note_index(self.ts_widget.notes_start,
                                             self.ts_widget.notes_end,
                                             playback_pos_sec)
        if index:
            workid = self.metadata[index][0]
            score_index = self.metadata[index][1]

            svg_path = self.notes_map[workid][str(score_index)]
            self.score_dialog.score_widget.update_note(svg_path, score_index)

    def add_1d_roi_items(self, f_type, item):
        """
        Adds 1d roi item.
        :param f_type: (str) Feature type
        :param item: (str) Feature subtype
        """
        if not hasattr(self, 'ts_widget'):
            self.__add_ts_widget()

        if item == 'notes':
            ftr = f_type + '--' + item + '.json'
            feature_path = os.path.join(DOCS_PATH, self.recid, ftr)
            notes_dict = load_notes(feature_path)

            notes = []
            metadata = []
            for workid in notes_dict.keys():
                for dic in notes_dict[workid]:
                    interval = dic['interval']
                    pitch = dic['performed_pitch']['value']
                    notes.append([interval[0], interval[1], pitch])
                    metadata.append([workid, dic['index_in_score'],
                                     dic['label'], dic['symbol']])

            self.ts_widget.notes = np.array(notes)
            self.ts_widget.notes_start = self.ts_widget.notes[:, 0]
            self.ts_widget.notes_end = self.ts_widget.notes[:, 1]

            self.metadata = metadata

            x_min, x_max = self.waveform_widget.get_waveform_region
            self.ts_widget.update_notes(x_min, x_max)
            self.ts_widget.is_notes_added = True

    def add_sections_to_waveform(self, feature_path):
        sections = get_sections(feature_path)

        colors = {}
        color_index = 0
        for work in sections:
            for section in sections[work]:
                sec_name = section['name'].split('--')[0]
                try:
                    color = colors[sec_name]

                except KeyError:
                    color = COLORS_RGB[color_index]
                    colors[sec_name] = color
                    color_index += 1

                self.waveform_widget.add_section(np.array(section['time']),
                                                 section['name'],
                                                 section['title'],
                                                 color)

    def open_score_dialog(self, mbid):
        metadata_path = os.path.join(DOCS_PATH, mbid,
                                     'audioanalysis--metadata.json')
        works = json.load(open(metadata_path))['works']

        notes_map = {}
        for work in works:
            notes_array = generate_score_map(work['mbid'])
            notes_map[work['mbid']] = notes_array
        self.notes_map = notes_map
        self.score_dialog = ScoreDialog(self)
        self.score_dialog.show()
        self.score_visible = True

    def find_current_note_index(self, n_array_start, n_array_end, value):
        index = (np.abs(n_array_start - value)).argmin()
        val_start = n_array_start[index]
        val_end = n_array_end[index]

        if self.index != index:
            if val_start < value < val_end:
                self.index = index
                return index + 1 # score indexes starts with 1
        else:
            return None
