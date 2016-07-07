# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo_design.ui'
#
# Created: Thu Jul  7 19:20:09 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 511)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView_score = QtGui.QTableWidget(Dialog)
        self.tableView_score.setObjectName("tableView_score")
        self.gridLayout.addWidget(self.tableView_score, 4, 1, 2, 2)
        self.comboBox_form = QtGui.QComboBox(Dialog)
        self.comboBox_form.setObjectName("comboBox_form")
        self.gridLayout.addWidget(self.comboBox_form, 1, 2, 1, 1)
        self.pushButton_query = QtGui.QPushButton(Dialog)
        self.pushButton_query.setObjectName("pushButton_query")
        self.gridLayout.addWidget(self.pushButton_query, 3, 1, 1, 2)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.comboBox_usul = QtGui.QComboBox(Dialog)
        self.comboBox_usul.setObjectName("comboBox_usul")
        self.gridLayout.addWidget(self.comboBox_usul, 2, 2, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.comboBox_makam = QtGui.QComboBox(Dialog)
        self.comboBox_makam.setObjectName("comboBox_makam")
        self.gridLayout.addWidget(self.comboBox_makam, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.pushButton_select = QtGui.QPushButton(Dialog)
        self.pushButton_select.setObjectName("pushButton_select")
        self.gridLayout.addWidget(self.pushButton_select, 6, 1, 1, 2)
        self.label_2.setBuddy(self.comboBox_form)
        self.label.setBuddy(self.comboBox_makam)
        self.label_3.setBuddy(self.comboBox_usul)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.comboBox_makam, self.comboBox_form)
        Dialog.setTabOrder(self.comboBox_form, self.comboBox_usul)
        Dialog.setTabOrder(self.comboBox_usul, self.pushButton_query)
        Dialog.setTabOrder(self.pushButton_query, self.tableView_score)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_query.setText(QtGui.QApplication.translate("Dialog", "Query", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Filter form:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Filter makam:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Filter usul:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_select.setText(QtGui.QApplication.translate("Dialog", "Select", None, QtGui.QApplication.UnicodeUTF8))

