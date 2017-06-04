import os

from PyQt5.QtGui import QStandardItemModel, QStandardItem


class CollectionModel(QStandardItemModel):
    def __init__(self):
        QStandardItemModel.__init__(self)
        self.set_columns()

    def set_columns(self):
        self.setHorizontalHeaderLabels(['', 'Title', 'Composer', 'Artists'])