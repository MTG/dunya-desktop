from PyQt5.QtCore import QSortFilterProxyModel, Qt, QRegExp


class SortFilterProxyModel(QSortFilterProxyModel):
    """Sort filter model is for filtering the table of query results."""
    def __init__(self, QObject_parent=None):
        QSortFilterProxyModel.__init__(self, QObject_parent)

    def filter_table(self, text):
        reg_exp = QRegExp(text, Qt.CaseInsensitive)
        self.setFilterRegExp(reg_exp)
