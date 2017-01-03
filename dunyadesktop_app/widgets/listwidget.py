import os
import json

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt5.QtCore import pyqtSignal

from .widgetutilities import set_css

CSS_LISTVIEW = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                            'css', 'listwidget.css')

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')


class DockListWidget(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        set_css(self, CSS_LISTVIEW)

        self.setViewMode(QListWidget.ListMode)


class CollectionsWidget(DockListWidget):
    index_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        DockListWidget.__init__(self, parent)
        # signals
        self.index = self.currentIndex().row()
        self.itemClicked.connect(self.item_clicked)

    def add_collections(self, colls):
        for coll in colls:
            item = QListWidgetItem(coll)
            self.addItem(item)

    def item_clicked(self):
        if not self.currentIndex().row() is self.index:
            self.index = self.currentIndex().row()
            self.index_changed.emit(self.item(self.index).text())

    def update_list(self, colls):
        self.clear()
        self.add_collections(colls)


class CollectionList(DockListWidget):
    def __init__(self, parent=None):
        DockListWidget.__init__(self, parent)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setAcceptDrops(True)

    def add_items(self, coll):
        # first cleans all the items on the list
        self.clear()
        for item in coll:
            path = os.path.join(DOCS_PATH, item,
                                'audioanalysis--metadata.json')
            metadata = json.load(open(path))
            item = QListWidgetItem(metadata['title'])
            self.addItem(item)
