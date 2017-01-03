import os

from PyQt5.QtWidgets import QTabWidget, QWidget
from PyQt5.QtGui import QFont

from .widgetutilities import set_css

CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'tabwidget.css')


class TabWidget(QTabWidget):
    """Tab widget of related collection/s"""
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self._set_font()
        set_css(self, CSS_PATH)

        # audio tab
        self.tab_audio = QWidget()
        self.addTab(self.tab_audio, "")

        self._retranslate_status_tips()

    def _set_font(self):
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

    def _retranslate_status_tips(self):
        self.tab_audio.setStatusTip("Audio collection of related culture...")
