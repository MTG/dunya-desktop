from __future__ import absolute_import

from PyQt4 import QtGui, QtCore


class RecordingModel(QtGui.QStandardItemModel):
    rec_fetched = QtCore.pyqtSignal(str)

    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        self.setHorizontalHeaderLabels(['', 'Title', 'Artists'])

    def clear_items(self):
        self.clear()
        self.setHorizontalHeaderLabels(['', 'Title', 'Artists'])

    def add_recording(self, work):
        for rec in work['recordings']:
            check_item = QtGui.QStandardItem()
            check_item.setCheckable(True)

            title = QtGui.QStandardItem(rec['title'])

            artists = ''
            rec['artists'] = [dict(tupleized) for tupleized in
                              set(tuple(element.items())
                                  for element in rec['artists'])]

            for artist in rec['artists']:
                artists += artist['name'] + ", "

            artists = artists[:-2]
            artist_item = QtGui.QStandardItem(artists)

            mbid = rec['mbid']
            self.rec_fetched.emit(mbid)

            self.insertRow(self.rowCount())
            self.setItem(self.rowCount() - 1, 0, check_item)
            self.setItem(self.rowCount() - 1, 1, title)
            self.setItem(self.rowCount() - 1, 2, artist_item)
