import sys

from demo_design import Ui_Dialog
from PySide import QtCore, QtGui

import compmusic.dunya.makam
import time

# setting the token
compmusic.dunya.conn.set_token('***REMOVED***')


def sort_dictionary(dictionary):
    """sorts the given dictionary according to the keys"""
    dictionary = sorted(dictionary, key=lambda k: k['name'])
    return dictionary


def set_combobox(combobox, attribute):
    """Sets the given comboboxes"""
    combobox.setEditable(True)
    combobox.setInsertPolicy(QtGui.QComboBox.NoInsert)

    for elememt in attribute:
        combobox.addItem(elememt['name'])
    combobox.setCurrentIndex(-1)
    return combobox


def get_attribute_id(attribute, index):
    """Returns the mb id of the selected attributes"""
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
        # gazel and taksim uuids
        GAZEL = u'a1d59289-ea72-4050-9253-01ca12bb5556'
        TAKSIM = u'b4658cef-f3cd-4ced-a534-1dd0a0d5b2de'

        # setting the push button disable
        self.pushButton_query.setDisabled(True)

        # getting the user selections
        makam_id = get_attribute_id(self.makams, self.comboBox_makam.currentIndex())
        form_id = get_attribute_id(self.forms, self.comboBox_form.currentIndex())
        usul_id = get_attribute_id(self.usuls, self.comboBox_usul.currentIndex())

        lenghts = []
        if makam_id != -1:
            data = compmusic.dunya.makam.get_makam(makam_id)
            makam_works = data['works']
            lenghts.append([makam_works, len(makam_works)])

        if usul_id != -1:
            usul_works = compmusic.dunya.makam.get_usul(usul_id)['works']
            lenghts.append([usul_works, len(usul_works)])

        if form_id != -1:
            form_works = compmusic.dunya.makam.get_form(form_id)['works']
            lenghts.append([form_works, len(form_works)])

        # sorting the lengths
        lenghts = sorted(lenghts, key=lambda x: x[1])[::-1]

        # filtering
        if len(lenghts) == 3:
            intersection = [common for common in [common for common in lenghts[0][0] if common in lenghts[1][0]]
                            if common in lenghts[2][0]]
        elif len(lenghts) == 2:
            intersection = [common for common in lenghts[0][0] if common in lenghts[1][0]]
        else:
            intersection = lenghts[0][0]

        for element in intersection: print element

        self.pushButton_query.setEnabled(True)
        '''
        if makam_id is not -1:
            data = compmusic.dunya.makam.get_makam(makam_id)

            # if the form is selected as gazel
            if form_id == GAZEL:
                if data['gazels']:
                    query = [recording for recording in data['gazels']]
            elif form_id == TAKSIM:
                if data['taksims']:
                    query = [recording for recording in data['taksims']]

            # checking the recording different than the gazel and taksim form
            else:
                if data['works']:
                    # checking the forms of the works
                    if form_id != -1:
                        works = []
                        for ind, work in enumerate(data['works']):
                            print ind, len(data['works'])
                            metadata = compmusic.dunya.makam.get_work(work['mbid'])
                            for form in metadata['forms']:
                                if form['uuid'] == form_id:
                                    for usul in metadata['usuls']:
                                        if usul['uuid'] == usul_id:
                                            print metadata

                                    #print([metadata['mbid'], metadata['title']])
                                    #works.append(work['mbid'])
                else:
                    print 'No recording'

        self.pushButton_query.setEnabled(True)
        '''

app = QtGui.QApplication(sys.argv)
dialog = DemoDialog()
dialog.show()
app.exec_()
