from __future__ import absolute_import
import os

from PyQt4 import QtGui, QtCore

from .filteringdialog import FilteringDialog

CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'combobox.css')


class ComboBox(QtGui.QComboBox):
    combobox_clicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtGui.QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.setInsertPolicy(QtGui.QComboBox.NoInsert)

        self._set_css()

    def _set_css(self):
        with open(CSS_PATH) as f:
            css = f.read()
        self.setStyleSheet(css)

    def wheelEvent(self, QWheelEvent):
        pass

    def mousePressEvent(self, QMouseEvent):
        self.filtering_widget = FilteringDialog(self.attribute)
        self.filtering_widget.exec_()

    def set_placeholder_text(self, text):
        font = QtGui.QFont()
        font.setPointSize(10)

        self.lineEdit().setPlaceholderText(text)
        self.lineEdit().setFont(font)

    def add_items(self, attribute):
        self.attribute = attribute
        for att in attribute:
            self.addItem(att['name'])
        self.setCurrentIndex(-1)

    def get_attribute_id(self):
        index = self.currentIndex()
        if index is not -1:
            return self.attribute[index]['uuid']
        else:
            return ''
