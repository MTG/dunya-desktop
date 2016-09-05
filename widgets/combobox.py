from PyQt4 import QtGui


class ComboBox(QtGui.QComboBox):
    def __init__(self, parent):

        QtGui.QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.setInsertPolicy(QtGui.QComboBox.NoInsert)

        self.set_css()

    def set_css(self):
        with open("../ui_files/css/combobox.css") as f:
            css = f.read()
        self.setStyleSheet(css)
