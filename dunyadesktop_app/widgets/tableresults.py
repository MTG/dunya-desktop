import os

from PyQt4 import QtGui

from .table import TableView

dunya_icon = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                                'icons', 'dunya.svg')

class TableViewResults(TableView):
    def __init__(self, parent=None):
        TableView.__init__(self)
        self.setSortingEnabled(True)

        self.horizontal_header = self.horizontalHeader()
        self._set_horizontal_header()

        self.menu = QtGui.QMenu(self)
        open_dunya = QtGui.QAction("Open on Player", self)
        open_dunya.setIcon(QtGui.QIcon(dunya_icon))
        self.menu.addAction(open_dunya)

    def _set_horizontal_header(self):
        self.horizontal_header.setStretchLastSection(True)
        self.horizontal_header.hide()

    def contextMenuEvent(self, event):
        if self.selectionModel().selection().indexes():
            for index in self.selectionModel().selection().indexes():
                row, column = index.row(), index.column()
        self.menu.popup(QtGui.QCursor.pos())