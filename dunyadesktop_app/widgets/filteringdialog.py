import os

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox
from PyQt5.QtCore import pyqtSignal, Qt

from table import TableView
from models.filteringmodel import FilteringModel
from models.proxymodel import SortFilterProxyModel

from .widgetutilities import set_css
import ui_files.resources_rc

CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'filteringdialog.css')


class FilteringDialog(QDialog):
    """The dialog which pops up when the user clicks the combobox"""
    ok_button_clicked = pyqtSignal()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.attribute = None
        self.setFixedSize(200, 300)
        set_css(self, CSS_PATH)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)

        v_layout = QVBoxLayout(self)
        self.filtering_edit = QLineEdit()
        self.table_attribute = TableView()

        self.button_box = QDialogButtonBox(self)
        self.button_box.addButton('OK', QDialogButtonBox.AcceptRole)
        self.button_box.addButton('Cancel', QDialogButtonBox.RejectRole)

        v_layout.addWidget(self.filtering_edit)
        v_layout.addWidget(self.table_attribute)
        v_layout.addWidget(self.button_box)

        self.setLayout(v_layout)

        self.filtering_model = FilteringModel(self)

        self.proxy_model = SortFilterProxyModel(self)
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
