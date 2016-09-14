import os
from PyQt4 import QtGui, QtCore

CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'tableview.css')


class TableView(QtGui.QTableView):
    cell_exited = QtCore.pyqtSignal(int, int)
    item_exited = QtCore.pyqtSignal(QtGui.QStandardItem)
    table_scrolled = QtCore.pyqtSignal(QtGui.QStandardItem)

    def __init__(self, *__args):
        QtGui.QTableView.__init__(self, *__args)

        # setting the table for no edit and row selection
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setMouseTracking(True)

        # hiding the vertical headers
        self.verticalHeader().hide()

        # arranging the artist column for being multi-line
        self.setWordWrap(True)
        self.setTextElideMode(QtCore.Qt.ElideMiddle)

        self._last_index = QtCore.QPersistentModelIndex()
        self.viewport().installEventFilter(self)

        self._set_css()
        self._set_font()

        self.horizontal_header = self.horizontalHeader()
        self.horizontal_header.setStretchLastSection(True)
        self.resizeRowsToContents()

    def eventFilter(self, widget, event):
        if widget is self.viewport():
            index = self._last_index
            if event.type() == QtCore.QEvent.MouseMove:
                index = self.indexAt(event.pos())
            elif event.type() == QtCore.QEvent.Leave:
                index = QtCore.QModelIndex()
            if index != self._last_index:
                row = self._last_index.row()
                column = self._last_index.column()
                item = self.model().sourceModel().item(row, column)
                if item is not None:
                    self.item_exited.emit(item)
                self.cell_exited.emit(row, column)
                self._last_index = QtCore.QPersistentModelIndex(index)
        return QtGui.QTableWidget.eventFilter(self, widget, event)

    def wheelEvent(self, QWheelEvent):
        super(TableView, self).wheelEvent(QWheelEvent)

        #row = self._last_index.row()
        #column = self._last_index.column()
        #item = self.model().sourceModel().item(row, column)

        #self.table_scrolled.emit(item)

    def _set_font(self):
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)

    def _set_css(self):
        with open(CSS_PATH) as f:
            css = f.read()
        self.setStyleSheet(css)
