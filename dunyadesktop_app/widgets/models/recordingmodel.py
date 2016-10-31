import os

from PyQt4 import QtGui, QtCore

DUNYA_ICON = os.path.join(os.path.dirname(__file__), '..', '..', 'ui_files',
                          'icons', 'dunya.svg')


class RecordingModel(QtGui.QStandardItemModel):
    """Recording model is for the results of queries."""
    rec_fetched = QtCore.pyqtSignal(str)

    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        self.set_columns()

    def set_columns(self):
        self.setHorizontalHeaderLabels(['', 'Title', 'Artists'])

    def clear_items(self):
        self.clear()
        self.set_columns()

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

            dunya = QtGui.QStandardItem()
            dunya.setIcon(QtGui.QIcon(DUNYA_ICON))

            mbid = rec['mbid']
            self.rec_fetched.emit(mbid)

            self.insertRow(self.rowCount())
            self.setItem(self.rowCount() - 1, 0, check_item)
            self.setItem(self.rowCount() - 1, 1, title)
            self.setItem(self.rowCount() - 1, 2, artist_item)
