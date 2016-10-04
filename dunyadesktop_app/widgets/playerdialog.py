from PyQt4 import QtGui, QtCore

from dunyadesktop_app.widgets.waveformwidget import WaveformWidget
from dunyadesktop_app.widgets.melodywidget import MelodyWidget
from dunyadesktop_app.widgets.playerframe import PlayerFrame
import dunyadesktop_app.ui_files.resources_rc


class PlayerDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.resize(850, 550)
        self.setMinimumSize(QtCore.QSize(850, 500))
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.verticalLayout = QtGui.QVBoxLayout(self)

        self.waveform_widget=WaveformWidget()
        self.verticalLayout.addWidget(self.waveform_widget)

        self.pitch_widget = MelodyWidget()
        self.verticalLayout.addWidget(self.pitch_widget)

        self.frame_player = PlayerFrame(self)
        self.verticalLayout.addWidget(self.frame_player)
        QtCore.QMetaObject.connectSlotsByName(self)
