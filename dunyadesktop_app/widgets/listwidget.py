import os

from PyQt4 import QtGui, QtCore

CSS_LISTVIEW = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                            'css', 'listwidget.css')


class CollectionsWidget(QtGui.QListWidget):
    def __init__(self):
        QtGui.QListView.__init__(self)

        self._set_css(self, CSS_LISTVIEW)

        self.setViewMode(QtGui.QListView.ListMode)
        self.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.startDrag(QtCore.Qt.CopyAction)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    @staticmethod
    def _set_css(obj, css_path):
        with open(css_path) as f:
            css = f.read()
        obj.setStyleSheet(css)

    def add_collections(self, colls):
        for coll in colls:
            item = QtGui.QListWidgetItem(coll)
            self.addItem(item)
