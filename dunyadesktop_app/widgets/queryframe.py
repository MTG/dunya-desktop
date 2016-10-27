from PyQt4 import QtCore, QtGui

from tableresults import TableViewResults
from tabwidget import TabWidget
from audioattframe import AudioAttFrame
from progressbar import ProgressBar
from models.recordingmodel import RecordingModel
from models.proxymodel import SortFilterProxyModel

import dunyadesktop_app.ui_files.resources_rc

DUNYA_ICON = ":/compmusic/icons/dunya.svg"
QUERY_ICON = ":/compmusic/icons/magnifying-glass.png"


class QueryFrame(QtGui.QFrame):
    def __init__(self):
        QtGui.QFrame.__init__(self)

        #self._set_mainwindow()

        # grid layout for main window
        self.gridLayout_mainwindow = QtGui.QGridLayout(self)
        self.gridLayout_mainwindow.setContentsMargins(5, 19, 5, 3)
        self.gridLayout_mainwindow.setHorizontalSpacing(0)
        self.gridLayout_mainwindow.setVerticalSpacing(8)

        # label for central widget
        #self.label_main = QtGui.QLabel(self)
        #self._set_label_main()

        self.tabWidget = TabWidget(self)

        self.verticalLayout = QtGui.QVBoxLayout(self.tabWidget.tab_audio)
        self.verticalLayout.setContentsMargins(5, 5, 5, 2)
        self.verticalLayout.setSpacing(5)

        self.label_filtering = QtGui.QLabel(self.tabWidget.tab_audio)
        self._set_label_filtering()

        self.frame_attributes = AudioAttFrame()
        self.verticalLayout.addWidget(self.frame_attributes)

        self.lineEdit_filter = QtGui.QLineEdit(self.tabWidget.tab_audio)
        self._set_line_edit_filter()

        self.tableView_results = TableViewResults(self.tabWidget.tab_audio)
        self.verticalLayout.addWidget(self.tableView_results)

        self.recording_model= RecordingModel()

        self.proxy_model = SortFilterProxyModel()
        self.proxy_model.setSourceModel(self.recording_model)
        self.proxy_model.setFilterKeyColumn(-1)

        self.tableView_results.setModel(self.proxy_model)

        self.gridLayout_mainwindow.addWidget(self.tabWidget, 1, 0, 1, 1)

        self._retranslate_ui()
        self.tabWidget.setCurrentIndex(1)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.lineEdit_filter.setDisabled(True)
        self.tableView_results.setGridStyle(QtCore.Qt.DotLine)
        self.tableView_results.setDisabled(True)

    def _set_label_main(self):
        # 11 point font
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(11)
        self.label_main.setFont(font)
        self.label_main.setAlignment(QtCore.Qt.AlignCenter)
        self.label_main.setWordWrap(False)
        self.gridLayout_mainwindow.addWidget(self.label_main, 0, 0, 1, 1)

    def _set_label_filtering(self):
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                        QtGui.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.label_filtering.sizePolicy().hasHeightForWidth())
        self.label_filtering.setSizePolicy(size_policy)

        # font for filtering label
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_filtering.setFont(font)
        self.verticalLayout.addWidget(self.label_filtering)

    def _set_line_edit_filter(self):
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_filter.setFont(font)
        self.verticalLayout.addWidget(self.lineEdit_filter)

    def _retranslate_ui(self):
        self.setWindowTitle("Dunya Desktop")

        self.label_filtering.setText("<html><head/><body><p><span style=\" font-size:10pt; color:#878787;\">FILTERING</span></p></body></html>")

        self.lineEdit_filter.setPlaceholderText("Type here to filter the results...")

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabWidget.tab_audio),
            "Audio Collection")
