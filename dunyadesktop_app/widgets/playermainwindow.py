import os
import json

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QDockWidget,
                             QDialog)
from PyQt5.QtCore import Qt, QMetaObject

from treewidget import FeatureTreeWidget, MetadataTreeMakam
from playerframe import PlayerFrame


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

    def _set_design(self, docid):
        self.resize(710, 550)
        self.central_widget = QWidget(self)

        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(2, 2, 2, 2)

        self.player_frame = PlayerFrame(recid=docid, parent=self)
        layout.addWidget(self.player_frame)

        self.setCentralWidget(self.central_widget)

        self.features_dw = QDockWidget(self)
        self.features_dw.setMinimumSize(QtCore.QSize(100, 130))
        self.features_dw.setMaximumSize(QtCore.QSize(400, 524287))
        self.features_dw.setFloating(False)
        self.features_dw.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.features_dw.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.features_dw.setWindowTitle("")
        self.features_dw.setObjectName("dockWidget")

        self.dockWidgetContents = QWidget()
        layout3 = QVBoxLayout(self.dockWidgetContents)
        layout3.setContentsMargins(0, 0, 0, 0)
        layout2 = QVBoxLayout()

        self.feature_tree = FeatureTreeWidget(self.dockWidgetContents)
        self.feature_tree.get_feature_list(docid=str(docid))

        layout2.addWidget(self.feature_tree)
        layout3.addLayout(layout2)

        self.features_dw.setWidget(self.dockWidgetContents)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.features_dw)

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
            else:
                self.player_frame.ts_widget.remove_given_items(
                    self.player_frame.ts_widget.zoom_selection,
                    self.player_frame.ts_widget.rois)
                self.player_frame.ts_widget.is_notes_added = False

        if item == 'metadata':
            if is_checked:
                m_feature = type + '--' + item + '.json'
                m_path = os.path.join(DOCS_PATH, self.docid, m_feature)
                metadata = json.load(open(m_path))

                dlg = QDialog(self)
                layout = QVBoxLayout(dlg)
                mt = MetadataTreeMakam(metadata)
                layout.addWidget(mt)
                dlg.setLayout(layout)
                dlg.show()
            else:
                print 'unchecked'
