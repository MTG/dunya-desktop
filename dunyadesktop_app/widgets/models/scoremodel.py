import os
import json

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem


DUNYA_ICON = os.path.join(os.path.dirname(__file__), '..', '..', 'ui_files',
                          'icons', 'dunya.svg')
DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'cultures',
                         'documents')


class ScoreModel(QStandardItemModel):
    """Recording model is for the results of queries."""
    work_fetched = pyqtSignal(str)

    def __init__(self, parent=None):
        QStandardItemModel.__init__(self, parent)
        self.set_columns()

    def set_columns(self):
        self.setHorizontalHeaderLabels(['', 'Title', 'Composer'])

    def clear_items(self):
        self.clear()
        self.set_columns()

    def add_score(self, work):
        check_item = QStandardItem()
        check_item.setCheckable(True)

        title = QStandardItem(work['title'])

        composers = ''
        for composer in work['composers']:
            composers += composer['name'] + ","
        composers_item = QStandardItem(composers)

        mbid = work['mbid']
        self.work_fetched.emit(mbid)

        if os.path.isdir(os.path.join(DOCS_PATH, str(work['mbid']))):
            check_item.setCheckState(Qt.Checked)
            check_item.setEnabled(False)

        self.insertRow(self.rowCount())
        self.setItem(self.rowCount() - 1, 0, check_item)
        self.setItem(self.rowCount() - 1, 1, title)
        self.setItem(self.rowCount() - 1, 2, composers_item)

    def set_checked(self, rows):
        for row in rows:
            check_item = QStandardItem()
            check_item.setCheckState(Qt.Checked)
            check_item.setEnabled(False)
            check_item.setToolTip('Already added to main collection...')
            self.setItem(row, 0, check_item)


class CollectionTableModel(QStandardItemModel):
    def __init__(self):
        QStandardItemModel.__init__(self)
        self.set_columns()
        self.items = {}

    def set_columns(self):
        self.setHorizontalHeaderLabels(['', 'Title', 'Artists', 'Makam',
                                        'Usul', 'Form'])

    def clear_items(self):
        self.clear()
        self.set_columns()
        self.items = {}

    def add_recording(self, recording):
        for index, mbid in enumerate(recording):
            metadata = CollectionTableModel._get_metadata(self, mbid[0], index)
            self._add_item(metadata)

    @staticmethod
    def _get_metadata(self, mbid, index):
        path = os.path.join(DOCS_PATH, mbid, 'audioanalysis--metadata.json')
        metadata = json.load(open(path))

        metadata_dict = {}
        mbid = metadata['mbid']
        metadata_dict['title'] = metadata['title']
        metadata_dict['artists'] = CollectionTableModel.parse_artists(metadata)
        metadata_dict['makam'] = \
            CollectionTableModel.parse_mattribute(metadata, 'makam')
        metadata_dict['usul'] = \
            CollectionTableModel.parse_mattribute(metadata, 'usul')
        metadata_dict['form'] = \
            CollectionTableModel.parse_mattribute(metadata, 'form')
        self.items[index] = mbid

        return metadata_dict

    def _add_item(self, metadata):
        self.insertRow(self.rowCount())
        self.setItem(self.rowCount()-1, 0,
                     self._make_item(str(self.rowCount())))
        self.setItem(self.rowCount()-1, 1, self._make_item(metadata['title']))
        self.setItem(self.rowCount()-1, 2,
                     self._make_item(metadata['artists']))
        self.setItem(self.rowCount()-1, 3, self._make_item(metadata['makam']))
        self.setItem(self.rowCount()-1, 4, self._make_item(metadata['usul']))
        self.setItem(self.rowCount()-1, 5, self._make_item(metadata['form']))

    @staticmethod
    def _make_item(text):
        return QStandardItem(text)

    @staticmethod
    def parse_artists(metadata):
        values = metadata['artists']
        v = []
        return_s = ''
        for k in values:
            v.append(k['name'])
        for a in v:
            return_s += a + ', '
        return return_s[:-2]

    @staticmethod
    def parse_mattribute(metadata, key):
        for value in metadata[key]:
            try:
                mattribute = value['mb_attribute']
                return mattribute
            except KeyError:
                pass
