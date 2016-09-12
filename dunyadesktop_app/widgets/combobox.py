import os
from PyQt4 import QtGui
from filteringwidget import FilteringWidget

CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'combobox.css')


class ComboBox(QtGui.QComboBox):
    def __init__(self, parent):
        QtGui.QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.setInsertPolicy(QtGui.QComboBox.NoInsert)

        self._set_css()
        self.filtering_widget = FilteringWidget()

        self.highlighted.connect(self.show_search_box)

    def _set_css(self):
        with open(CSS_PATH) as f:
            css = f.read()
        self.setStyleSheet(css)

    def set_placeholder_text(self, text):
        font = QtGui.QFont()
        font.setPointSize(10)

        self.lineEdit().setPlaceholderText(text)
        self.lineEdit().setFont(font)

    def add_items(self, attribute):
        for att in attribute:
            self.addItem(att['name'])
        self.setCurrentIndex(-1)

    def show_search_box(self):
        self.hidePopup()
        self.filtering_widget.show()
