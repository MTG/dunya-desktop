from PyQt5.QtWidgets import (QFrame, QGridLayout, QVBoxLayout, QLabel,
                             QLineEdit, QSizePolicy)
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QFont

from table import TableViewResults
from tabwidget import TabWidget
from audioattframe import AudioAttFrame
from models.recordingmodel import RecordingModel
from models.proxymodel import SortFilterProxyModel

import dunyadesktop_app.ui_files.resources_rc

DUNYA_ICON = ":/compmusic/icons/dunya.svg"
QUERY_ICON = ":/compmusic/icons/magnifying-glass.png"


class QueryFrame(QFrame):
    """Query frame of the main window. Contains the results table, attribute
    frame, line edits for filtering and labels."""
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        # grid layout for main window
        layout_main = QGridLayout(self)
        layout_main.setContentsMargins(5, 19, 5, 3)
        layout_main.setHorizontalSpacing(0)
        layout_main.setVerticalSpacing(8)

        self.tabWidget = TabWidget(self)

        layout_v = QVBoxLayout(self.tabWidget.tab_audio)
        layout_v.setContentsMargins(5, 5, 5, 2)
        layout_v.setSpacing(5)

        self.label_filtering = QLabel(self.tabWidget.tab_audio)
        self._set_label_filtering()
        layout_v.addWidget(self.label_filtering)

        self.frame_attributes = AudioAttFrame()
        layout_v.addWidget(self.frame_attributes)

        self.lineEdit_filter = QLineEdit(self.tabWidget.tab_audio)
        self._set_line_edit_filter()
        layout_v.addWidget(self.lineEdit_filter)
        
        self.tableView_results = TableViewResults(self.tabWidget.tab_audio)
        layout_v.addWidget(self.tableView_results)

        self.recording_model = RecordingModel()

        self.proxy_model = SortFilterProxyModel()
        self.proxy_model.setSourceModel(self.recording_model)
        self.proxy_model.setFilterKeyColumn(-1)

        self.tableView_results.setModel(self.proxy_model)

        layout_main.addWidget(self.tabWidget, 1, 0, 1, 1)

        self._retranslate_ui()
        self.tabWidget.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(self)

        self.lineEdit_filter.setDisabled(True)
        self.tableView_results.setGridStyle(Qt.DotLine)
        self.tableView_results.setDisabled(True)

    def _set_label_filtering(self):
        """Sets the size policies of filtering label"""
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.label_filtering.sizePolicy().hasHeightForWidth())
        self.label_filtering.setSizePolicy(size_policy)

        # font for filtering label
        font = QFont()
        font.setPointSize(11)
        self.label_filtering.setFont(font)

    def _set_line_edit_filter(self):
        """Sets the size policies of line edit filter"""
        font = QFont()
        font.setPointSize(10)
        self.lineEdit_filter.setFont(font)

    def _retranslate_ui(self):
        self.setWindowTitle("Dunya Desktop")

        self.label_filtering.setText("<html><head/><body><p><span style=\" "
                                     "font-size:10pt; "
                                     "color:#878787;\">FILTERING</span></p"
                                     "></body></html>")

        self.lineEdit_filter.setPlaceholderText(
            "Type here to filter the results...")

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabWidget.tab_audio),
            "Audio Collection")
