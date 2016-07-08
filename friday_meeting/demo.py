import sys

from demo_design import Ui_Dialog
from PySide import QtCore, QtGui

import compmusic.dunya.makam
import time
import webbrowser

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
        self.setWindowTitle('CompMusic Makam Works')

        # fetching makam,usul and form data from dunya
        self.makams = compmusic.dunya.makam.get_makams()
        self.makams = sort_dictionary(self.makams)

        self.usuls = compmusic.dunya.makam.get_usuls()
        self.usuls = sort_dictionary(self.usuls)

        self.forms = compmusic.dunya.makam.get_forms()
        self.forms = sort_dictionary(self.forms)

        self.work_metadata = compmusic.dunya.makam.get_works()

        # setting the combobox
        self.comboBox_makam = set_combobox(self.comboBox_makam, self.makams)
        self.comboBox_form = set_combobox(self.comboBox_form, self.forms)
        self.comboBox_usul = set_combobox(self.comboBox_usul, self.usuls)

        # signals
        # buttons
        self.pushButton_query.clicked.connect(self.do_query)
        self.pushButton_select.clicked.connect(self.get_selection_button)

        # table signals
        self.tableView_score.doubleClicked.connect(self.get_selection_double_click)

    def get_selection_double_click(self):
        webbrowser.open(url=u"https://musicbrainz.org/work/{0:s}".format(
            self.work_list[self.tableView_score.currentItem().row()]['mbid']))

    def get_selection_button(self):
        print self.work_list[self.tableView_score.currentItem().row()]['mbid']
        #self.open_recordings()

    #def open_recordings(self):
    #    self.wid = QtGui.QWidget()
    #    self.wid.resize(250, 150)
    #    self.wid.setWindowTitle('NewWindow')
    #    self.wid.show()

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
            work_list = [common for common in [common for common in lenghts[0][0] if common in lenghts[1][0]]
                         if common in lenghts[2][0]]
        elif len(lenghts) == 2:
            work_list = [common for common in lenghts[0][0] if common in lenghts[1][0]]
        else:
            work_list = lenghts[0][0]

        self.work_list = work_list
        self.set_table(work_list)
        self.pushButton_query.setEnabled(True)

    def set_table(self, score_list):
        self.tableView_score.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView_score.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.tableView_score.setRowCount(len(score_list))
        self.tableView_score.setColumnCount(2)
        self.tableView_score.verticalHeader().setVisible(False)

        for xx, element in enumerate(score_list):
            title = QtGui.QTableWidgetItem(element['title'])
            self.tableView_score.setItem(xx, 0, title)

            work_metadata = (item for item in self.work_metadata if item["mbid"] == element['mbid']).next()
            if work_metadata['composers']:
                composer = QtGui.QTableWidgetItem(work_metadata['composers'][0]['name'])
                self.tableView_score.setItem(xx, 1, composer)

        self.tableView_score.setHorizontalHeaderLabels(['Title', 'Composer'])
        #self.tableView_score.hideColumn(1)
        self.tableView_score.resizeColumnsToContents()
        self.tableView_score.resizeRowsToContents()


app = QtGui.QApplication(sys.argv)
dialog = DemoDialog()
dialog.show()
app.exec_()
