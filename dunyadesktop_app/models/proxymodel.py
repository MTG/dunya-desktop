from __future__ import absolute_import

from PyQt4 import QtGui, QtCore

class SortFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        QtGui.QSortFilterProxyModel.__init__(self)

    def filtering_the_table(self, text):
        reg_exp = QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive)
        self.setFilterRegExp(reg_exp)
