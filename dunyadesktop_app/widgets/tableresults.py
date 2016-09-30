from PyQt4 import QtGui

from .table import TableView


class TableViewResults(TableView):
    def __init__(self, parent=None):
        TableView.__init__(self)

        self.setSortingEnabled(True)

        self.horizontal_header = self.horizontalHeader()
        self.horizontal_header.setStretchLastSection(True)
        self.horizontal_header.hide()

        self.menu = QtGui.QMenu(self)

    def contextMenuEvent(self, event):
        if self.selectionModel().selection().indexes():
            for i in self.selectionModel().selection().indexes():
                row, column = i.row(), i.column()
        print(row)
