from PyQt4 import QtGui
from table import TableWidget

import dunyadesktop_app.ui_files.resources_rc


class FilteringWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.setWindowTitle('Attribute')
        v_layout = QtGui.QVBoxLayout(self)

        self.search_edit = QtGui.QLineEdit()
        self.table_attribute = TableWidget()

        v_layout.addWidget(self.search_edit)
        v_layout.addWidget(self.table_attribute)
        self.setLayout(v_layout)

    def add_items(self, attirubute):
        pass
