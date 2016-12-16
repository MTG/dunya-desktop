from PyQt5.QtGui import QStandardItemModel, QStandardItem


class FilteringModel(QStandardItemModel):
    """This model is contains the attributes"""
    def __init__(self, parent=None):
        QStandardItemModel.__init__(self, parent)

    def add_items(self, attribute):
        self.setRowCount(len(attribute))

        for row, item in enumerate(attribute):
            name = QStandardItem(item['name'])
            self.setItem(row, 0, name)
