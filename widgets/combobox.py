from PyQt4 import QtGui


class ComboBox(QtGui.QComboBox):
    def __init__(self, parent):

        QtGui.QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.setInsertPolicy(QtGui.QComboBox.NoInsert)

        self._set_css()

    def _set_css(self):
        with open("../ui_files/css/combobox.css") as f:
            css = f.read()
        self.setStyleSheet(css)

    def set_placeholder_text(self, text):
        font = QtGui.QFont()
        font.setPointSize(10)

        self.lineEdit().setPlaceholderText(text)
        self.lineEdit().setFont(font)
