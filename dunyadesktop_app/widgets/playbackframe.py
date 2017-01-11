from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QToolButton,
                             QSlider, QSizePolicy)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt


class PlaybackFrame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent=parent)

        self._set_size_policy()
        self._set_visualization()

        self.horizontalLayout = QHBoxLayout(self)
        self.setMaximumHeight(40)

        self.toolbutton_play = QToolButton(self)
        self.toolbutton_pause = QToolButton(self)
        self._set_buttons()

        self.slider = QSlider(self)
        self._set_slider()

    def _set_size_policy(self):
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)

    def _set_visualization(self):
        self.setStyleSheet("QFrame{\n"
                           "border: 0.5px solid white;\n"
                           "border-radius: 4px;\n"
                           "padding: 2px;\n"
                           "background-color: rgb(25, 25,25);\n"
                           "}")

        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

    def _set_buttons(self):
        self.toolbutton_play.setMinimumSize(QSize(50, 15))
        self.toolbutton_play.setStyleSheet("QToolButton {\n"
                                           "border: none;\n"
                                           "background: transparent;\n"
                                           "}\n"
                                           "\n"
                                           "")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/compmusic/icons/play.png"),
                       QIcon.Normal, QIcon.Off)
        self.toolbutton_play.setIcon(icon)
        self.toolbutton_play.setIconSize(QSize(20, 20))
        self.toolbutton_play.setObjectName("toolButton_play")
        self.horizontalLayout.addWidget(self.toolbutton_play)

        self.toolbutton_pause.setMinimumSize(QSize(50, 15))
        self.toolbutton_pause.setStyleSheet("QToolButton {\n"
                                            "border: none;\n"
                                            "background: transparent;\n"
                                            "}\n"
                                            "")

        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/compmusic/icons/pause.png"),
                        QIcon.Normal, QIcon.Off)
        self.toolbutton_pause.setIcon(icon1)
        self.toolbutton_pause.setIconSize(QSize(20, 20))
        self.horizontalLayout.addWidget(self.toolbutton_pause)

    def _set_slider(self):
        self.slider.setStyleSheet(
            "QSlider::groove:horizontal {\n"
            "border: 1px solid #999999;\n"
            "height: 2px;"
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 "
            "#B1B1B1, stop:1 #c4c4c4);\n "
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

        self.slider.setOrientation(Qt.Horizontal)
        self.horizontalLayout.addWidget(self.slider)
