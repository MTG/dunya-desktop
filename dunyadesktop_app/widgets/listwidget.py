import os
import json

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt5.QtCore import pyqtSignal


CSS_LISTVIEW = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                            'css', 'listwidget.css')

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')


class DockListWidget(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)

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
