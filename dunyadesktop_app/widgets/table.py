import os
from PyQt4 import QtGui, QtCore

CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'tableview.css')

class TableWidget(QtGui.QTableWidget):
    def __init__(self, *__args):
        QtGui.QTableWidget.__init__(self, *__args)

        # setting the table for no edit and row selection
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        # hiding the vertical headers
        self.verticalHeader().hide()

        # arranging the artist column for being multi-line
        self.setWordWrap(True)
        self.setTextElideMode(QtCore.Qt.ElideMiddle)

        self._set_css()

    def _set_css(self):
        with open(CSS_PATH) as f:
            css = f.read()
        self.setStyleSheet(css)
