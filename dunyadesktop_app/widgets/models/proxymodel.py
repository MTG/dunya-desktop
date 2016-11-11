from PyQt4 import QtGui, QtCore


class SortFilterProxyModel(QtGui.QSortFilterProxyModel):
    """Sort filter model is for filtering the table of query results."""
    def __init__(self, QObject_parent=None):
        QtGui.QSortFilterProxyModel.__init__(self, QObject_parent)

    def filter_table(self, text):
        reg_exp = QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive)
        self.setFilterRegExp(reg_exp)
