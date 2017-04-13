import os

from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QToolButton,
                             QSlider, QSizePolicy, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt


PLAY_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'playback', 'play-button_gray.svg')
PAUSE_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'playback', 'pause_gray.svg')
REWIND_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                           'icons', 'playback', 'rewind_gray.svg')
NEXT_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                         'icons', 'playback', 'next_gray.svg')
REPLAY_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                           'icons', 'playback', 'replay_gray.svg')


class PlaybackFrame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent=parent)

        self._set_size_policy()
        self._set_visualization()

        vertical_layout = QVBoxLayout(self)
        self.hor_layout_top = QHBoxLayout()
        self.hor_layout_bottom = QHBoxLayout()
        self.setMaximumHeight(150)

        self.button_play = QToolButton()
        self.button_pause = QToolButton()
        self.button_rewind = QToolButton()
        self.button_next = QToolButton()
        self.button_replay = QToolButton()


        self.hor_layout_top.addWidget(self.button_rewind)
        self.hor_layout_top.addWidget(self.button_play)
        self.hor_layout_top.addWidget(self.button_pause)
        self.hor_layout_top.addWidget(self.button_next)
        self.hor_layout_top.addWidget(self.button_replay)

        self._set_buttons()

        self.slider = QSlider()
        self._set_slider()

        vertical_layout.addLayout(self.hor_layout_top)
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
        self.button_play.setIcon(QIcon(PLAY_ICON))
        self.button_pause.setIcon(QIcon(PAUSE_ICON))
        self.button_rewind.setIcon(QIcon(REWIND_ICON))
        self.button_next.setIcon(QIcon(NEXT_ICON))
        self.button_replay.setIcon(QIcon(REPLAY_ICON))

    def _set_slider(self):
        self.slider.setOrientation(Qt.Horizontal)
        self.hor_layout_bottom.addWidget(self.slider)
