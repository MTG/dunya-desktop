from __future__ import absolute_import
import os

from PyQt4 import QtGui, QtCore

from .filteringdialog import FilteringDialog

CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'combobox.css')


class ComboBox(QtGui.QComboBox):
    def __init__(self, parent):
        QtGui.QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.setInsertPolicy(QtGui.QComboBox.NoInsert)

        self._set_css()
        self.dialog_filtering = FilteringDialog()
        self.dialog_filtering.table_attribute.doubleClicked.connect(
                                                            self.set_selection)
        self.dialog_filtering.ok_button_clicked.connect(
            lambda: self.set_selection(self.dialog_filtering.selection))

    def _set_css(self):
        with open(CSS_PATH) as f:
            css = f.read()
        self.setStyleSheet(css)

    def wheelEvent(self, QWheelEvent):
        pass

    def mousePressEvent(self, QMouseEvent):
        self.dialog_filtering.attribute = self.attribute
        self.dialog_filtering.setWindowTitle("")
        self.dialog_filtering.filtering_model.add_items(self.attribute)
        self.dialog_filtering.exec_()

    def set_placeholder_text(self, text):
        font = QtGui.QFont()
        font.setPointSize(10)

        self.lineEdit().setPlaceholderText(text)
        self.lineEdit().setFont(font)

    def add_items(self, attribute):
        self.attribute = attribute
        for att in self.attribute:
            self.addItem(att['name'])
        self.setCurrentIndex(-1)

    def get_attribute_id(self):
        index = self.currentIndex()
        if index is not -1:
            try:
                return self.attribute[index]['uuid']
            except:
                return self.attribute[index]['mbid']

        else:
            return ''

    def set_selection(self, index):
        try:
            index_row = index.row()
        except:
            index_row = index
        self.setCurrentIndex(index_row)
        self.lineEdit().setText(self.attribute[index_row]['name'])
