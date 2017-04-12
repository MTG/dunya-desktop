from PyQt5.QtWidgets import (QDialog, QGridLayout, QLineEdit, QMessageBox,
                             QLabel, QDialogButtonBox, QSizePolicy, QTextEdit)
from PyQt5.QtCore import pyqtSignal, QSize

import utilities.database as database


class NewCollectionDialog(QDialog):
    """The dialog which pops up when the user clicks the combobox"""
    new_collection_added = pyqtSignal()

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self._set_dialog()

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 2, 0, 1)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(2)

        self.coll_edit = QLineEdit(self)
        self.coll_edit.setMaximumSize(QSize(16777215, 40))
        layout.addWidget(self.coll_edit, 1, 0, 1, 1)

        self.desc_edit = QTextEdit(self)
        self._set_desc_edit()
        layout.addWidget(self.desc_edit, 3, 0, 1, 1)

        self.label_name = QLabel(self)
        self.label_name.setText('Name')
        layout.addWidget(self.label_name, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel |
                                          QDialogButtonBox.Ok)
        layout.addWidget(self.buttonBox, 7, 0, 1, 1)

        self.label_description = QLabel(self)
        self.label_description.setText('Description')
        layout.addWidget(self.label_description, 2, 0, 1, 1)

        self.buttonBox.rejected.connect(self.clicked_cancel)
        self.buttonBox.accepted.connect(self.clicked_ok)

    def _set_dialog(self):
        self.setWindowTitle('New Collection')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(350, 250))
        self.setMaximumSize(QSize(350, 250))

    def _set_desc_edit(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.desc_edit.sizePolicy().hasHeightForWidth())
        self.desc_edit.setSizePolicy(size_policy)
        self.desc_edit.setMinimumSize(QSize(0, 140))
        self.desc_edit.setMaximumSize(QSize(16777215, 150))

    def clicked_cancel(self):
        """Closes the window"""
        self.close()

    def clicked_ok(self):
        conn, c = database.connect()
        user_input = str(self.coll_edit.text())

        status = False
        if user_input:
            status = database.add_collection(conn, c, user_input)

        if status:
            self.close()
            self.new_collection_added.emit()
            self.parent().update_collection_widget()
        else:
            msg_box = QMessageBox()
            msg_box.setText('Given collection name is not valid!')
            msg_box.setWindowTitle('')
            msg_box.exec_()
