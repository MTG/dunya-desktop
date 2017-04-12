import os

from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QToolButton,
                             QSlider, QSizePolicy, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt


PLAY_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'playback', 'play-button_gray.svg')
PAUSE_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'playback', 'pause_gray.svg')


class PlaybackFrame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent=parent)

        self._set_size_policy()
        self._set_visualization()

        vertical_layout = QVBoxLayout(self)
        # self.hor_layout_top = QHBoxLayout()
        self.hor_layout_bottom = QHBoxLayout()
        # self.setMaximumHeight(40)

        self.toolbutton_play = QToolButton(self)
        self.toolbutton_pause = QToolButton(self)
        self._set_buttons()

        self.slider = QSlider(self)
        self._set_slider()

        #vertical_layout.addLayout(self.hor_layout_top)
        vertical_layout.addLayout(self.hor_layout_bottom)

    def _set_size_policy(self):
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)

    def _set_visualization(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

    def _set_buttons(self):
        self.toolbutton_play.setMinimumSize(QSize(50, 15))

        self.toolbutton_play.setIcon(QIcon(PLAY_ICON))
        self.toolbutton_play.setIconSize(QSize(20, 20))
        self.toolbutton_play.setObjectName("toolButton_play")
        self.hor_layout_bottom.addWidget(self.toolbutton_play)

        self.toolbutton_pause.setMinimumSize(QSize(50, 15))

        self.toolbutton_pause.setIcon(QIcon(PAUSE_ICON))
        self.toolbutton_pause.setIconSize(QSize(20, 20))
        self.hor_layout_bottom.addWidget(self.toolbutton_pause)

    def _set_slider(self):
        self.slider.setOrientation(Qt.Horizontal)
        self.hor_layout_bottom.addWidget(self.slider)
