import sys

from design.makam_main_design import Ui_MainWindow
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


class MainMakam(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # setting the interface
        super(MainMakam, self).__init__(parent)
        # setting the qt-designer design
        self.setupUi(self)

        # title of the window
        self.setWindowTitle('Turkish Makam Music Corpus')

        # proxy modal
        self.proxy_modal = QtGui.QSortFilterProxyModel()

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

        # signals
        # buttons
        self.toolButton_query.clicked.connect(self.do_query)

    def do_query(self):
        # gazel and taksim uuids
        GAZEL = u'a1d59289-ea72-4050-9253-01ca12bb5556'
        TAKSIM = u'b4658cef-f3cd-4ced-a534-1dd0a0d5b2de'

        # setting the push button disable
        self.toolButton_query.setDisabled(True)

        # getting the user selections
        makam_id = get_attribute_id(self.makams, self.comboBox_makam.currentIndex())
        form_id = get_attribute_id(self.forms, self.comboBox_form.currentIndex())
        usul_id = get_attribute_id(self.usuls, self.comboBox_usul.currentIndex())

        # arranging the recordings and works for the filtering process
        lengths_recording_taksims = []
        lengths_recording_gazels = []
        lenghts_works = []

        # if makam is selected
        if makam_id != -1:
            data = compmusic.dunya.makam.get_makam(makam_id)
            makam_works = data['works']
            lenghts_works.append([makam_works, len(makam_works)])

            # merging the recordings
            lengths_recording_taksims.append([data['taksims'], len(data['taksims'])])
            lengths_recording_gazels.append([data['gazels'], len(data['gazels'])])

        # if usul is selected
        if usul_id != -1:
            data = compmusic.dunya.makam.get_usul(usul_id)
            usul_works = data['works']
            lenghts_works.append([usul_works, len(usul_works)])

            # merging the recordings
            lengths_recording_taksims.append([data['taksims'], len(data['taksims'])])
            lengths_recording_gazels.append([data['gazels'], len(data['gazels'])])

        # if form is selected
        if form_id != -1:
            # TODO: add only taksim or gazel selection
            data = compmusic.dunya.makam.get_form(form_id)
            form_works = data['works']
            lenghts_works.append([form_works, len(form_works)])

        # sorting the lengths
        lenghts_works = sorted(lenghts_works, key=lambda x: x[1])[::-1]
        lengths_recording_gazels = sorted(lengths_recording_gazels, key=lambda x: x[1])[::-1]
        lengths_recording_taksims = sorted(lengths_recording_taksims, key=lambda x: x[1])[::-1]

        # filtering
        recording_list = []
        if len(lenghts_works) == 3:
            work_list = [common for common in
                         [common for common in lenghts_works[0][0] if common in lenghts_works[1][0]]
                         if common in lenghts_works[2][0]]

            if form_id == TAKSIM:
                recording_list = [common for common in [common for common in lengths_recording_taksims[0][0]
                                                        if common in lengths_recording_taksims[1][0]]
                                  if common in lengths_recording_taksims[2][0]]
            elif form_id == GAZEL:
                recording_list = [common for common in [common for common in lengths_recording_gazels[0][0]
                                                        if common in lengths_recording_gazels[1][0]]
                                  if common in lengths_recording_gazels[2][0]]

        elif len(lenghts_works) == 2:
            work_list = [common for common in lenghts_works[0][0] if common in lenghts_works[1][0]]

            if form_id == -1:
                recording_list = lengths_recording_taksims[0][0] + lengths_recording_gazels[0][0]
            elif form_id == TAKSIM:
                recording_list = lengths_recording_taksims[0][0]
            elif form_id == GAZEL:
                recording_list = lengths_recording_gazels[0][0]

        else:
            work_list = lenghts_works[0][0]
            recording_list = lengths_recording_gazels[0][0] + lengths_recording_taksims[0][0]

        self.work_list = work_list
        self.recording_list = recording_list

        # for element in lengths_recording: print element

        self.set_table(work_list, recording_list)
        self.toolButton_query.setEnabled(True)

    def set_table(self, score_list, recording_list):
        # setting the table for no edit and row selection
        #self.tableView_results.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        #self.tableView_results.setSelectionBitemehavior(QtGui.QAbstractItemView.SelectRows)

        # setting the modal
        model = QtGui.QStandardItemModel(self)

        # getting the related audio-recordings

        for xx, element in enumerate(score_list):
            work_data = compmusic.dunya.makam.get_work(element['mbid'])
            for rec in work_data['recordings']:
                print work_data['title'], rec['artists']
            #for rec in compmusic.dunya.makam.get_work(element['mbid'])['recordings']: print rec


        '''
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
        # self.tableView_score.hideColumn(1)
        self.tableView_score.resizeColumnsToContents()
        self.tableView_score.resizeRowsToContents()
        '''


app = QtGui.QApplication(sys.argv)
dialog = MainMakam()
dialog.show()
app.exec_()
