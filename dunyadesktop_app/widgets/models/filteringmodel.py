from PyQt4 import QtGui


class FilteringModel(QtGui.QStandardItemModel):
    """This model is contains the attributes"""
    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)

    def add_items(self, attribute):
        self.setRowCount(len(attribute))

        for row, item in enumerate(attribute):
            name = QtGui.QStandardItem(item['name'])
            self.setItem(row, 0, name)
