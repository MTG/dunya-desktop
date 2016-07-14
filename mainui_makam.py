import sys

from design.makam_main_design import Ui_MainWindow
from PySide import QtCore, QtGui

import compmusic.dunya.makam
import time
import os

from multiprocessing.pool import ThreadPool as Pool
from threading import Thread

# setting the token
compmusic.dunya.conn.set_token('***REMOVED***')


def sort_dictionary(dictionary, key):
    """sorts the given dictionary according to the keys"""
    dictionary = sorted(dictionary, key=lambda k: k[key])
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
        self.proxy_model = QtGui.QSortFilterProxyModel()

        # fetching makam,usul and form data from dunya
        self.makams = compmusic.dunya.makam.get_makams()
        self.makams = sort_dictionary(self.makams, 'name')

        self.usuls = compmusic.dunya.makam.get_usuls()
        self.usuls = sort_dictionary(self.usuls, 'name')

        self.forms = compmusic.dunya.makam.get_forms()
        self.forms = sort_dictionary(self.forms, 'name')

        # setting the combobox
        self.comboBox_makam = set_combobox(self.comboBox_makam, self.makams)
        self.comboBox_form = set_combobox(self.comboBox_form, self.forms)
        self.comboBox_usul = set_combobox(self.comboBox_usul, self.usuls)

        # setting filter line editer disabled in the beginning
        self.lineEdit_filter.setDisabled(True)

        self.thread = QtCore.QThread()

        # signals
        # buttons
        self.toolButton_query.clicked.connect(self.do_query)

        #self.toolButton_download_audio.clicked.connect(self.download_audio)
        self.toolButton_download_audio.clicked.connect(self.download_audio_thread)

        # line edit
        self.lineEdit_filter.textChanged.connect(self.filtering_the_table)

    def download_audio_thread(self):
        thread = Thread(target=self.download_audio)
        thread.start()

    def download_audio(self):
        if not os.path.isdir("audio"):
            os.makedirs("audio")

        for xx, rec in enumerate(self.recording_list):
            print xx, rec['title']
            compmusic.dunya.makam.download_mp3(rec['mbid'], "audio")

    def filtering_the_table(self):
        """Insensitive case filter"""
        # setting the case
        reg_exp = QtCore.QRegExp(self.lineEdit_filter.text(), QtCore.Qt.CaseInsensitive)

        self.proxy_model.setFilterRegExp(reg_exp)

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

        # recording list
        self.recording_list = recording_list

        # setting the table
        thread = Thread(target=self.set_table, args=(work_list,))
        thread.start()

        #self.set_table(work_list)

        # enabling the query button
        self.toolButton_query.setEnabled(True)

    def set_table(self, score_list):
        # setting the table for no edit and row selection
        self.tableView_results.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView_results.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        # creating a pool for multi-processing
        pool = Pool(4)
        for element in score_list:
            pool.apply_async(self.adding_items_to_table, (element,))
        pool.close()
        # starting the multi-processing
        pool.join()

        # sorting the recording dictionary
        self.recording_list = sort_dictionary(self.recording_list, 'title')

        # creating the table model
        # setting the column and row
        self.model = QtGui.QStandardItemModel(len(self.recording_list), 2)
        self.model.setHorizontalHeaderLabels(['Title', 'Artists'])

        # adding items to the model
        for row, item in enumerate(self.recording_list):
            # creating an item
            title_item = QtGui.QStandardItem(item['title'])

            # setting the created item checkable
            title_item.setCheckable(True)
            title_item.setCheckState(QtCore.Qt.Checked)

            # creating an item for artists column.
            artists = ''
            # appending all artists in the same item
            for artist in item['artists']:
                artists += artist['name'] + ", "

            artist_item = QtGui.QStandardItem(artists)

            # setting the items in to the model
            self.model.setItem(row, 0, title_item)
            self.model.setItem(row, 1, artist_item)

        # setting the model
        self.proxy_model.setSourceModel(self.model)
        # filtering affects all columns by setting it as -1
        self.proxy_model.setFilterKeyColumn(-1)

        # setting the proxy model to the table
        self.tableView_results.setModel(self.proxy_model)

        # filter line edit is enabled
        self.lineEdit_filter.setEnabled(True)

        # hiding the vertical headers
        self.tableView_results.verticalHeader().hide()

        # arranging the artist column for being multi-line
        self.tableView_results.setWordWrap(True)
        self.tableView_results.setTextElideMode(QtCore.Qt.ElideMiddle)

        # setting the widths of rows and columns
        self.tableView_results.horizontalHeader().setStretchLastSection(True)
        self.tableView_results.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableView_results.resizeColumnToContents(0)
        self.tableView_results.resizeRowsToContents()

    def adding_items_to_table(self, element):
        """This function is used for the multiprocess"""
        try:
            work_data = compmusic.dunya.makam.get_work(element['mbid'])
            for rec in work_data['recordings']:
                self.recording_list.append(rec)
        except:
            print('error with item')

app = QtGui.QApplication(sys.argv)
dialog = MainMakam()
dialog.show()
app.exec_()
