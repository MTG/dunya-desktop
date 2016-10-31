from PyQt4 import QtGui, QtCore

from table import TableView

from models.filteringmodel import FilteringModel
from models.proxymodel import SortFilterProxyModel

import dunyadesktop_app.ui_files.resources_rc


class FilteringDialog(QtGui.QDialog):
    """The dialog which pops up when the user clicks the combobox"""
    ok_button_clicked = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.attribute = None
        self.setFixedSize(200, 300)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)

        v_layout = QtGui.QVBoxLayout(self)
        self.filtering_edit = QtGui.QLineEdit()
        self.table_attribute = TableView()

        self.button_box = QtGui.QDialogButtonBox()
        self.button_box.addButton('OK', QtGui.QDialogButtonBox.AcceptRole)
        self.button_box.addButton('Cancel', QtGui.QDialogButtonBox.RejectRole)

        v_layout.addWidget(self.filtering_edit)
        v_layout.addWidget(self.table_attribute)
        v_layout.addWidget(self.button_box)

        self.setLayout(v_layout)

        self.filtering_model = FilteringModel()

        self.proxy_model = SortFilterProxyModel()
        self.proxy_model.setSourceModel(self.filtering_model)
        self.proxy_model.setFilterKeyColumn(-1)

        self.table_attribute.horizontalHeader().hide()
        self.table_attribute.setModel(self.proxy_model)
        self.table_attribute.setColumnWidth(0, 28)

        self.filtering_edit.setPlaceholderText('Type here to filter...')
        self.selection = -1

        self.filtering_edit.textChanged.connect(
            lambda: self.proxy_model.filter_table(self.filtering_edit.text()))

        self.button_box.rejected.connect(self.clicked_cancel)
        self.table_attribute.doubleClicked.connect(
            self.get_selected_item_index)
        self.button_box.accepted.connect(self.get_selected_item_index)

    def get_selected_item_index(self):
        """Stores the index of the selected item and emits the clicked
        signal."""
        self.filtering_edit.setText('')
        self.selection = self.table_attribute.model().mapToSource(
            self.table_attribute.currentIndex())
        self.close()
        self.ok_button_clicked.emit()

    def clicked_cancel(self):
        """Closes the window"""
        self.close()
