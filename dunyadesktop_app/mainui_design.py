import sys
from PyQt4 import QtCore, QtGui

from utilities import utilities
from widgets.combobox import ComboBox
from widgets.table import TableWidget
from widgets.tabwidget import TabWidgetMakam

import ui_files.resources_rc

DUNYA_ICON = ":/compmusic/icons/dunya.svg"
QUERY_ICON = ":/compmusic/icons/magnifying-glass.png"


class MainWindow(QtGui.QMainWindow):
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

        self.tabWidget = TabWidgetMakam(self.central_widget)

        self.verticalLayout = QtGui.QVBoxLayout(self.tabWidget.tab_audio)
        self.verticalLayout.setContentsMargins(5, 5, 5, 2)
        self.verticalLayout.setSpacing(5)

        self.label_filtering = QtGui.QLabel(self.tabWidget.tab_audio)
        self._set_label_filtering()

        self.frame_attributes = QtGui.QFrame(self.tabWidget.tab_audio)
        self._set_frame_attributes()

        self.gridLayout_filtering = QtGui.QGridLayout(self.frame_attributes)
        self._set_gridlayout_filtering()

        self.lineEdit_filter = QtGui.QLineEdit(self.tabWidget.tab_audio)
        self._set_line_edit_filter()

        self.tableView_results = TableWidget(self.tabWidget.tab_audio)
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

    def _set_frame_attributes(self):
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                        QtGui.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.frame_attributes.sizePolicy().hasHeightForWidth())
        self.frame_attributes.setSizePolicy(size_policy)
        self.frame_attributes.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.frame_attributes.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_attributes.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_attributes.setLineWidth(1)

    def _set_gridlayout_filtering(self):
        self.gridLayout_filtering.setSizeConstraint(
            QtGui.QLayout.SetNoConstraint)
        self.gridLayout_filtering.setMargin(2)
        self.gridLayout_filtering.setSpacing(3)

        # spacer in grid layout of filtering section
        spacer_item = QtGui.QSpacerItem(3, 20, QtGui.QSizePolicy.Fixed,
                                        QtGui.QSizePolicy.Minimum)
        self.gridLayout_filtering.addItem(spacer_item, 0, 1, 1, 1)

        # combo boxes
        # melodic structure
        self.comboBox_melodic = ComboBox(self.frame_attributes)
        self.gridLayout_filtering.addWidget(self.comboBox_melodic, 0, 0, 1, 1)

        # form structure
        self.comboBox_form = ComboBox(self.frame_attributes)
        self.gridLayout_filtering.addWidget(self.comboBox_form, 0, 2, 1, 1)

        # rhythmic structure
        self.comboBox_rhythm = ComboBox(self.frame_attributes)
        self.gridLayout_filtering.addWidget(self.comboBox_rhythm, 0, 4, 1, 1)

        # composer
        self.comboBox_composer = ComboBox(self.frame_attributes)
        self.gridLayout_filtering.addWidget(self.comboBox_composer, 1, 0, 1, 1)
        self.comboBox_composer.set_placeholder_text('Composer')

        # performer
        self.comboBox_performer = ComboBox(self.frame_attributes)
        self.gridLayout_filtering.addWidget(self.comboBox_performer,
                                            1, 2, 1, 1)
        self.comboBox_performer.set_placeholder_text('Performer')

        # instrument
        self.comboBox_instrument = ComboBox(self.frame_attributes)
        self.gridLayout_filtering.addWidget(self.comboBox_instrument,
                                            1, 4, 1, 1)
        self.comboBox_instrument.set_placeholder_text('Instrument')

        spacer_item1 = QtGui.QSpacerItem(3, 20, QtGui.QSizePolicy.Minimum,
                                         QtGui.QSizePolicy.Fixed)
        self.gridLayout_filtering.addItem(spacer_item1, 1, 3, 1, 1)

        spacer_item2 = QtGui.QSpacerItem(3, 20, QtGui.QSizePolicy.Minimum,
                                         QtGui.QSizePolicy.Fixed)
        self.gridLayout_filtering.addItem(spacer_item2, 0, 5, 1, 1)
        self.verticalLayout.addWidget(self.frame_attributes)

        # query button and layout
        self.horizontalLayout_query = QtGui.QHBoxLayout()
        self.horizontalLayout_query.setSpacing(0)

        self.toolButton_query = QtGui.QToolButton(self.frame_attributes)
        self.toolButton_query.setMinimumSize(QtCore.QSize(50, 50))
        self.toolButton_query.setMaximumSize(QtCore.QSize(60, 60))
        icon_query = QtGui.QIcon()
        icon_query.addPixmap(QtGui.QPixmap(utilities._fromUtf8(QUERY_ICON)),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_query.setIcon(icon_query)
        self.toolButton_query.setIconSize(QtCore.QSize(25, 25))
        self.horizontalLayout_query.addWidget(self.toolButton_query)
        self.gridLayout_filtering.addLayout(self.horizontalLayout_query, 0, 6,
                                            2, 1)

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
            utilities._translate("MainWindow", "CompMusic", None))

        self.tabWidget.setStatusTip(
            utilities._translate("MainWindow",
                                 "Audio corpus and audio related features",
                                 None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabWidget.tab_score),
            utilities._translate("MainWindow", "Score", None))
        self.label_filtering.setText(utilities._translate("MainWindow",
                                                          "<html><head/><body><p><span style=\" font-weight:600;\">Filtering</span></p></body></html>",
                                                          None))

        self.lineEdit_filter.setPlaceholderText(
            utilities._translate("MainWindow",
                                 "Type here to filter the results...",
                                 None))

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabWidget.tab_audio),
            utilities._translate("MainWindow", "Audio", None))


class MainMakam(MainWindow):
    def __init__(self):
        # setting the interface
        super(MainMakam, self).__init__()



app = QtGui.QApplication(sys.argv)
dialog = MainMakam()
dialog.show()
app.exec_()
