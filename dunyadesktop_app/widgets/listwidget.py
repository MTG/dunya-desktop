import os
import json

from PyQt4 import QtGui, QtCore

CSS_LISTVIEW = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                            'css', 'listwidget.css')

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')


class DockListWidget(QtGui.QListWidget):
    def __init__(self):
        QtGui.QListView.__init__(self)

        self._set_css(self, CSS_LISTVIEW)

        self.setViewMode(QtGui.QListView.ListMode)

    @staticmethod
    def _set_css(obj, css_path):
        with open(css_path) as f:
            css = f.read()
        obj.setStyleSheet(css)


class CollectionsWidget(DockListWidget):
    index_changed = QtCore.pyqtSignal(str)

    def __init__(self):
        DockListWidget.__init__(self)
        # signals
        self.index = self.currentIndex().row()
        self.itemClicked.connect(self.item_clicked)

    def add_collections(self, colls):
        for coll in colls:
            item = QtGui.QListWidgetItem(coll)
            self.addItem(item)

    def item_clicked(self):
        if not self.currentIndex().row() is self.index:
            self.index = self.currentIndex().row()
            self.index_changed.emit(self.item(self.index).text())


class CollectionList(DockListWidget):
    def __init__(self):
        DockListWidget.__init__(self)
        self.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.setAcceptDrops(True)

    def add_items(self, coll):
        # first cleans all the items on the list
        self.clear()
        for item in coll:
            path = os.path.join(DOCS_PATH, item,
                                'audioanalysis--metadata.json')
            metadata = json.load(open(path))
            item = QtGui.QListWidgetItem(metadata['title'])
            self.addItem(item)
