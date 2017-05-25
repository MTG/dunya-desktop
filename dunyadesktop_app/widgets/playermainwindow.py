import os
import json

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QDockWidget,
                             QDialog, QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt, QMetaObject

from .treewidget import (FeatureTreeWidget, MetadataTreeMakam,
                         FeatureWidgetAdaptive)
from .playerframe import PlayerFrame
from .playbackframe import PlaybackFrame
from .histogram import HistogramDialog
from .table import TablePlaylist
from cultures.makam.featureparsers import load_pd, mp3_to_wav_converter
from cultures.makam.utilities import get_filenames_in_dir
from utilities import database

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'scores')


class PlayerMainWindow(QMainWindow):
    def __init__(self, docid, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.docid = docid
        self._set_design(docid)
        self._convert_mp3_to_wav()
        QMetaObject.connectSlotsByName(self)

        # signals
        #self.feature_tree.item_checked.connect(self.evaluate_checked_signal)

        # signals
        self.playback_frame.button_play.clicked.connect(
            self.player_frame.playback_play)
        self.playback_frame.button_pause.clicked.connect(
            self.player_frame.playback_pause)

    def _convert_mp3_to_wav(self):
        PATH = os.path.join(DOCS_PATH, self.docid)
        fullnames, folders, names = get_filenames_in_dir(PATH)

        for mp3 in fullnames:
            wav = mp3[:-4] + '.wav'
            if not os.path.exists(wav):
                mp3_to_wav_converter(mp3)

    def _set_design(self, docid):
        self.resize(710, 550)
        self.central_widget = QWidget(self)

        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(2, 2, 2, 2)

        self.setCentralWidget(self.central_widget)

        # dock widget for features
        self.dw_features = QDockWidget(self)
        self.dw_features.setTitleBarWidget(QWidget())
        self.dw_features.setMinimumSize(QtCore.QSize(100, 130))
        self.dw_features.setMaximumSize(QtCore.QSize(400, 524287))
        self.dw_features.setFloating(False)
        self.dw_features.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dw_features.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)

        self.dw_contents_features = FeatureWidgetAdaptive(docid, self)
        self.dw_features.setWidget(self.dw_contents_features)

        # dock widget for playlist
        self.dw_playlist = QDockWidget(self)
        self.dw_playlist.setTitleBarWidget(QWidget())
        self.dw_playlist.setMinimumSize(QtCore.QSize(100, 130))
        self.dw_playlist.setMaximumSize(QtCore.QSize(400, 524287))
        self.dw_playlist.setFloating(False)
        self.dw_playlist.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dw_playlist.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)

        self.dw_playlist_widgets = QWidget(self)
        layout5 = QVBoxLayout()
        self.playlist_table = TablePlaylist()
        collection = self.parent().dwc_left.listView_collections.currentItem()
        coll_label = QLabel(collection.text())
        if collection:
            coll_name = collection.text()
        else:
            coll_name = 'MainCollection'
        self._set_playlist_table(coll_name)
        layout5.addWidget(coll_label)
        layout5.addWidget(self.playlist_table)
        self.dw_playlist_widgets.setLayout(layout5)
        self.dw_playlist.setWidget(self.dw_playlist_widgets)

        # dock widget for playback
        self.dw_playback = QDockWidget(self.central_widget)
        self.dw_playback.setTitleBarWidget(QWidget())
        self.dw_playback.setFixedHeight(90)
        self.dw_playback.setFloating(False)
        self.dw_playback.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.dw_playback.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

        dw_contents = QWidget()
        layout4 = QHBoxLayout(dw_contents)
        layout4.setContentsMargins(3, 3, 3, 3)
        self.playback_frame = PlaybackFrame(dw_contents)
        layout4.addWidget(self.playback_frame)
        self.dw_playback.setWidget(dw_contents)

        self.player_frame = PlayerFrame(self.docid, parent=self)
        layout.addWidget(self.player_frame)

        # add dock widgets to main window
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dw_features)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dw_playlist)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dw_playback)

    def _set_playlist_table(self, coll_name):
        conn, c = database.connect()
        collection = database.fetch_collection(c, coll_name)
        self.playlist_table.add_recordings(collection)

    def __set_slider(self, len_audio):
        """
        Sets the slider according to the given audio recording.
        :param len_audio:
        """
        self.playback_frame.slider.setMinimum(0)
        self.playback_frame.slider.setMaximum(len_audio)
        self.playback_frame.slider.setTickInterval(10)
        self.playback_frame.slider.setSingleStep(1)

    def closeEvent(self, close_event):
        self.player_frame.playback.pause()
        self.player_frame.score_widget.close_event()

    def evaluate_checked_signal(self, type, item, is_checked):
        if item == 'pitch' or item == 'pitch_filtered':
            if is_checked:
                self.player_frame.plot_1d_data(type, item)
            else:
                self.player_frame.ts_widget.zoom_selection.clearPlots()
                self.player_frame.is_pitch_plotted = False
                self.player_frame.ts_widget.pitch_plot = None

                if hasattr(self.player_frame.ts_widget, 'hline_histogram'):
                    self.player_frame.ts_widget.right_axis.removeItem(
                        self.player_frame.ts_widget.hline_histogram)

        if item == 'tonic':
            if is_checked:
                self.player_frame.plot_1d_data(type, item)
            else:
                self.player_frame.ts_widget.remove_given_items(
                    self.player_frame.ts_widget.zoom_selection,
                    self.player_frame.ts_widget.tonic_lines)

        if item == 'notes':
            if is_checked:
                self.player_frame.add_1d_roi_items(type, item)
                self.player_frame.open_score_dialog(self.docid)
            else:
                self.player_frame.ts_widget.remove_given_items(
                    self.player_frame.ts_widget.zoom_selection,
                    self.player_frame.ts_widget.rois)
                self.player_frame.ts_widget.is_notes_added = False

        if item == 'metadata':
            if is_checked:
                m_path = self.get_feature_path(self.docid, type=type,
                                               item=item)
                metadata = json.load(open(m_path))

                self.metadata_dialog = QDialog(self)
                layout = QVBoxLayout(self.metadata_dialog)
                mt = MetadataTreeMakam(metadata)
                layout.addWidget(mt)
                self.metadata_dialog.setLayout(layout)
                self.metadata_dialog.show()
            else:
                self.metadata_dialog.close()

        if item == 'sections':
            if is_checked:
                s_path = self.get_feature_path(self.docid, type=type,
                                               item=item)
                self.player_frame.add_sections_to_waveform(s_path)
            else:
                self.player_frame.waveform_widget.remove_sections()

        if item == 'pitch_distribution':
            if is_checked:
                s_path = self.get_feature_path(self.docid, type=type,
                                               item=item)
                vals, bins = load_pd(s_path)
                self.hist_dialog = HistogramDialog()
                self.hist_dialog.plot_histogram(bins, vals)
                self.hist_dialog.show()
                self.player_frame.hist_visible= True

                self.player_frame.update_histogram.connect(
                    self.hist_dialog.update_histogram)

            else:
                self.hist_dialog.close()
                self.player_frame.hist_visible = False

    @staticmethod
    def get_feature_path(mbid, type, item):
        feature = type + '--' + item + '.json'
        path = os.path.join(DOCS_PATH, mbid, feature)
        return path
