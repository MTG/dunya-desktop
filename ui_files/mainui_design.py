import sys

from PyQt4 import QtCore, QtGui
from widgets.tab_widget import TabWidgetMakam
from widgets.combobox import ComboBox
from widgets.table import TableWidget
import resources_rc

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class UiMainWindow(object):
    def setup_ui(self, MainWindow):
        # window sizes
        MainWindow.resize(680, 655)
        MainWindow.setMinimumSize(QtCore.QSize(680, 655))
        MainWindow.setBaseSize(QtCore.QSize(4, 4))
        MainWindow.setMouseTracking(False)

        # main window icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/compmusic/icons/dunya.svg")),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        # central widget
        self.central_widget = QtGui.QWidget(MainWindow)

        # grid layout for main window
        self.gridLayout_mainwindow = QtGui.QGridLayout(self.central_widget)
        self.gridLayout_mainwindow.setContentsMargins(5, 19, 5, 3)
        self.gridLayout_mainwindow.setHorizontalSpacing(0)
        self.gridLayout_mainwindow.setVerticalSpacing(8)

        # label for central widget
        self.label_main = QtGui.QLabel(self.central_widget)

        # 11 point font
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)

        self.label_main.setFont(font)
        self.label_main.setAlignment(QtCore.Qt.AlignCenter)
        self.label_main.setWordWrap(False)

        self.gridLayout_mainwindow.addWidget(self.label_main, 0, 0, 1, 1)
        self.tabWidget = TabWidgetMakam(parent=self.central_widget)

        self.verticalLayout = QtGui.QVBoxLayout(self.tabWidget.tab_audio)
        self.verticalLayout.setContentsMargins(5, 5, 5, 2)
        self.verticalLayout.setSpacing(5)

        # setting the label for filtering section
        self.label_filtering = QtGui.QLabel(self.tabWidget.tab_audio)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_filtering.sizePolicy().hasHeightForWidth())
        self.label_filtering.setSizePolicy(sizePolicy)

        # font for filtering label
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_filtering.setFont(font)
        self.verticalLayout.addWidget(self.label_filtering)

        # frame for attributes
        self.frame_attiributes = QtGui.QFrame(self.tabWidget.tab_audio)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_attiributes.sizePolicy().hasHeightForWidth())
        self.frame_attiributes.setSizePolicy(sizePolicy)
        self.frame_attiributes.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.frame_attiributes.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_attiributes.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_attiributes.setLineWidth(1)

        # grid layout for filtering section
        self.gridLayout_filtering = QtGui.QGridLayout(self.frame_attiributes)
        self.gridLayout_filtering.setSizeConstraint(
            QtGui.QLayout.SetNoConstraint)
        self.gridLayout_filtering.setMargin(2)
        self.gridLayout_filtering.setSpacing(3)

        # spacer in grid layout of filtering section
        spacerItem = QtGui.QSpacerItem(3, 20, QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Minimum)
        self.gridLayout_filtering.addItem(spacerItem, 0, 1, 1, 1)

        # query button and layout
        self.horizontalLayout_query = QtGui.QHBoxLayout()
        self.horizontalLayout_query.setSpacing(0)
        self.horizontalLayout_query.setObjectName(
            _fromUtf8("horizontalLayout_query"))

        self.toolButton_query = QtGui.QToolButton(self.frame_attiributes)
        self.toolButton_query.setMinimumSize(QtCore.QSize(50, 50))
        self.toolButton_query.setMaximumSize(QtCore.QSize(60, 60))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(_fromUtf8(":/compmusic/icons/magnifying-glass.png")),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_query.setIcon(icon1)
        self.toolButton_query.setIconSize(QtCore.QSize(25, 25))
        self.horizontalLayout_query.addWidget(self.toolButton_query)
        self.gridLayout_filtering.addLayout(self.horizontalLayout_query, 0, 6,
                                            2, 1)
        # combo boxes
        # performer
        self.comboBox_performer = ComboBox(self.frame_attiributes)
        self.gridLayout_filtering.addWidget(self.comboBox_performer,
                                            1, 2, 1, 1)
        # melodic structure
        self.comboBox_melodic = ComboBox(self.frame_attiributes)
        self.gridLayout_filtering.addWidget(self.comboBox_melodic, 0, 0, 1, 1)

        # form structure
        self.comboBox_form = ComboBox(self.frame_attiributes)
        self.gridLayout_filtering.addWidget(self.comboBox_form, 0, 2, 1, 1)

        # rhythmic structure
        self.comboBox_rhythm = ComboBox(self.frame_attiributes)
        self.gridLayout_filtering.addWidget(self.comboBox_rhythm, 0, 4, 1, 1)

        # instrument
        self.comboBox_instrument = ComboBox(self.frame_attiributes)
        self.gridLayout_filtering.addWidget(self.comboBox_instrument,
                                            1, 4, 1, 1)

        spacerItem1 = QtGui.QSpacerItem(3, 20, QtGui.QSizePolicy.Minimum,
                                        QtGui.QSizePolicy.Fixed)
        self.gridLayout_filtering.addItem(spacerItem1, 1, 3, 1, 1)

        # composer
        self.comboBox_composer = ComboBox(self.frame_attiributes)
        self.gridLayout_filtering.addWidget(self.comboBox_composer, 1, 0, 1, 1)

        spacerItem2 = QtGui.QSpacerItem(3, 20, QtGui.QSizePolicy.Minimum,
                                        QtGui.QSizePolicy.Fixed)
        self.gridLayout_filtering.addItem(spacerItem2, 0, 5, 1, 1)
        self.verticalLayout.addWidget(self.frame_attiributes)

        # line edit for filtering the results
        self.lineEdit_filter = QtGui.QLineEdit(self.tabWidget.tab_audio)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_filter.setFont(font)
        self.lineEdit_filter.setText(_fromUtf8(""))
        self.verticalLayout.addWidget(self.lineEdit_filter)

        # table for results
        self.tableView_results = TableWidget(self.tabWidget.tab_audio)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView_results.setFont(font)
        self.verticalLayout.addWidget(self.tableView_results)

        self.gridLayout_mainwindow.addWidget(self.tabWidget, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.central_widget)

        # menu bar
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 25))
        MainWindow.setMenuBar(self.menubar)

        # status bar
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setMinimumSize(QtCore.QSize(0, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.statusbar.setFont(font)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "CompMusic", None))
        self.label_main.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Turkish Makam Corpus</span></p></body></html>",
                                           None))
        self.tabWidget.setStatusTip(
            _translate("MainWindow", "Audio corpus and audio related features",
                       None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabWidget.tab_score),
            _translate("MainWindow", "Score", None))
        self.label_filtering.setText(_translate("MainWindow",
                                                "<html><head/><body><p><span style=\" font-weight:600;\">Filtering</span></p></body></html>",
                                                None))
        self.toolButton_query.setText(_translate("MainWindow", "...", None))
        self.lineEdit_filter.setPlaceholderText(
            _translate("MainWindow", "Type here to filter the results...",
                       None))

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabWidget.tab_audio),
            _translate("MainWindow", "Audio", None))


class MainMakam(QtGui.QMainWindow, UiMainWindow):

    def __init__(self, parent=None):
        # setting the interface
        super(MainMakam, self).__init__(parent)
        # setting the qt-designer design
        self.setup_ui(self)


app = QtGui.QApplication(sys.argv)
dialog = MainMakam()
dialog.show()
app.exec_()
