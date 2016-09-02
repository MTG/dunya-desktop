# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designs/makam_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(679, 656)
        MainWindow.setBaseSize(QtCore.QSize(4, 4))
        MainWindow.setMouseTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/compmusic/icons/logoDunya.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget_makam = QtGui.QWidget(MainWindow)
        self.centralwidget_makam.setObjectName(_fromUtf8("centralwidget_makam"))
        self.gridLayout_mainwindow = QtGui.QGridLayout(self.centralwidget_makam)
        self.gridLayout_mainwindow.setContentsMargins(5, 9, 5, 3)
        self.gridLayout_mainwindow.setHorizontalSpacing(0)
        self.gridLayout_mainwindow.setVerticalSpacing(8)
        self.gridLayout_mainwindow.setObjectName(_fromUtf8("gridLayout_mainwindow"))
        self.label_makam = QtGui.QLabel(self.centralwidget_makam)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        self.label_makam.setFont(font)
        self.label_makam.setAlignment(QtCore.Qt.AlignCenter)
        self.label_makam.setWordWrap(False)
        self.label_makam.setObjectName(_fromUtf8("label_makam"))
        self.gridLayout_mainwindow.addWidget(self.label_makam, 0, 0, 1, 1)
        self.tabWidget_makam_corpus = QtGui.QTabWidget(self.centralwidget_makam)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget_makam_corpus.setFont(font)
        self.tabWidget_makam_corpus.setStyleSheet(_fromUtf8("QTabWidget::pane { /* The tab widget frame */\n"
"    border-top: 2px solid #C2C7CB;\n"
"    position: absolute;\n"
"    top: -0.5em;\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    alignment: center;\n"
"}\n"
"\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"    border: 2px solid #C4C4C3;\n"
"    border-bottom-color: #C2C7CB;  /*same as the pane color */\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 8ex;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"/*qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"*/\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n"
"                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n"
"    /*border-bottom-color: #85C1E9;*/\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color: #9B9B9B;\n"
"    border-bottom-color: #85C1E9; /* same as pane color */\n"
"}"))
        self.tabWidget_makam_corpus.setObjectName(_fromUtf8("tabWidget_makam_corpus"))
        self.tab_score = QtGui.QWidget()
        self.tab_score.setObjectName(_fromUtf8("tab_score"))
        self.tabWidget_makam_corpus.addTab(self.tab_score, _fromUtf8(""))
        self.tab_audio = QtGui.QWidget()
        self.tab_audio.setObjectName(_fromUtf8("tab_audio"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_audio)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 2)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_filtering = QtGui.QLabel(self.tab_audio)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_filtering.sizePolicy().hasHeightForWidth())
        self.label_filtering.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_filtering.setFont(font)
        self.label_filtering.setObjectName(_fromUtf8("label_filtering"))
        self.verticalLayout_2.addWidget(self.label_filtering)
        self.frame_attiributes = QtGui.QFrame(self.tab_audio)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_attiributes.sizePolicy().hasHeightForWidth())
        self.frame_attiributes.setSizePolicy(sizePolicy)
        self.frame_attiributes.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.frame_attiributes.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_attiributes.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_attiributes.setLineWidth(1)
        self.frame_attiributes.setObjectName(_fromUtf8("frame_attiributes"))
        self.gridLayout_filtering = QtGui.QGridLayout(self.frame_attiributes)
        self.gridLayout_filtering.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout_filtering.setMargin(2)
        self.gridLayout_filtering.setSpacing(3)
        self.gridLayout_filtering.setObjectName(_fromUtf8("gridLayout_filtering"))
        spacerItem = QtGui.QSpacerItem(3, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_filtering.addItem(spacerItem, 0, 1, 1, 1)
        self.horizontalLayout_query = QtGui.QHBoxLayout()
        self.horizontalLayout_query.setSpacing(0)
        self.horizontalLayout_query.setObjectName(_fromUtf8("horizontalLayout_query"))
        self.toolButton_query = QtGui.QToolButton(self.frame_attiributes)
        self.toolButton_query.setMinimumSize(QtCore.QSize(50, 50))
        self.toolButton_query.setMaximumSize(QtCore.QSize(60, 60))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/compmusic/icons/magnifying-glass.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_query.setIcon(icon1)
        self.toolButton_query.setIconSize(QtCore.QSize(25, 25))
        self.toolButton_query.setObjectName(_fromUtf8("toolButton_query"))
        self.horizontalLayout_query.addWidget(self.toolButton_query)
        self.gridLayout_filtering.addLayout(self.horizontalLayout_query, 0, 6, 2, 1)
        self.comboBox_performer = QtGui.QComboBox(self.frame_attiributes)
        self.comboBox_performer.setStyleSheet(_fromUtf8("QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    /*padding: 1px 18px 1px 3px;*/\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"   background: rgb(255, 255, 255);\n"
"    /*background: transparent*/\n"
"}\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"}\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
"                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}"))
        self.comboBox_performer.setEditable(True)
        self.comboBox_performer.setObjectName(_fromUtf8("comboBox_performer"))
        self.gridLayout_filtering.addWidget(self.comboBox_performer, 1, 2, 1, 1)
        self.comboBox_makam = QtGui.QComboBox(self.frame_attiributes)
        self.comboBox_makam.setStyleSheet(_fromUtf8("QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    /*padding: 1px 18px 1px 3px;*/\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"   background: rgb(255, 255, 255);\n"
"    /*background: transparent*/\n"
"}\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"}\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
"                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}"))
        self.comboBox_makam.setEditable(True)
        self.comboBox_makam.setObjectName(_fromUtf8("comboBox_makam"))
        self.gridLayout_filtering.addWidget(self.comboBox_makam, 0, 0, 1, 1)
        self.comboBox_form = QtGui.QComboBox(self.frame_attiributes)
        self.comboBox_form.setStyleSheet(_fromUtf8("QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    /*padding: 1px 18px 1px 3px;*/\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"   background: rgb(255, 255, 255);\n"
"    /*background: transparent*/\n"
"}\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"}\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
"                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}"))
        self.comboBox_form.setEditable(True)
        self.comboBox_form.setObjectName(_fromUtf8("comboBox_form"))
        self.gridLayout_filtering.addWidget(self.comboBox_form, 0, 2, 1, 1)
        self.comboBox_usul = QtGui.QComboBox(self.frame_attiributes)
        self.comboBox_usul.setStyleSheet(_fromUtf8("QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    /*padding: 1px 18px 1px 3px;*/\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"   background: rgb(255, 255, 255);\n"
"    /*background: transparent*/\n"
"}\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"}\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
"                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}"))
        self.comboBox_usul.setEditable(True)
        self.comboBox_usul.setObjectName(_fromUtf8("comboBox_usul"))
        self.gridLayout_filtering.addWidget(self.comboBox_usul, 0, 4, 1, 1)
        self.comboBox_instrument = QtGui.QComboBox(self.frame_attiributes)
        self.comboBox_instrument.setStyleSheet(_fromUtf8("QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    /*padding: 1px 18px 1px 3px;*/\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"   background: rgb(255, 255, 255);\n"
"    /*background: transparent*/\n"
"}\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"}\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
"                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}"))
        self.comboBox_instrument.setEditable(True)
        self.comboBox_instrument.setObjectName(_fromUtf8("comboBox_instrument"))
        self.gridLayout_filtering.addWidget(self.comboBox_instrument, 1, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(3, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_filtering.addItem(spacerItem1, 1, 3, 1, 1)
        self.comboBox_composer = QtGui.QComboBox(self.frame_attiributes)
        self.comboBox_composer.setStyleSheet(_fromUtf8("QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    /*padding: 1px 18px 1px 3px;*/\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"   background: rgb(255, 255, 255);\n"
"    /*background: transparent*/\n"
"}\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"}\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
"                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}"))
        self.comboBox_composer.setEditable(True)
        self.comboBox_composer.setObjectName(_fromUtf8("comboBox_composer"))
        self.gridLayout_filtering.addWidget(self.comboBox_composer, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(3, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_filtering.addItem(spacerItem2, 0, 5, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_attiributes)
        self.lineEdit_filter = QtGui.QLineEdit(self.tab_audio)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_filter.setFont(font)
        self.lineEdit_filter.setText(_fromUtf8(""))
        self.lineEdit_filter.setObjectName(_fromUtf8("lineEdit_filter"))
        self.verticalLayout_2.addWidget(self.lineEdit_filter)
        self.tableView_results = QtGui.QTableView(self.tab_audio)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView_results.setFont(font)
        self.tableView_results.setStyleSheet(_fromUtf8("/*background-image: url(:/compmusic/icons/compmusic-logo-opac.svg); */\n"
"background-image: url(:/compmusic/icons/compmusic-logo-opac.svg);\n"
"background-repeat: no-repeat;\n"
"background-attachment: fixed; \n"
"background-position: center;\n"
"/*background-repeat: no-repeat;*/\n"
"background-color: rgb(228, 228, 228)"))
        self.tableView_results.setObjectName(_fromUtf8("tableView_results"))
        self.verticalLayout_2.addWidget(self.tableView_results)
        self.frame = QtGui.QFrame(self.tab_audio)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 25))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame.setStyleSheet(_fromUtf8(""))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setMargin(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.toolButton_download_audio = QtGui.QToolButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_download_audio.sizePolicy().hasHeightForWidth())
        self.toolButton_download_audio.setSizePolicy(sizePolicy)
        self.toolButton_download_audio.setMinimumSize(QtCore.QSize(0, 25))
        self.toolButton_download_audio.setMaximumSize(QtCore.QSize(75, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.toolButton_download_audio.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/compmusic/icons/sound-waves.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_download_audio.setIcon(icon2)
        self.toolButton_download_audio.setIconSize(QtCore.QSize(18, 18))
        self.toolButton_download_audio.setCheckable(False)
        self.toolButton_download_audio.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_download_audio.setObjectName(_fromUtf8("toolButton_download_audio"))
        self.horizontalLayout.addWidget(self.toolButton_download_audio)
        self.toolButton_download_pdm = QtGui.QToolButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_download_pdm.sizePolicy().hasHeightForWidth())
        self.toolButton_download_pdm.setSizePolicy(sizePolicy)
        self.toolButton_download_pdm.setMinimumSize(QtCore.QSize(0, 25))
        self.toolButton_download_pdm.setMaximumSize(QtCore.QSize(180, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.toolButton_download_pdm.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/compmusic/icons/pdm_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_download_pdm.setIcon(icon3)
        self.toolButton_download_pdm.setIconSize(QtCore.QSize(20, 20))
        self.toolButton_download_pdm.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_download_pdm.setObjectName(_fromUtf8("toolButton_download_pdm"))
        self.horizontalLayout.addWidget(self.toolButton_download_pdm)
        self.toolButton_histogram = QtGui.QToolButton(self.frame)
        self.toolButton_histogram.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.toolButton_histogram.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/compmusic/icons/bozkurt_pcd.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_histogram.setIcon(icon4)
        self.toolButton_histogram.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_histogram.setObjectName(_fromUtf8("toolButton_histogram"))
        self.horizontalLayout.addWidget(self.toolButton_histogram)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout_2.addWidget(self.frame)
        self.tabWidget_makam_corpus.addTab(self.tab_audio, _fromUtf8(""))
        self.tab_metadata = QtGui.QWidget()
        self.tab_metadata.setObjectName(_fromUtf8("tab_metadata"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_metadata)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tabWidget_makam_corpus.addTab(self.tab_metadata, _fromUtf8(""))
        self.gridLayout_mainwindow.addWidget(self.tabWidget_makam_corpus, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget_makam)
        self.menubar_makam = QtGui.QMenuBar(MainWindow)
        self.menubar_makam.setGeometry(QtCore.QRect(0, 0, 679, 25))
        self.menubar_makam.setObjectName(_fromUtf8("menubar_makam"))
        MainWindow.setMenuBar(self.menubar_makam)
        self.statusbar_makam = QtGui.QStatusBar(MainWindow)
        self.statusbar_makam.setMinimumSize(QtCore.QSize(0, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.statusbar_makam.setFont(font)
        self.statusbar_makam.setObjectName(_fromUtf8("statusbar_makam"))
        MainWindow.setStatusBar(self.statusbar_makam)

        self.retranslateUi(MainWindow)
        self.tabWidget_makam_corpus.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "CompMusic", None))
        self.label_makam.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Turkish Makam Corpus</span></p></body></html>", None))
        self.tabWidget_makam_corpus.setStatusTip(_translate("MainWindow", "Audio corpus and audio related features", None))
        self.tabWidget_makam_corpus.setTabText(self.tabWidget_makam_corpus.indexOf(self.tab_score), _translate("MainWindow", "Score", None))
        self.label_filtering.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Filtering</span></p></body></html>", None))
        self.toolButton_query.setText(_translate("MainWindow", "...", None))
        self.lineEdit_filter.setPlaceholderText(_translate("MainWindow", "Type here to filter the results...", None))
        self.toolButton_download_audio.setStatusTip(_translate("MainWindow", "Download the selected audio recordings", None))
        self.toolButton_download_audio.setText(_translate("MainWindow", "Audio", None))
        self.toolButton_download_pdm.setText(_translate("MainWindow", "Predominant Melody", None))
        self.toolButton_histogram.setText(_translate("MainWindow", "Histogram", None))
        self.tabWidget_makam_corpus.setTabText(self.tabWidget_makam_corpus.indexOf(self.tab_audio), _translate("MainWindow", "Audio", None))
        self.tabWidget_makam_corpus.setTabText(self.tabWidget_makam_corpus.indexOf(self.tab_metadata), _translate("MainWindow", "Metadata", None))

import resources_rc
