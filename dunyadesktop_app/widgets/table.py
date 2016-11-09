import os
import platform

from PyQt4 import QtGui, QtCore

if platform.system() == 'Linux':
    FONT_SIZE = 9
else:
    FONT_SIZE = 12

CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'tableview.css')

dunya_icon = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'dunya.svg')


class TableView(QtGui.QTableView):
    def __init__(self, *__args):
        QtGui.QTableView.__init__(self, *__args)

        # setting the table for no edit and row selection
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setMouseTracking(True)

        # hiding the vertical headers
        self.verticalHeader().hide()

        # arranging the artist column for being multi-line
        self.setWordWrap(True)
        self.setTextElideMode(QtCore.Qt.ElideMiddle)

        self.horizontalHeader().setStretchLastSection(True)
        self.setColumnWidth(0, 10)

        self._last_index = QtCore.QPersistentModelIndex()
        self.viewport().installEventFilter(self)

        self._set_css()
        self._set_font()

    def _set_font(self):
        font = QtGui.QFont()
        font.setPointSize(FONT_SIZE)
        self.setFont(font)

    def _set_css(self):
        with open(CSS_PATH) as f:
            css = f.read()
        self.setStyleSheet(css)


class TableViewResults(TableView):
    """Table view widget of query results."""
    def __init__(self, parent=None):
        TableView.__init__(self)
        self.setSortingEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragOnly)

        self.horizontal_header = self.horizontalHeader()
        self._set_horizontal_header()

        self.menu = QtGui.QMenu(self)
        self._set_menu()
        self.add_maincoll = QtGui.QAction("Add to main collection", self)

        self.open_dunya = QtGui.QAction("Open on Player", self)
        self.open_dunya.setIcon(QtGui.QIcon(dunya_icon))

        self.menu.addAction(self.add_maincoll)
        self.menu.addAction(self.open_dunya)

    def _set_menu(self):
        self.add_maincoll = QtGui.QAction("Add to main collection", self)

        self.menu.addSeparator()

        self.open_dunya = QtGui.QAction("Open on Player", self)
        self.open_dunya.setIcon(QtGui.QIcon(dunya_icon))

    def _set_horizontal_header(self):
        self.horizontal_header.setStretchLastSection(True)
        self.horizontal_header.hide()

    def contextMenuEvent(self, event):
        """Pops up the context menu when the right button is clicked."""
        if self.selectionModel().selection().indexes():
            for index in self.selectionModel().selection().indexes():
                row, column = index.row(), index.column()
        self.index = index
        self.menu.popup(QtGui.QCursor.pos())


class TableWidget(QtGui.QTableWidget, TableView):
    def __init__(self):
        #TableView.__init__(self)
        QtGui.QTableWidget.__init__(self)
        TableView.__init__(self)
        # setting the table for no edit and row selection
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setMouseTracking(True)

        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setAcceptDrops(True)
