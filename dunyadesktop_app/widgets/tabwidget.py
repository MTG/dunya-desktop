from PyQt5.QtWidgets import QTabWidget, QWidget
from PyQt5.QtGui import QFont


class TabWidget(QTabWidget):
    """Tab widget of related collection/s"""
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self._set_font()

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
