from __future__ import absolute_import

from PyQt4 import QtCore, QtGui

from utilities import utilities
from widgets.table import TableView
from widgets.tabwidget import TabWidget
from widgets.audioattframe import AudioAttFrame
from widgets.progressbar import ProgressBar

import dunyadesktop_app.ui_files.resources_rc

DUNYA_ICON = ":/compmusic/icons/dunya.svg"
QUERY_ICON = ":/compmusic/icons/magnifying-glass.png"


class MainWindowDesign(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self._set_mainwindow()

        # central widget
        self.central_widget = QtGui.QWidget(self)

        # grid layout for main window
        self.gridLayout_mainwindow = QtGui.QGridLayout(self.central_widget)
        self.gridLayout_mainwindow.setContentsMargins(5, 19, 5, 3)
        self.gridLayout_mainwindow.setHorizontalSpacing(0)
        self.gridLayout_mainwindow.setVerticalSpacing(8)

        # label for central widget
        self.label_main = QtGui.QLabel(self.central_widget)
        self._set_label_main()

        self.tabWidget = TabWidget(self.central_widget)

        self.verticalLayout = QtGui.QVBoxLayout(self.tabWidget.tab_audio)
        self.verticalLayout.setContentsMargins(5, 5, 5, 2)
        self.verticalLayout.setSpacing(5)

        self.label_filtering = QtGui.QLabel(self.tabWidget.tab_audio)
        self._set_label_filtering()

        self.frame_attributes = AudioAttFrame()
        self.verticalLayout.addWidget(self.frame_attributes)

        self.lineEdit_filter = QtGui.QLineEdit(self.tabWidget.tab_audio)
        self._set_line_edit_filter()

        self.tableView_results = TableView(self.tabWidget.tab_audio)
        self.verticalLayout.addWidget(self.tableView_results)

        self.gridLayout_mainwindow.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.setCentralWidget(self.central_widget)

        # menu bar
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 25))
        self.setMenuBar(self.menubar)

        # status bar
        self.statusbar = QtGui.QStatusBar(self)
        self._set_status_bar()
        self.progress_bar = ProgressBar(self)
        self.statusbar.addPermanentWidget(self.progress_bar)
        self.progress_bar.setVisible(False)

        self._retranslate_ui()
        self.tabWidget.setCurrentIndex(1)

        QtCore.QMetaObject.connectSlotsByName(self)

    def _set_mainwindow(self):
        # window sizes
        self.resize(680, 655)
        self.setMinimumSize(QtCore.QSize(680, 655))
        self.setBaseSize(QtCore.QSize(4, 4))
        self.setMouseTracking(False)

        # main window icon
        icon_dunya = QtGui.QIcon()
        icon_dunya.addPixmap(QtGui.QPixmap(utilities._fromUtf8(DUNYA_ICON)),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon_dunya)

    def _set_label_main(self):
        # 11 point font
        font = QtGui.QFont()
        font.setFamily(utilities._fromUtf8("Ubuntu"))
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

    def _set_status_bar(self):
        self.statusbar.setMinimumSize(QtCore.QSize(0, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.statusbar.setFont(font)
        self.setStatusBar(self.statusbar)

    def _retranslate_ui(self):
        self.setWindowTitle(
            utilities._translate("MainWindow", "Dunya Desktop", None))

        self.label_filtering.setText(utilities._translate("MainWindow",
                                                          "<html><head/><body><p><span style=\" font-weight:600;\">Filtering</span></p></body></html>",
                                                          None))

        self.lineEdit_filter.setPlaceholderText(
            utilities._translate("MainWindow",
                                 "Type here to filter the results...",
                                 None))

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabWidget.tab_audio),
            utilities._translate("MainWindow", "Audio Collection", None))
