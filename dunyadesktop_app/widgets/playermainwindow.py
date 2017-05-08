import os
import json

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QDockWidget,
                             QDialog, QHBoxLayout)
from PyQt5.QtCore import Qt, QMetaObject
import pyqtgraph

from .treewidget import FeatureTreeWidget, MetadataTreeMakam
from .playerframe import PlayerFrame
from .playerframe import PlaybackFrame
from .histogram import HistogramDialog
from cultures.makam.featureparsers import load_pd

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')


class PlayerMainWindow(QMainWindow):
    def __init__(self, docid, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.docid = docid
        self._set_design(docid)
        QMetaObject.connectSlotsByName(self)

        # signals
        self.feature_tree.item_checked.connect(self.evaluate_checked_signal)

        # signals
        self.playback_frame.button_play.clicked.connect(
            self.player_frame.playback_play)
        self.playback_frame.button_pause.clicked.connect(
            self.player_frame.playback_pause)

    def _set_design(self, docid):
        self.resize(710, 550)
        self.central_widget = QWidget()

        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(2, 2, 2, 2)

        self.player_frame = PlayerFrame(recid=docid, parent=self)
        layout.addWidget(self.player_frame)

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

        self.dw_contents_features = QWidget()
        layout3 = QVBoxLayout(self.dw_contents_features)
        layout3.setContentsMargins(3, 3, 3, 3)
        layout2 = QVBoxLayout()

        self.feature_tree = FeatureTreeWidget(self.dw_contents_features)
        self.feature_tree.get_feature_list(docid=str(docid))

        layout2.addWidget(self.feature_tree)
        layout3.addLayout(layout2)
        self.dw_features.setWidget(self.dw_contents_features)

        # dock widget for playlist
        self.dw_playlist = QDockWidget(self.central_widget)
        self.dw_playlist.setTitleBarWidget(QWidget())
        self.dw_playlist.setMinimumSize(QtCore.QSize(100, 130))
        self.dw_playlist.setMaximumSize(QtCore.QSize(400, 524287))
        self.dw_playlist.setFloating(False)
        self.dw_playlist.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dw_playlist.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)

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

        # add dock widgets to main window
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dw_features)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dw_playlist)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dw_playback)

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
        self.player_frame.closeEvent(close_event)

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
