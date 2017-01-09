import sys
import os

from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QApplication,
                             QCheckBox)
from PyQt5.QtCore import Qt

from cultures.makam.utilities import get_filenames_in_dir


DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')


class CheckBox(QCheckBox):
    def __init__(self, parent=None):
        QCheckBox.__init__(self, parent)
        self.stateChanged.connect(self._state_changed)

    def _state_changed(self, state):
        print self.parent()
        #print(self.parent().currentItem())


class FeatureWidget(QTreeWidget):

    def __init__(self, parent=None):
        QTreeWidget.__init__(self, parent=parent)
        self.feature_dict = {}
        self.is_ready = False

        self._set_tree_widget()
        self.expanded.connect(lambda: self.resizeColumnToContents(0))
        self.itemChanged.connect(self._item_changed)

    def _item_changed(self, item, column):
        if self.is_ready:
            print item.data(0, 0), item.checkState(column)

    def _set_tree_widget(self):
        header = QTreeWidgetItem(['Features', 'Visualize'])
        self.setHeaderItem(header)
        self.setMinimumWidth(250)

    def get_feature_list(self, docid):
        fullnames, folders, names = get_filenames_in_dir(
            os.path.join(DOCS_PATH, docid),keyword='*.json')

        for name in names:
            f_type = name.split('--')[0].strip()
            f_name = name.split('--')[1].strip().split('.')[0].strip()

            try:
                f_list = self.feature_dict[f_type]
                f_list.append(f_name)
                self.feature_dict[f_type] = f_list
            except KeyError:
                f_list= [f_name]
                self.feature_dict[f_type] = f_list

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


app = QApplication(sys.argv)
t = FeatureWidget()
t.get_feature_list('519264d7-255d-41cf-9c70-6ff3e7ba0ca5')
t.add_items()
t.show()
app.exec_()
