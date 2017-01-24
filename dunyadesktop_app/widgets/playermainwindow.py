import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout,
                             QDockWidget)
from PyQt5.QtCore import Qt, QMetaObject

from treewidget import FeatureTreeWidget
from playerframe import PlayerFrame


class PlayerMainWindow(QMainWindow):
    def __init__(self, docid, parent=None):
        QMainWindow.__init__(self, parent=parent)
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

    def closeEvent(self, QCloseEvent):
        self.player_frame.closeEvent(QCloseEvent)

    def evaluate_checked_signal(self, type, item, is_checked):
        if item == 'pitch' or item == 'pitch_filtered':
            if is_checked:
                self.player_frame.plot_1d_data(type, item)
            else:
                self.player_frame.ts_widget.zoom_selection.clearPlots()
                self.player_frame.is_pitch_plotted = False
                self.player_frame.ts_widget.pitch_plot = None
        if item == 'tonic':
            if is_checked:
                self.player_frame.plot_1d_data(type, item)
            else:
                if hasattr(self.player_frame.ts_widget, 'tonic_line'):
                    self.player_frame.ts_widget.zoom_selection.removeItem(
                        self.player_frame.ts_widget.tonic_line)
                    del self.player_frame.ts_widget.tonic_line

        if item == 'notes':
            if is_checked:
                self.player_frame.add_1d_roi_items(type, item)


app = QApplication(sys.argv)
ply = PlayerMainWindow(docid='f09db163-2549-4f67-bfb3-7b626f20a8c2')
ply.show()
app.exec_()
