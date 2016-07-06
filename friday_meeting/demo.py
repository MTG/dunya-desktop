import sys
import operator

from demo_design import Ui_Dialog
from PySide import QtCore, QtGui

import compmusic.dunya.makam
import time


# setting the token
compmusic.dunya.conn.set_token('***REMOVED***')


def set_combobox(attribute):
    attribute.setEditable(True)
    attribute.setInsertPolicy(QtGui.QComboBox.NoInsert)

    # fetching attribute from dunya
    for element in attribute:
        attribute.addItem(element['name'])
    element.setCurrentIndex(-1)


class DemoDialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(DemoDialog, self).__init__(parent)
        # setting the qt-designer design
        self.setupUi(self)

        # fetching makam,usul and form data from dunya
        self.makams = compmusic.dunya.makam.get_makams()
        self.makams = sorted(self.makams, key=lambda k: k['name'])

        self.usuls = compmusic.dunya.makam.get_usuls()
        self.usuls = sorted(self.usuls, key=lambda k: k['name'])

        self.forms = compmusic.dunya.makam.get_forms()
        self.forms = sorted(self.forms, key=lambda k: k['name'])

        # combobox form
        self.comboBox_form.setEditable(True)
        self.comboBox_form.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.set_form_combobox()

        # combobox usul
        self.comboBox_usul.setEditable(True)
        self.comboBox_form.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.set_usul_combobox()

        # combobox makam
        self.comboBox_makam.setEditable(True)
        self.comboBox_makam.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.set_makam_combobox()

        self.pushButton_query.clicked.connect(self.do_query)

    def do_query(self):
        selected_makam = self.comboBox_makam.currentIndex()
        selected_usul = self.comboBox_form.currentIndex()
        selected_form = self.comboBox_usul.currentIndex()

        print selected_makam, selected_usul, selected_form

    def set_makam_combobox(self):
        # fetching makams from dunya
        for makam in self.makams:
            self.comboBox_makam.addItem(makam['name'])
        self.comboBox_makam.setCurrentIndex(-1)

    def set_usul_combobox(self):
        # fetching forms from dunya
        for form in self.usuls:
            self.comboBox_usul.addItem(form['name'])
        self.comboBox_usul.setCurrentIndex(-1)

    def set_form_combobox(self):
        # fetching forms from dunya
        for form in self.forms:
            self.comboBox_form.addItem(form['name'])
        self.comboBox_form.setCurrentIndex(-1)


app = QtGui.QApplication(sys.argv)
dialog = DemoDialog()
dialog.show()
app.exec_()
