#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from ui_files.makam_main_design import Ui_MainWindow
from PyQt4 import QtCore, QtGui

import time
import os
import webbrowser

import compmusic.dunya.makam
from utilities import utilities

# multiprocessing and threading
from threading import Thread
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool as Pool

# setting the token
compmusic.dunya.conn.set_token('***REMOVED***')

# gazel and taksim uuids
GAZEL = u'a1d59289-ea72-4050-9253-01ca12bb5556'
TAKSIM = u'b4658cef-f3cd-4ced-a534-1dd0a0d5b2de'


def show_checked_index(topLeft, bottomRight):
    print "signal"
    print topLeft.row(), topLeft.column(), 'topLeft'
    print bottomRight.row(), bottomRight.column()


class MainMakam(QtGui.QMainWindow, Ui_MainWindow):
    # signals for query
    query_finished = QtCore.pyqtSignal()
    query_step_done = QtCore.pyqtSignal()

    # signal for downloading audio
    download_audio_finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        # setting the interface
        super(MainMakam, self).__init__(parent)
        # setting the qt-designer design
        self.setupUi(self)

        # title of the window
        self.setWindowTitle('Dunya Desktop')

        # proxy modal
        self.proxy_model = QtGui.QSortFilterProxyModel()

        # creating the table model
        # setting the column and row
        self.recording_model = QtGui.QStandardItemModel()

        # progress bar
        self.progress_bar = QtGui.QProgressBar()
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.setGeometry(30, 40, 200, 25)
        # hiding the progress bar
        self.progress_bar.setVisible(False)

        # horizontal header for filtering the results
        self.horizontal_header = self.tableView_results.horizontalHeader()

        # fetching makam,usul and form data from dunya
        self.makams = compmusic.dunya.makam.get_makams()
        self.makams = utilities.sort_dictionary(self.makams, 'name')

        self.usuls = compmusic.dunya.makam.get_usuls()
        self.usuls = utilities.sort_dictionary(self.usuls, 'name')

        self.forms = compmusic.dunya.makam.get_forms()
        self.forms = utilities.sort_dictionary(self.forms, 'name')

        self.composers = compmusic.dunya.makam.get_composers()
        self.composers = utilities.sort_dictionary(self.composers, 'name')

        self.performers = compmusic.dunya.makam.get_artists()
        self.performers = utilities.sort_dictionary(self.performers, 'name')

        self.instruments = compmusic.dunya.makam.get_instruments()
        self.instruments = utilities.sort_dictionary(self.instruments, 'name')

        # setting the combobox
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_makam = utilities.set_combobox(self.comboBox_makam,
                                                     self.makams)
        self.comboBox_makam.lineEdit().setPlaceholderText("Makam...")
        self.comboBox_makam.lineEdit().setFont(font)

        self.comboBox_form = utilities.set_combobox(self.comboBox_form,
                                                    self.forms)
        self.comboBox_form.lineEdit().setFont(font)
        self.comboBox_form.lineEdit().setPlaceholderText("Form")

        self.comboBox_usul = utilities.set_combobox(self.comboBox_usul,
                                                    self.usuls)
        self.comboBox_usul.lineEdit().setPlaceholderText("Usul")
        self.comboBox_usul.lineEdit().setFont(font)

        self.comboBox_composer = utilities.set_combobox(self.comboBox_composer,
                                                        self.composers)
        self.comboBox_composer.lineEdit().setPlaceholderText('Composer...')
        self.comboBox_composer.lineEdit().setFont(font)

        self.comboBox_performer = utilities.set_combobox(self.comboBox_performer,
                                                         self.performers)
        self.comboBox_performer.lineEdit().setPlaceholderText('Performer...')
        self.comboBox_performer.lineEdit().setFont(font)

        self.comboBox_instrument = utilities.set_combobox(self.comboBox_instrument,
                                                          self.instruments)
        self.comboBox_instrument.lineEdit().setPlaceholderText('Instrument...')
        self.comboBox_instrument.lineEdit().setFont(font)

        # query index for progress bar
        self.query_index = 0
        self.query_finished.connect(self.add_model_to_table)
        self.query_step_done.connect(lambda: self.update_progress_bar(
            self.query_index, self.work_list))

        # downloading audio
        self.downloading_audio_index = 0
        self.download_audio_finished.connect(lambda:
                                             self.update_progress_bar(
                                                 self.downloading_audio_index,
                                                 self.recording_list))

        # setting filter line editer disabled in the beginning
        self.lineEdit_filter.setDisabled(True)

        # signals
        # buttons
        self.toolButton_query.clicked.connect(self.query_thread)
        self.toolButton_query.clicked.connect(lambda:
                                              self.progress_bar.setVisible(
                                                  True))
        self.toolButton_download_audio.clicked.connect(
                                                    self.download_audio_thread)

        # line edit
        self.lineEdit_filter.textChanged.connect(self.filtering_the_table)
        # table signals
        self.tableView_results.doubleClicked.connect(
                                            self.get_selection_double_click)
        self.horizontal_header.sectionClicked.connect(self.header_filter)

    @QtCore.pyqtSlot(int)
    def header_filter(self, index):
        # filter for table header
        self.horizontal_header_menu = QtGui.QMenu()
        self.header_signal_mapper = QtCore.QSignalMapper()
        self.column_index = index
        # getting the unique values in the selected column
        # getting row values
        row_values = [
            str(self.recording_model.item(row, index).text().toUtf8())
            for row in range(self.recording_model.rowCount())]
        # getting unique one
        unique_values = []
        for row in row_values:
            for element in row.split(','):
                unique_values.append(element.strip())
        unique_values = sorted(set(unique_values))

        # action for selecting all values
        action_all = QtGui.QAction('All', self)
        self.horizontal_header_menu.addAction(action_all)
        self.horizontal_header_menu.addSeparator()

        action_all.triggered.connect(self.on_action_all_triggered)

        for action_index, action_name in enumerate(unique_values):
            action = QtGui.QAction(action_name.decode('utf-8', 'ignore'), self)
            action.setCheckable(True)
            self.header_signal_mapper.setMapping(action, action_index)
            action.triggered.connect(self.header_signal_mapper.map)
            self.horizontal_header_menu.addAction(action)

        self.header_signal_mapper.mapped.connect(self.on_signal_mapper)

        header_pos = self.tableView_results.mapToGlobal(
            self.horizontal_header.pos())

        pos_y = header_pos.y() + self.horizontal_header.height()
        pos_x = header_pos.x() + self.horizontal_header.sectionPosition(
            self.column_index)

        self.horizontal_header_menu.exec_(QtCore.QPoint(pos_x, pos_y))

    def on_action_all_triggered(self):
        filter_string = QtCore.QRegExp("", QtCore.Qt.CaseInsensitive)
        self.proxy_model.setFilterRegExp(filter_string)
        self.proxy_model.setFilterKeyColumn(self.column_index)

    def on_signal_mapper(self, index):
        action_string = self.header_signal_mapper.mapping(index).text()
        filter_string = QtCore.QRegExp(action_string,
                                       QtCore.Qt.CaseInsensitive)
        self.proxy_model.setFilterRegExp(filter_string)
        self.proxy_model.setFilterKeyColumn(self.column_index)

    def get_selection_double_click(self):
        webbrowser.open(url=u"https://musicbrainz.org/recording/{0:s}".format(
            self.recording_list[self.tableView_results.currentIndex().row()][
                'mbid']))

    def update_progress_bar(self, index, fulllist):
        """Updates the progressbar while querying"""

        progress = (float(index) / len(fulllist)) * 100
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("{0}/{1}".format(index, len(fulllist)))
        self.progress_bar.setValue(progress)

    def query_thread(self):
        """Creates a thread for querying"""

        query_thread = Thread(target=self.do_query)
        query_thread.start()

    def download_audio_thread(self):
        self.progress_bar.setVisible(True)
        self.toolButton_download_audio.setDisabled(True)

        query_thread = Thread(target=self.download_audio_parallel)
        query_thread.start()

    def download_audio_parallel(self):
        if not os.path.isdir("audio"):
            os.makedirs("audio")

        for rec in self.recording_list:
            self.download_audio(rec)

        self.progress_bar.setVisible(False)
        self.toolButton_download_audio.setEnabled(True)

    def download_audio(self, rec):
        try:
            print(rec['title'], 'is downloading')
            compmusic.dunya.makam.download_mp3(rec['mbid'], "audio")
        except:
            print('error with item')
        self.downloading_audio_index += 1
        self.download_audio_finished.emit()

    def filtering_the_table(self):
        """Insensitive case filter for line edit"""

        # setting the case
        reg_exp = QtCore.QRegExp(self.lineEdit_filter.text(),
                                 QtCore.Qt.CaseInsensitive)
        self.proxy_model.setFilterRegExp(reg_exp)

    def do_query(self):
        """fetches the recordings"""
        self.tableView_results.setDisabled(True)
        # setting the push button disable
        self.toolButton_query.setDisabled(True)

        # getting the user selections
        makam_id = utilities.get_attribute_id(self.makams,
                                              self.comboBox_makam.currentIndex())
        form_id = utilities.get_attribute_id(self.forms,
                                             self.comboBox_form.currentIndex())
        usul_id = utilities.get_attribute_id(self.usuls,
                                             self.comboBox_usul.currentIndex())

        # arranging the recordings and works for the filtering process
        length_recording_taksims = []
        length_recording_gazels = []
        length_works = []

        # if makam is selected
        if makam_id != -1:
            data = compmusic.dunya.makam.get_makam(makam_id)
            length_works.append([data['works'], len(data['works'])])

            # merging the recordings
            length_recording_taksims.append(
                [data['taksims'], len(data['taksims'])])
            length_recording_gazels.append(
                [data['gazels'], len(data['gazels'])])

        # if usul is selected
        if usul_id != -1:
            data = compmusic.dunya.makam.get_usul(usul_id)
            length_works.append([data['works'], len(data['works'])])

            # merging the recordings
            length_recording_taksims.append(
                [data['taksims'], len(data['taksims'])])
            length_recording_gazels.append(
                [data['gazels'], len(data['gazels'])])

        # if form is selected
        if form_id != -1:
            # TODO: add only taksim or gazel selection
            data = compmusic.dunya.makam.get_form(form_id)
            length_works.append([data['works'], len(data['works'])])

        # sorting the lengths
        length_works = sorted(length_works, key=lambda x: x[1])[::-1]
        length_recording_gazels = sorted(length_recording_gazels,
                                         key=lambda x: x[1])[::-1]
        length_recording_taksims = sorted(length_recording_taksims,
                                          key=lambda x: x[1])[::-1]

        # filtering
        recording_list = []
        # if all attributes are selected by the user
        if len(length_works) == 3:
            work_list = [common for common in
                         [common for common in length_works[0][0] if
                          common in length_works[1][0]]
                         if common in length_works[2][0]]

            if form_id == TAKSIM:
                recording_list = [common for common in
                                  [common for common in
                                   length_recording_taksims[0][0] if common in
                                   length_recording_taksims[1][0]]
                                  if common in length_recording_taksims[2][0]]
            elif form_id == GAZEL:
                recording_list = [common for common in
                                  [common for common in
                                   length_recording_gazels[0][0] if common in
                                   length_recording_gazels[1][0]]
                                  if common in length_recording_gazels[2][0]]

        elif len(length_works) == 2:
            work_list = [common for common in length_works[0][0] if
                         common in length_works[1][0]]

            if form_id == -1:
                recording_list = length_recording_taksims[0][0] + \
                                 length_recording_gazels[0][0]
            elif form_id == TAKSIM:
                recording_list = length_recording_taksims[0][0]
            elif form_id == GAZEL:
                recording_list = length_recording_gazels[0][0]
        else:
            # if form is not selected
            if form_id == -1:
                work_list = length_works[0][0]
                recording_list = length_recording_gazels[0][0] + \
                                 length_recording_taksims[0][0]

            elif form_id != -1:
                if form_id != GAZEL or form_id != TAKSIM:
                    work_list = length_works[0][0]
                    recording_list = []
                else:
                    # TODO: Add only taksim or gazel selection
                    work_list = length_works[0][0]

        # recording list
        self.recording_list = recording_list
        self.work_list = work_list

        self.fetch_related_recs(work_list)

        # enabling the query button
        self.toolButton_query.setEnabled(True)

    def fetch_related_recs(self, score_list):
        """Fetches the related recordings"""

        # creating a pool for multi-processing
        pool = Pool(cpu_count())
        for element in score_list:
            pool.apply_async(self.fetching_recs_of_works, (element,))
        pool.close()

        # starting the multi-processing
        pool.join()

        # sorting the recording dictionary
        self.recording_list = utilities.sort_dictionary(self.recording_list,
                                                        'title')

        # arranging the rows of the model
        self.recording_model.setHorizontalHeaderLabels(['', 'Title',
                                                        'Artists'])
        self.recording_model.setRowCount(len(self.recording_list))

        # adding items to the model
        for row, item in enumerate(self.recording_list):
            # creating an item
            title_item = QtGui.QStandardItem(item['title'])

            # creating an item for artists column.
            artists = ''
            # appending all artists in the same item
            # removing the duplicate artists
            item['artists'] = [dict(tupleized) for tupleized in
                               set(tuple(element.items())
                                   for element in item['artists'])]

            for artist in item['artists']:
                artists += artist['name'] + ", "
            artists = artists[:-2]
            artist_item = QtGui.QStandardItem(artists)

            check_item = QtGui.QStandardItem()
            check_item.setCheckable(True)
            # setting the items in to the model
            self.recording_model.setItem(row, 0, check_item)
            self.recording_model.setItem(row, 1, title_item)
            self.recording_model.setItem(row, 2, artist_item)

        self.query_finished.emit()

    def fetching_recs_of_works(self, element):
        """This function is used for the multiprocess"""
        try:
            work_data = compmusic.dunya.makam.get_work(element['mbid'])
            for rec in work_data['recordings']:
                self.recording_list.append(rec)
        except:
            print('error with item')
        self.query_index += 1
        self.query_step_done.emit()

    def add_model_to_table(self):
        """Adds the created model to table"""
        # setting the table for no edit and row selection
        self.tableView_results.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView_results.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)

        self.tableView_results.setEnabled(True)

        # hiding the vertical headers
        self.tableView_results.verticalHeader().hide()

        # arranging the artist column for being multi-line
        self.tableView_results.setWordWrap(True)
        self.tableView_results.setTextElideMode(QtCore.Qt.ElideMiddle)

        # setting the model
        self.proxy_model.setSourceModel(self.recording_model)

        # filtering affects all columns by setting it as -1
        self.proxy_model.setFilterKeyColumn(-1)

        # setting the proxy model to the table
        self.tableView_results.setModel(self.proxy_model)

        # filter line edit is enabled
        self.lineEdit_filter.setEnabled(True)

        # setting the widths of rows and columns
        self.tableView_results.horizontalHeader().setStretchLastSection(True)
        self.tableView_results.resizeColumnToContents(1)
        self.tableView_results.setColumnWidth(0, 28)
        self.tableView_results.resizeRowsToContents()

        self.query_index = 0
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.recording_model.dataChanged.connect(show_checked_index)


app = QtGui.QApplication(sys.argv)
dialog = MainMakam()
dialog.show()
app.exec_()
