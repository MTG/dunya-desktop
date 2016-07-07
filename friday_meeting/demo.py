import sys
import operator

from demo_design import Ui_Dialog
from PySide import QtCore, QtGui

import compmusic.dunya.makam
import time

# setting the token
compmusic.dunya.conn.set_token('***REMOVED***')


def sort_dictionary(dictionary):
    dictionary = sorted(dictionary, key=lambda k: k['name'])
    return dictionary


def set_combobox(combobox, attribute):
    combobox.setEditable(True)
    combobox.setInsertPolicy(QtGui.QComboBox.NoInsert)

    for elememt in attribute:
        combobox.addItem(elememt['name'])
    combobox.setCurrentIndex(-1)
    return combobox


def get_attribute_id(attribute, index):
    if index is not -1:
        return attribute[index]['uuid']
    else:
        return -1


class DemoDialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(DemoDialog, self).__init__(parent)
        # setting the qt-designer design
        self.setupUi(self)

        # fetching makam,usul and form data from dunya
        self.makams = compmusic.dunya.makam.get_makams()
        self.makams = sort_dictionary(self.makams)

        self.usuls = compmusic.dunya.makam.get_usuls()
        self.usuls = sort_dictionary(self.usuls)

        self.forms = compmusic.dunya.makam.get_forms()
        self.forms = sort_dictionary(self.forms)

        # setting the combobox
        self.comboBox_makam = set_combobox(self.comboBox_makam, self.makams)
        self.comboBox_form = set_combobox(self.comboBox_form, self.forms)
        self.comboBox_usul = set_combobox(self.comboBox_usul, self.usuls)

        self.pushButton_query.clicked.connect(self.do_query)

    def do_query(self):
        self.pushButton_query.setDisabled(True)
        makam_id = get_attribute_id(self.makams, self.comboBox_makam.currentIndex())
        usul_id = self.comboBox_form.currentIndex()
        form_id = self.comboBox_usul.currentIndex()

        filtered_list = []

        if makam_id is not -1:
            data = compmusic.dunya.makam.get_makam(makam_id)

        self.pushButton_query.setEnabled(True)
        #print makam_id, usul_id, form_id
        #print selected_makam_id, selected_usul, selected_form



app = QtGui.QApplication(sys.argv)
dialog = DemoDialog()
dialog.show()
app.exec_()
