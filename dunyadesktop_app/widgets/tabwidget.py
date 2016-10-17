import os

from PyQt4 import QtGui

from dunyadesktop_app.utilities import utilities

CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'tabwidget.css')

class TabWidget(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self._set_font()
        self._set_css()

        # audio tab
        self.tab_audio = QtGui.QWidget()
        self.addTab(self.tab_audio, utilities._fromUtf8(""))

        self._retranslate_status_tips()

    def _set_font(self):
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)

    def _set_css(self):
        with open(CSS_PATH)as f:
            css = f.read()
        self.setStyleSheet(css)

    def _retranslate_status_tips(self):
        self.tab_audio.setStatusTip("Audio collection of related culture...")
