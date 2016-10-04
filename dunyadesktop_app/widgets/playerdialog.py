import sys

from PyQt4 import QtGui, QtCore
from pyqtgraph import GraphicsLayoutWidget

from dunyadesktop_app.widgets.waveformwidget import WaveformWidget
from dunyadesktop_app.widgets.melody_widget import MelodyWidget
import dunyadesktop_app.ui_files.resources_rc


class PlayerDialogDesign(QtGui.QDialog):
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

        self._set_frame()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _set_frame(self):
        self.frame_player = QtGui.QFrame(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_player.sizePolicy().hasHeightForWidth())
        self.frame_player.setSizePolicy(sizePolicy)
        self.frame_player.setStyleSheet("QFrame{\n"
                                        "border: 0.5px solid white;\n"
                                        "border-radius: 4px;\n"
                                        "padding: 2px;\n"
                                        "background-color: rgb(25, 25,25);\n"
                                        "}")
        self.frame_player.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_player.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_player)
        self.frame_player.setMaximumHeight(40)

        self.toolButton_play = QtGui.QToolButton(self.frame_player)
        self.toolButton_play.setMinimumSize(QtCore.QSize(50, 15))
        self.toolButton_play.setStyleSheet("QToolButton {\n"
                                           "border: none;\n"
                                           "background: transparent;\n"
                                           "}\n"
                                           "\n"
                                           "")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/compmusic/icons/play.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_play.setIcon(icon)
        self.toolButton_play.setIconSize(QtCore.QSize(20, 20))
        self.toolButton_play.setObjectName("toolButton_play")
        self.horizontalLayout.addWidget(self.toolButton_play)

        self.toolButton_pause = QtGui.QToolButton(self.frame_player)
        self.toolButton_pause.setMinimumSize(QtCore.QSize(50, 15))
        self.toolButton_pause.setStyleSheet("QToolButton {\n"
                                            "border: none;\n"
                                            "background: transparent;\n"
                                            "}\n"
                                            "")

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/compmusic/icons/pause.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_pause.setIcon(icon1)
        self.toolButton_pause.setIconSize(QtCore.QSize(20, 20))
        self.horizontalLayout.addWidget(self.toolButton_pause)

        self.horizontalSlider_playback = QtGui.QSlider(self.frame_player)
        self.horizontalSlider_playback.setStyleSheet(
            "QSlider::groove:horizontal {\n"
            "border: 1px solid #999999;\n"
            "height: 2px;"
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);\n"
            "margin: 2px 0;\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal {\n"
            "background: solid black;\n"
            "border: 1px solid black;\n"
            "width: 5px;\n"
            "margin: -2px 0;"
            "border-radius: 3px;\n"
            "}")

        self.horizontalSlider_playback.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalLayout.addWidget(self.horizontalSlider_playback)
        self.verticalLayout.addWidget(self.frame_player)


app = QtGui.QApplication(sys.argv)
dialog = PlayerDialogDesign()
dialog.show()
app.exec_()
