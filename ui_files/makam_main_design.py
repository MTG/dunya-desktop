# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designs/makam_main.ui'
#
# Created: Thu Jul 21 23:01:08 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(629, 622)
        MainWindow.setBaseSize(QtCore.QSize(4, 4))
        MainWindow.setMouseTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/compmusic/icons/compmusic-logo-black.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget_makam = QtGui.QWidget(MainWindow)
        self.centralwidget_makam.setObjectName("centralwidget_makam")
        self.gridLayout_4 = QtGui.QGridLayout(self.centralwidget_makam)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_makam = QtGui.QLabel(self.centralwidget_makam)
        self.label_makam.setAlignment(QtCore.Qt.AlignCenter)
        self.label_makam.setWordWrap(False)
        self.label_makam.setObjectName("label_makam")
        self.gridLayout_4.addWidget(self.label_makam, 0, 0, 1, 1)
        self.tabWidget_makam_corpus = QtGui.QTabWidget(self.centralwidget_makam)
        self.tabWidget_makam_corpus.setStyleSheet("QTabWidget::pane { /* The tab widget frame */\n"
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
"}")
        self.tabWidget_makam_corpus.setObjectName("tabWidget_makam_corpus")
        self.tab_score = QtGui.QWidget()
        self.tab_score.setObjectName("tab_score")
        self.tabWidget_makam_corpus.addTab(self.tab_score, "")
        self.tab_audio = QtGui.QWidget()
        self.tab_audio.setObjectName("tab_audio")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_audio)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_filtering = QtGui.QLabel(self.tab_audio)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_filtering.sizePolicy().hasHeightForWidth())
        self.label_filtering.setSizePolicy(sizePolicy)
        self.label_filtering.setObjectName("label_filtering")
        self.verticalLayout_2.addWidget(self.label_filtering)
        self.frame_attiributes = QtGui.QFrame(self.tab_audio)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_attiributes.sizePolicy().hasHeightForWidth())
        self.frame_attiributes.setSizePolicy(sizePolicy)
        self.frame_attiributes.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_attiributes.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_attiributes.setObjectName("frame_attiributes")
        self.gridLayout = QtGui.QGridLayout(self.frame_attiributes)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_filtering = QtGui.QHBoxLayout()
        self.horizontalLayout_filtering.setSpacing(2)
        self.horizontalLayout_filtering.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_filtering.setObjectName("horizontalLayout_filtering")
        self.label_filter_makam = QtGui.QLabel(self.frame_attiributes)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_filter_makam.sizePolicy().hasHeightForWidth())
        self.label_filter_makam.setSizePolicy(sizePolicy)
        self.label_filter_makam.setMaximumSize(QtCore.QSize(55, 16777215))
        self.label_filter_makam.setObjectName("label_filter_makam")
        self.horizontalLayout_filtering.addWidget(self.label_filter_makam)
        self.comboBox_makam = QtGui.QComboBox(self.frame_attiributes)
        self.comboBox_makam.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_makam.setObjectName("comboBox_makam")
        self.horizontalLayout_filtering.addWidget(self.comboBox_makam)
        spacerItem = QtGui.QSpacerItem(7, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_filtering.addItem(spacerItem)
        self.label_filter_form = QtGui.QLabel(self.frame_attiributes)
        self.label_filter_form.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label_filter_form.setObjectName("label_filter_form")
        self.horizontalLayout_filtering.addWidget(self.label_filter_form)
        self.comboBox_form = QtGui.QComboBox(self.frame_attiributes)
        self.comboBox_form.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_form.setObjectName("comboBox_form")
        self.horizontalLayout_filtering.addWidget(self.comboBox_form)
        spacerItem1 = QtGui.QSpacerItem(7, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_filtering.addItem(spacerItem1)
        self.label_filter_usul = QtGui.QLabel(self.frame_attiributes)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_filter_usul.sizePolicy().hasHeightForWidth())
        self.label_filter_usul.setSizePolicy(sizePolicy)
        self.label_filter_usul.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label_filter_usul.setObjectName("label_filter_usul")
        self.horizontalLayout_filtering.addWidget(self.label_filter_usul)
        self.comboBox_usul = QtGui.QComboBox(self.frame_attiributes)
        self.comboBox_usul.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_usul.setObjectName("comboBox_usul")
        self.horizontalLayout_filtering.addWidget(self.comboBox_usul)
        spacerItem2 = QtGui.QSpacerItem(7, 5, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_filtering.addItem(spacerItem2)
        self.toolButton_query = QtGui.QToolButton(self.frame_attiributes)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_query.sizePolicy().hasHeightForWidth())
        self.toolButton_query.setSizePolicy(sizePolicy)
        self.toolButton_query.setMinimumSize(QtCore.QSize(50, 25))
        self.toolButton_query.setMaximumSize(QtCore.QSize(30, 25))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/compmusic/icons/magnifying-glass.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_query.setIcon(icon1)
        self.toolButton_query.setCheckable(False)
        self.toolButton_query.setObjectName("toolButton_query")
        self.horizontalLayout_filtering.addWidget(self.toolButton_query)
        self.gridLayout.addLayout(self.horizontalLayout_filtering, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_attiributes)
        self.frame_results = QtGui.QFrame(self.tab_audio)
        self.frame_results.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_results.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_results.setObjectName("frame_results")
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_results)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_results = QtGui.QVBoxLayout()
        self.verticalLayout_results.setObjectName("verticalLayout_results")
        self.lineEdit_filter = QtGui.QLineEdit(self.frame_results)
        self.lineEdit_filter.setText("")
        self.lineEdit_filter.setObjectName("lineEdit_filter")
        self.verticalLayout_results.addWidget(self.lineEdit_filter)
        self.tableView_results = QtGui.QTableView(self.frame_results)
        self.tableView_results.setObjectName("tableView_results")
        self.verticalLayout_results.addWidget(self.tableView_results)
        self.gridLayout_2.addLayout(self.verticalLayout_results, 0, 0, 1, 1)
        self.frame = QtGui.QFrame(self.frame_results)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 45))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.toolButton_download_audio = QtGui.QToolButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_download_audio.sizePolicy().hasHeightForWidth())
        self.toolButton_download_audio.setSizePolicy(sizePolicy)
        self.toolButton_download_audio.setMinimumSize(QtCore.QSize(0, 30))
        self.toolButton_download_audio.setMaximumSize(QtCore.QSize(75, 35))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/compmusic/icons/sound-waves.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_download_audio.setIcon(icon2)
        self.toolButton_download_audio.setIconSize(QtCore.QSize(18, 18))
        self.toolButton_download_audio.setCheckable(False)
        self.toolButton_download_audio.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_download_audio.setObjectName("toolButton_download_audio")
        self.horizontalLayout.addWidget(self.toolButton_download_audio)
        self.toolButton_download_pdm = QtGui.QToolButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_download_pdm.sizePolicy().hasHeightForWidth())
        self.toolButton_download_pdm.setSizePolicy(sizePolicy)
        self.toolButton_download_pdm.setMinimumSize(QtCore.QSize(0, 30))
        self.toolButton_download_pdm.setMaximumSize(QtCore.QSize(180, 35))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/compmusic/icons/pdm_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_download_pdm.setIcon(icon3)
        self.toolButton_download_pdm.setIconSize(QtCore.QSize(23, 23))
        self.toolButton_download_pdm.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_download_pdm.setObjectName("toolButton_download_pdm")
        self.horizontalLayout.addWidget(self.toolButton_download_pdm)
        self.toolButton_histogram = QtGui.QToolButton(self.frame)
        self.toolButton_histogram.setMinimumSize(QtCore.QSize(0, 30))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/compmusic/icons/bozkurt_pcd.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_histogram.setIcon(icon4)
        self.toolButton_histogram.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_histogram.setObjectName("toolButton_histogram")
        self.horizontalLayout.addWidget(self.toolButton_histogram)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_results)
        self.tabWidget_makam_corpus.addTab(self.tab_audio, "")
        self.tab_metadata = QtGui.QWidget()
        self.tab_metadata.setObjectName("tab_metadata")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_metadata)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget_makam_corpus.addTab(self.tab_metadata, "")
        self.gridLayout_4.addWidget(self.tabWidget_makam_corpus, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget_makam)
        self.menubar_makam = QtGui.QMenuBar(MainWindow)
        self.menubar_makam.setGeometry(QtCore.QRect(0, 0, 629, 25))
        self.menubar_makam.setObjectName("menubar_makam")
        MainWindow.setMenuBar(self.menubar_makam)
        self.statusbar_makam = QtGui.QStatusBar(MainWindow)
        self.statusbar_makam.setObjectName("statusbar_makam")
        MainWindow.setStatusBar(self.statusbar_makam)
        self.label_filter_makam.setBuddy(self.comboBox_makam)
        self.label_filter_form.setBuddy(self.comboBox_form)
        self.label_filter_usul.setBuddy(self.comboBox_usul)

        self.retranslateUi(MainWindow)
        self.tabWidget_makam_corpus.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "CompMusic", None, QtGui.QApplication.UnicodeUTF8))
        self.label_makam.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Turkish Makam Corpus</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_makam_corpus.setStatusTip(QtGui.QApplication.translate("MainWindow", "Audio corpus and audio related features", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_makam_corpus.setTabText(self.tabWidget_makam_corpus.indexOf(self.tab_score), QtGui.QApplication.translate("MainWindow", "Score", None, QtGui.QApplication.UnicodeUTF8))
        self.label_filtering.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Filtering</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_filter_makam.setText(QtGui.QApplication.translate("MainWindow", "Makam:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_makam.setStatusTip(QtGui.QApplication.translate("MainWindow", "Select makam", None, QtGui.QApplication.UnicodeUTF8))
        self.label_filter_form.setText(QtGui.QApplication.translate("MainWindow", "Form:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_form.setStatusTip(QtGui.QApplication.translate("MainWindow", "Select form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_filter_usul.setText(QtGui.QApplication.translate("MainWindow", "Usul:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_usul.setStatusTip(QtGui.QApplication.translate("MainWindow", "Select usul", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_query.setText(QtGui.QApplication.translate("MainWindow", "Query", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_filter.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Type here to filter the results...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_download_audio.setStatusTip(QtGui.QApplication.translate("MainWindow", "Download the selected audio recordings", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_download_audio.setText(QtGui.QApplication.translate("MainWindow", "Audio", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_download_pdm.setText(QtGui.QApplication.translate("MainWindow", "Predominant Melody", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_histogram.setText(QtGui.QApplication.translate("MainWindow", "Histogram", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_makam_corpus.setTabText(self.tabWidget_makam_corpus.indexOf(self.tab_audio), QtGui.QApplication.translate("MainWindow", "Audio", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_makam_corpus.setTabText(self.tabWidget_makam_corpus.indexOf(self.tab_metadata), QtGui.QApplication.translate("MainWindow", "Metadata", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
