import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout,
                             QFrame, QDockWidget, QPushButton)
from PyQt5.QtCore import Qt, QMetaObject

from treewidget import FeatureTreeWidget
from playerdialog import PlayerDialog

class PlayerMainWindow(QMainWindow):
    def __init__(self, docid, parent=None):
        QMainWindow.__init__(self, parent=parent)

        self.resize(710, 550)
        self.centralwidget = QWidget(self)

        layout = QVBoxLayout(self.centralwidget)
        layout.setContentsMargins(2, 2, 2, 2)


        self.player_frame = PlayerDialog(recid=docid, parent=self)
        layout.addWidget(self.player_frame)

        self.setCentralWidget(self.centralwidget)

        button = QPushButton(self)
        l = QVBoxLayout()
        l.addWidget(button)
        self.player_frame.setLayout(l)

        self.features_dw = QDockWidget(self)
        self.features_dw.setMinimumSize(QtCore.QSize(100, 130))
        self.features_dw.setMaximumSize(QtCore.QSize(400, 524287))
        self.features_dw.setFloating(False)
        self.features_dw.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
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

        self.addDockWidget(Qt.DockWidgetArea(1), self.features_dw)

        QMetaObject.connectSlotsByName(self)

    def closeEvent(self, QCloseEvent):
        self.player_frame.closeEvent(QCloseEvent)