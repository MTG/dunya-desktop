import os

from PyQt4 import QtGui, QtCore

DUNYA_ICON = os.path.join(os.path.dirname(__file__), '..', '..', 'ui_files',
                          'icons', 'dunya.svg')
DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'cultures',
                         'documents')


class RecordingModel(QtGui.QStandardItemModel):
    """Recording model is for the results of queries."""
    rec_fetched = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
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

            if os.path.isdir(os.path.join(DOCS_PATH, str(rec['mbid']))):
                check_item.setCheckState(QtCore.Qt.Checked)
                check_item.setEnabled(False)

                # brush = QtGui.QBrush(QtGui.QColor(210, 220, 210))
                # check_item.setBackground(brush)
                # check_item.setEnabled(False)
                # title.setBackground(brush)
                # title.setEnabled(False)
                # artist_item.setBackground(brush)
                # artist_item.setEnabled(False)

            self.insertRow(self.rowCount())
            self.setItem(self.rowCount() - 1, 0, check_item)
            self.setItem(self.rowCount() - 1, 1, title)
            self.setItem(self.rowCount() - 1, 2, artist_item)

    def set_checked(self, rows):
        for row in rows:
            check_item = QtGui.QStandardItem()
            check_item.setCheckState(QtCore.Qt.Checked)
            check_item.setEnabled(False)
            check_item.setToolTip('Already added to main collection...')
            self.setItem(row, 0, check_item)