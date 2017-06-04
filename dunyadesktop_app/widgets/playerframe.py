import os
import json

import numpy as np
import pyqtgraph.dockarea as pgdock
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLayout, QSizePolicy
from PyQt5.Qt import pyqtSignal

from .waveformwidget import WaveformWidget
from .scoredialog import ScoreWidget
from .widgetutilities import cursor_pos_sample, current_pitch
from utilities.playback import Playback
from cultures.makam.featureparsers import (read_raw_audio, load_pitch, load_pd,
                                           load_tonic, get_feature_paths,
                                           load_notes, get_sections,
                                           generate_score_map,
                                           mp3_to_wav_converter,
                                           generate_score_onsets,
                                           get_score_sections)


DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'scores')
COLORS_RGB = [(77, 157, 224, 70), (255, 217, 79, 70), (224, 76, 114, 70),
              (250, 240, 202, 70), (255, 89, 100, 70), (255, 196, 165, 70),
              (102, 0, 17, 70), (201, 149, 18, 70), (58, 1, 92, 70),
              (117, 112, 201, 70)]


class DockAreaWidget(pgdock.DockArea):
    def __init__(self, temporary=False, home=None):
        pgdock.DockArea.__init__(self, temporary=temporary, home=home)
        self.allowedAreas = ['top', 'bottom']
        self.layout.setSizeConstraint(QLayout.SetMinimumSize)

    def floatDock(self, dock):
        pass


class PlayerFrame(QFrame):
    samplerate = 44100.
    update_histogram = pyqtSignal(float)

    def __init__(self, docid, parent=None):
        QFrame.__init__(self, parent=parent)
        self.docid = docid
        self.__set_design()

        self.current_folder = os.path.join(DOCS_PATH, self.docid)
        current_synthesis = self.get_current_synthesis()
        self.get_synt_path(current_synthesis)
        self.__set_waveform()
        self.__add_sections()

        # initializing playback class
        self.playback = Playback()
        self.playback.set_source(self.current_synth_wav)

        # flags
        self.score_visible = False
        self.index = 0

        # signals
        self.playback.positionChanged.connect(self.player_pos_changed)

        #self.waveform_widget.region_wf.sigRegionChangeFinished.connect(
        #    self.wf_region_changed)
        #self.waveform_widget.region_wf.clicked.connect(
        #    self.wf_region_item_clicked)

    def __add_sections(self):
        metadata_path = os.path.join(DOCS_PATH, self.docid,
                                     'scoreanalysis--metadata.json')
        metadata = json.load(open(metadata_path))
        sections = get_score_sections(metadata)

        self.add_sections_to_waveform(sections)

    def _change_synthesis(self, synthesis):
        self.playback_pause()
        self.get_synt_path(synthesis)
        current_pos = self.playback.position()
        self.playback.set_source(self.current_synth_wav)
        self.playback.setPosition(current_pos)
        self.playback_play()

    def get_synt_path(self, current_synth):
        path = os.path.join(self.current_folder, current_synth)
        self.current_synth_mp3 = path + '.mp3'
        self.current_synth_wav = path + '.wav'

    def get_current_synthesis(self):
        main_window = self.parent()
        return main_window.dw_contents_features.current_synthesis()

    def __set_design(self):
        """
        Sets general settings of frame widget, adds dock area and dock widgets.
        """
        self.setWindowTitle('Player')
        self.resize(1200, 550)

        self.dock_area = DockAreaWidget()

        # dock fixed waveform
        dock_waveform = pgdock.Dock(name="Waveform", area='Top',
                                    hideTitle=True, closable=False,
                                    autoOrientation=False)
        dock_waveform.setMinimumHeight(100)
        dock_waveform.layout.setSizeConstraint(QLayout.SetMinimumSize)
        dock_waveform.widgetArea.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,
                                                           QSizePolicy.Minimum))

        # initializing waveform widget
        self.waveform_widget = WaveformWidget()

        # adding waveform widget to waveform dock
        dock_waveform.addWidget(self.waveform_widget)
        dock_waveform.allowedAreas = ['top']
        dock_waveform.setAcceptDrops(False)
        # adding waveform dock to dock area
        self.dock_area.addDock(dock_waveform, position='top')

        dock_score = pgdock.Dock(name='Score', area='bottom', closable=False,
                                 autoOrientation=False)
        dock_score.setStyleSheet('background-color: #F4ECD7;')
        self.score_widget = ScoreWidget()
        dock_score.addWidget(self.score_widget)
        dock_score.setAcceptDrops(False)
        self.dock_area.addDock(dock_score, position='bottom')

        self._prepare_score_widget(self.docid)

        # adding dock area to frame
        layout = QVBoxLayout(self)
        layout.addWidget(self.dock_area)

    def __set_waveform(self):
        """
        Reads the audio and plots the waveform.
        """
        if not os.path.exists(self.current_synth_wav):
            mp3_to_wav_converter(self.current_synth_mp3)
        (raw_audio, len_audio, min_audio,
         max_audio) = read_raw_audio(self.current_synth_wav)
        self.waveform_widget.min_raw_audio = min_audio
        self.waveform_widget.plot_waveform(raw_audio)

    def wf_region_item_clicked(self):
        self.playback_pause()

    def closeEvent(self, QCloseEvent):
        super(QFrame, self).closeEvent(QCloseEvent)
        if hasattr(self, 'waveform_widget'):
            self.waveform_widget.clear()
            self.waveform_widget.close()
        if hasattr(self, 'playback'):
            self.playback.pause()
        self.close()

    def playback_play(self):
        self.playback.play()

    def playback_pause(self):
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
            #self.parent().playback_frame.slider.setValue(pos_sample)
            self.waveform_widget.update_wf_vline(pos_sample)

        if hasattr(self, 'ts_widget'):
            if hasattr(self.ts_widget, 'zoom_selection'):
                if self.ts_widget.is_pitch_plotted:
                    self.ts_widget.update_plot(start=x_min, stop=x_max,
                                               hop_size=self.hopsize)
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

            # TODO
            #self.parent().playback_frame.slider.setValue(playback_pos_sample)

            # checks the position of linear region item. If the position of
            # waveform cursor is
            xmin, xmax = self.waveform_widget.get_waveform_region
            diff = (xmax - xmin) * 0.1
            if not playback_pos_sec <= xmax - diff:
                x_start = xmax - diff
                x_end = x_start + (xmax - xmin)
                self.waveform_widget.change_wf_region(x_start, x_end)

            self.__update_score(playback_pos_sec)

    def __update_score(self, playback_pos_sec):
        index = self.find_current_note_index(self.onsets_starts,
                                             self.onsets_ends,
                                             self.onsets_indexes,
                                             playback_pos_sec)
        if index:
            svg_path = self.notes_map[self.docid][str(index)]
            self.score_widget.update_note(svg_path, index)

    def add_sections_to_waveform(self, sections):
        colors = {}
        color_index = 0

        for section in sections:
            try:
                color = colors[section]

            except KeyError:
                color = COLORS_RGB[color_index]
                colors[section] = color
                color_index += 1

            durations = sections[section]

            for duration in durations:
                try:
                    start = list(self.onsets_indexes).index(duration[0])
                    end = list(self.onsets_indexes).index(duration[1])

                    self.waveform_widget.add_section(
                        np.array([self.onsets_starts[start],
                                  self.onsets_ends[end]]), section, section,
                        color)
                except ValueError:
                    pass

    def _prepare_score_widget(self, mbid):
        notes_map = {}

        # generating note map
        notes_array = generate_score_map(mbid)
        notes_map[mbid] = notes_array

        # getting onsets
        self.onsets_starts, self.onsets_ends, self.onsets_indexes = \
            generate_score_onsets(mbid)

        self.notes_map = notes_map
        self.score_visible = True

    def find_current_note_index(self, n_array_start, n_array_end, n_array_indexes,
                                value):
        index = (np.abs(n_array_start - value)).argmin()

        array_index = n_array_indexes[index]
        val_start = n_array_start[index]
        val_end = n_array_end[index]

        if self.index != array_index:
            if val_start < value < val_end:
                self.index = n_array_indexes[index]
                return n_array_indexes[index] # score indexes starts with 1
        else:
            return None
