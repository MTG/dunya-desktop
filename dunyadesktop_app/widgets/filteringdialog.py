from PyQt4 import QtGui, QtCore
from table import TableView
from dunyadesktop_app.models.filteringmodel import FilteringModel
from dunyadesktop_app.models.proxymodel import SortFilterProxyModel

import dunyadesktop_app.ui_files.resources_rc


class FilteringDialog(QtGui.QDialog):
    def __init__(self, attribute):
        QtGui.QDialog.__init__(self)
        self.attribute = attribute

        self.setWindowTitle('Attribute')
        v_layout = QtGui.QVBoxLayout(self)

        self.filtering_edit = QtGui.QLineEdit()
        self.table_attribute = TableView()

        self.button_box = QtGui.QDialogButtonBox()
        self.button_box.addButton('OK',
                                  QtGui.QDialogButtonBox.AcceptRole)
        self.button_box.addButton('Cancel',
                                  QtGui.QDialogButtonBox.RejectRole)

        v_layout.addWidget(self.filtering_edit)
        v_layout.addWidget(self.table_attribute)
        v_layout.addWidget(self.button_box)

        self.setLayout(v_layout)

        self.filtering_model = FilteringModel()
        self.filtering_model.add_items(self.attribute)

        self.proxy_model = SortFilterProxyModel()
        self.proxy_model.setSourceModel(self.filtering_model)
        self.proxy_model.setFilterKeyColumn(-1)

        self.table_attribute.horizontalHeader().hide()
        self.table_attribute.setModel(self.proxy_model)
        self.table_attribute.setColumnWidth(0, 28)

        self.filtering_edit.setPlaceholderText('Type here to filter...')

        self.table_attribute.entered.connect(self.item_entered)
        self.table_attribute.item_exited.connect(self.item_exited)

        self.filtering_edit.textChanged.connect(lambda: self.proxy_model.filtering_the_table(self.filtering_edit.text()))
        #self.table_attribute.table_scrolled.connect(self.item_exited)

    def item_entered(self, item):
        self.table_attribute.model().sourceModel().item(item.row(),
                        item.column()).setBackground(QtGui.QColor('moccasin'))

    def item_exited(self, item):
        self.table_attribute.model().sourceModel().item(item.row(),
            item.column()).setBackground(QtGui.QTableWidgetItem().background())
