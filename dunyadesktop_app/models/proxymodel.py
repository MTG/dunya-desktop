from PyQt4 import QtGui


class SortFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        QtGui.QSortFilterProxyModel.__init__(self)
