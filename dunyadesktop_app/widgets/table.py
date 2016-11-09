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
        #self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
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

    def get_selected_rows(self):
        selectedRows = []
        for item in self.selectionModel().selectedRows():
            if item.row() not in selectedRows:
                selectedRows.append(item.row())
        selectedRows.sort()
        return selectedRows


class TableWidget(QtGui.QTableWidget, TableView):
    def __init__(self):
        QtGui.QTableWidget.__init__(self)
        TableView.__init__(self)
        self.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)

        self.setColumnCount(3)

        self.last_drop_row = None

    def dropMimeData(self, row, col, mimeData, action):
        self.last_drop_row = row
        return True

    def dropEvent(self, event):
        # The QTableWidget from which selected rows will be moved
        sender = event.source()

        # Default dropEvent method fires dropMimeData with appropriate
        # parameters (we're interested in the row index).
        super(QtGui.QTableWidget, self).dropEvent(event)
        # Now we know where to insert selected row(s)
        drop_row = self.last_drop_row
        selected_rows = sender.get_selected_rows()

        # Allocate space for transfer
        for _ in selected_rows:
            self.insertRow(drop_row)

        # if sender == receiver (self), after creating new empty rows selected
        # rows might change their locations
        sel_rows_offsets = [0 if self != sender or srow < drop_row
                            else len(selected_rows) for srow in selected_rows]
        selected_rows = [row + offset for row, offset in zip(selected_rows,
                                                             sel_rows_offsets)]

        # copy content of selected rows into empty ones
        for i, srow in enumerate(selected_rows):
            for j in range(self.columnCount()):
                item = sender.model().sourceModel().item(srow, j)
                if item:
                    source = QtGui.QTableWidgetItem(item.text())
                    self.setItem(drop_row + i, j, source)

        # delete selected rows
        for srow in reversed(selected_rows):
            sender.model().removeRow(srow)

        event.accept()

