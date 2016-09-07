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

    def _set_font(self):
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)

    def _set_css(self):
        with open(CSS_PATH)as f:
            css = f.read()
        self.setStyleSheet(css)


class TabWidgetMakam(TabWidget):
    def __init__(self, parent=None):
        super(TabWidgetMakam, self).__init__(parent)
        self._add_tabs()

    def _add_tabs(self):
        # score tab
        self.tab_score = QtGui.QWidget()
        self.addTab(self.tab_score, utilities._fromUtf8(""))

        # audio tab
        self.tab_audio = QtGui.QWidget()
        self.addTab(self.tab_audio, utilities._fromUtf8(""))
