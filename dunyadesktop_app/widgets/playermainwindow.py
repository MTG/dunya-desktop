import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QDockWidget,
                             QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt, QMetaObject

from .treewidget import FeatureWidgetAdaptive
from .playerframe import PlayerFrame
from .playbackframe import PlaybackFrame
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
        self.playback_frame.button_play.clicked.connect(
            self.player_frame.playback_play)
        self.playback_frame.button_pause.clicked.connect(
            self.player_frame.playback_pause)
        self.dw_contents_features.synthesis_changed.connect(
            self.player_frame._change_synthesis)

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

    @staticmethod
    def get_feature_path(mbid, type, item):
        feature = type + '--' + item + '.json'
        path = os.path.join(DOCS_PATH, mbid, feature)
        return path
