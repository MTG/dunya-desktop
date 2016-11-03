import sys

from PyQt4 import QtGui, QtCore


class NewCollectionDialog(QtGui.QDialog):
    """The dialog which pops up when the user clicks the combobox"""
    ok_button_clicked = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.attribute = None

        layout = QtGui.QGridLayout(self)
        layout.setContentsMargins(0, 2, 0, 1)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(2)

        self.coll_edit = QtGui.QLineEdit(self)
        self.coll_edit.setMaximumSize(QtCore.QSize(16777215, 40))
        layout.addWidget(self.coll_edit, 1, 0, 1, 1)

        self.desc_edit = QtGui.QTextEdit(self)
        self._set_desc_edit()
        layout.addWidget(self.desc_edit, 3, 0, 1, 1)

        self.label_name = QtGui.QLabel(self)
        self.label_name.setText('Name')
        layout.addWidget(self.label_name, 0, 0, 1, 1)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        layout.addWidget(self.buttonBox, 7, 0, 1, 1)

        self.label_description = QtGui.QLabel(self)
        self.label_description.setText('Description')
        layout.addWidget(self.label_description, 2, 0, 1, 1)

    def _set_dialog(self):
        self.setWindowTitle('New Collection')
        self.resize(350, 250)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(350, 250))
        self.setMaximumSize(QtCore.QSize(350, 250))

    def _set_desc_edit(self):
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.desc_edit.sizePolicy().hasHeightForWidth())
        self.desc_edit.setSizePolicy(sizePolicy)
        self.desc_edit.setMinimumSize(QtCore.QSize(0, 150))
        self.desc_edit.setMaximumSize(QtCore.QSize(16777215, 150))

app = QtGui.QApplication(sys.argv)
mainwindow_makam = NewCollectionDialog()
mainwindow_makam.show()
app.exec_()
