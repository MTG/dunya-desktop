import os

from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QApplication,
                             QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal

from cultures.makam.utilities import get_filenames_in_dir

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')
MB_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                       'icons', 'musicbrainzicon.svg')


class FeatureTreeWidget(QTreeWidget):
    item_checked = pyqtSignal(str, str, bool)

    def __init__(self, parent=None):
        QTreeWidget.__init__(self, parent=parent)
        self.feature_dict = {}
        self.is_ready = False

        self._set_tree_widget()
        self.expanded.connect(lambda: self.resizeColumnToContents(0))
        self.itemChanged.connect(self._item_changed)

    def _item_changed(self, item, column):
        if self.is_ready:
            type = item.parent().data(0, 0)
            it = item.data(0, 0)
            check_state = item.checkState(column)
            if check_state == 2:
                is_checked = True
            else:
                is_checked = False
            self.item_checked.emit(type, it, is_checked)

    def _set_tree_widget(self):
        header = QTreeWidgetItem(['Features', 'Visualize'])
        self.setHeaderItem(header)
        self.setMinimumWidth(250)

    def get_feature_list(self, docid):
        fullnames, folders, names = get_filenames_in_dir(
            os.path.join(DOCS_PATH, docid), keyword='*.json')

        for name in names:
            f_type = name.split('--')[0].strip()
            f_name = name.split('--')[1].strip().split('.')[0].strip()

            try:
                f_list = self.feature_dict[f_type]
                f_list.append(f_name)
                self.feature_dict[f_type] = f_list
            except KeyError:
                f_list = [f_name]
                self.feature_dict[f_type] = f_list
        self.add_items()

    def add_items(self):
        if self.feature_dict:
            for key in self.feature_dict.keys():
                root = QTreeWidgetItem(self, [key])

                for type in self.feature_dict[key]:
                    feature = QTreeWidgetItem(root, ['Feature Types'])
                    feature.setData(0, Qt.EditRole, type)
                    feature.setCheckState(1, Qt.Unchecked)

        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)

        self.is_ready = True


class MBItem(QPushButton):
    def __init__(self, mb_link):
        QPushButton.__init__(self)

        self.setFixedWidth(20)
        self.setFixedHeight(20)
        self.setIcon(QIcon(MB_ICON))

        self.mb_link = mb_link
        self.clicked.connect(self._button_clicked)

    def _button_clicked(self):
        print('clicked', self.mb_link)


class MetadataTreeMakam(QTreeWidget):
    MB = 'https://musicbrainz.org/'

    def __init__(self, metadata_dict, parent=None):
        QTreeWidget.__init__(self, parent=parent)
        self.metadata_dict = metadata_dict

        header = QTreeWidgetItem(['Metadata', '', '', '', ''])
        self.setHeaderItem(header)
        self._parse_dict()

    def _parse_dict(self):
        self.root_title = QTreeWidgetItem(self, ['Title'])
        mbid_link = self.MB + "recording/" + self.metadata_dict['mbid']
        title = QTreeWidgetItem(self.root_title, ['Title'])
        title.setData(1, Qt.EditRole, self.metadata_dict['title'])
        title.setData(2, Qt.EditRole, mbid_link)

        # parsing and adding musical attributes
        self.root_ma = QTreeWidgetItem(self, ['Musical Attribute'])
        self.root_release = QTreeWidgetItem(self, ['Releases'])
        self.root_art_cred = QTreeWidgetItem(self, ['Artist Credits'])
        self.root_artists = QTreeWidgetItem(self, ['Artists'])
        self.root_work = QTreeWidgetItem(self, ['Works'])

        for att in ['makam', 'usul', 'form']:
            try:
                for item in self.metadata_dict[att]:
                    self.__add_musical_attribute(self.root_ma, att.title(),
                                                 item)
            except KeyError:
                print 'no', att

        for att in [(self.root_release, 'releases', 'Release'),
                    (self.root_art_cred, 'artist_credits', 'Credits'),
                    (self.root_work, 'works', 'Work')]:
            try:
                for item in self.metadata_dict[att[1]]:
                    self.__add_to_tree(att[0], att[1], att[2], item)
            except KeyError:
                print 'No', att

        # artists
        try:
            for item in self.metadata_dict['artists']:
                mb_artist = self.MB + 'artist/' + item['mbid']
                artist = QTreeWidgetItem(self.root_artists, ['Artist'])
                artist.setData(1, Qt.EditRole, item['type'])
                artist.setData(2, Qt.EditRole, item['name'])

                att_list = u''
                for item in item['attribute-list']:
                    att_list += item
                artist.setData(3, Qt.EditRole, att_list)
                artist.setData(4, Qt.EditRole, mb_artist)

        except KeyError:
            print 'no artistssss'

        # audio attributes
        self.root_audio = QTreeWidgetItem(self, ['Audio'])
        fs = self.metadata_dict['sampling_frequency']
        bit_rate = self.metadata_dict['bit_rate']
        duration = self.metadata_dict['duration']

        fs_item = QTreeWidgetItem(self.root_audio, ['Sampling Frequency'])
        fs_item.setData(1, Qt.EditRole, fs)

        bit_rate_item = QTreeWidgetItem(self.root_audio, ['Bit Rate'])
        bit_rate_item.setData(1, Qt.EditRole, bit_rate)

        duration_item = QTreeWidgetItem(self.root_audio, ['Duration'])
        duration_item.setData(1, Qt.EditRole, duration)

    def __add_musical_attribute(self, root, name, item):
        widget_item = QTreeWidgetItem(root, [name])
        try:
            self.__set_item_widget(widget_item, 1, item, 'mb_attribute')
        except KeyError:
            self.__set_item_widget(widget_item, 1, item, 'mb_tag')

        mb_item = MBItem(item['source'])
        self.setItemWidget(widget_item, 2, mb_item)

    def __add_to_tree(self, root, key, name, item):
        mb_link = self.MB + 'release/' + item['mbid']
        item_widget = QTreeWidgetItem(root, [name])

        try:
            self.__set_item_widget(item_widget, 1, item, 'title')
        except KeyError:
            self.__set_item_widget(item_widget, 1, item, 'name')

        mb_item = MBItem(mb_link=mb_link)
        self.setItemWidget(item_widget, 2, mb_item)

    @staticmethod
    def __set_item_widget(widget, col, item, key):
        widget.setData(col, Qt.EditRole, item[key])
