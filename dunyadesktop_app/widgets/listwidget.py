import os

from PyQt4 import QtGui, QtCore

CSS_LISTVIEW = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                            'css', 'listwidget.css')


class CollectionsWidget(QtGui.QListWidget):
    index_changed = QtCore.pyqtSignal(str)

    def __init__(self):
        QtGui.QListView.__init__(self)

        self._set_css(self, CSS_LISTVIEW)

        self.setViewMode(QtGui.QListView.ListMode)
        self.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.startDrag(QtCore.Qt.CopyAction)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

        # signals
        self.index = self.currentIndex().row()
        self.itemClicked.connect(self.item_clicked)

    @staticmethod
    def _set_css(obj, css_path):
        with open(css_path) as f:
            css = f.read()
        obj.setStyleSheet(css)

    def add_collections(self, colls):
        for coll in colls:
            item = QtGui.QListWidgetItem(coll)
            self.addItem(item)

    def item_clicked(self):
        if not self.currentIndex().row() is self.index:
            self.index = self.currentIndex().row()
            self.index_changed.emit(self.item(self.index).text())
