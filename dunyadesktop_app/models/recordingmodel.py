from __future__ import absolute_import

from PyQt4 import QtGui, QtCore


class RecordingModel(QtGui.QStandardItemModel):
    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        self.setColumnCount(2)

    def add_recording(self, work):
        for rec in work['recordings']:
            artists = rec['artists']
            mbid = QtGui.QStandardItem(rec['mbid'])
            title = QtGui.QStandardItem(rec['title'])
            self.insertRow(self.rowCount(), title)
            self.setItem(self.rowCount()-1, 1, mbid)