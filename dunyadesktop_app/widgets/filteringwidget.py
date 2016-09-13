from PyQt4 import QtGui, QtCore
from table import TableView
from dunyadesktop_app.models.filteringmodel import FilteringModel
from dunyadesktop_app.models.proxymodel import SortFilterProxyModel

import dunyadesktop_app.ui_files.resources_rc


class FilteringWidget(QtGui.QWidget):
    def __init__(self, attribute):
        QtGui.QWidget.__init__(self)
        self.attribute = attribute

        self.setWindowTitle('Attribute')
        v_layout = QtGui.QVBoxLayout(self)

        self.filtering_edit = QtGui.QLineEdit()
        self.table_attribute = TableView()
        self.table_attribute.horizontalHeader().hide()

        v_layout.addWidget(self.filtering_edit)
        v_layout.addWidget(self.table_attribute)
        self.setLayout(v_layout)

        self.filtering_model = FilteringModel()
        self.filtering_model.add_items(self.attribute)

        self.proxy_model = SortFilterProxyModel()
        self.proxy_model.setSourceModel(self.filtering_model)

        self.table_attribute.setModel(self.proxy_model)
        self.table_attribute.setColumnWidth(0, 28)

        self.table_attribute.entered.connect(self.item_entered)
        self.table_attribute.item_exited.connect(self.item_exited)

    def item_entered(self, item):
        self.table_attribute.model().sourceModel().item(item.row(),
                        item.column()).setBackground(QtGui.QColor('moccasin'))

    def item_exited(self, item):
        self.table_attribute.model().sourceModel().item(item.row(),
            item.column()).setBackground(QtGui.QTableWidgetItem().background())
