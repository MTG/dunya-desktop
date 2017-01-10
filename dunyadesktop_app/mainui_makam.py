import sys
import os
import Queue

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox

from cultures import apiconfig
from cultures.makam import utilities
from cultures.makam.query import QueryThread
from mainui_design_makam import MainWindowMakamDesign
from widgets.playerdialog import PlayerDialog
from widgets.playermainwindow import PlayerMainWindow
from utilities import database

apiconfig.set_token()
# apiconfig.set_hostname()

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')


class MainWindowMakam(MainWindowMakamDesign):
    """The main window of makam"""
    def __init__(self):
        MainWindowMakamDesign.__init__(self)

        # check if dunya is up or not
        if utilities.is_dunya_up():
            # fetches the attributes and sets the comboboxes
            (self.makams, self.forms, self.usuls, self.composers,
             self.performers, self.instruments) = utilities.get_attributes()
            self._set_combobox_attributes()
            self.frame_query.frame_attributes.comboBox_instrument.setDisabled(True)
            self.recordings = []
            self.work_count = 0
            self.progress_number = 0
            self.d_threads = []
            self.q_threads = []
            self.queue = Queue.Queue()

            # signals
            self.online_status = True

        else:
            # working in offline mode
            self.frame_query.setDisabled(True)
            QMessageBox.information(self, "QMessageBox.information()",
                                    "Dunya-desktop is working in offline "
                                    "mode.")
            self.dwc_top.label_status.setText('Offline')
            self.online_status = False

        # creating db
        self._set_collections()
        self.download_queue = []

        # signals

        self.frame_query.frame_attributes.toolButton_query.clicked.connect(
            self.query)

        self.frame_query.recording_model.rec_fetched.connect(
            self.append_recording)

        # filtering the results
        self.frame_query.lineEdit_filter.textChanged.connect(
            lambda: self.frame_query.proxy_model.filter_table(
                self.frame_query.lineEdit_filter.text()))
        self.frame_query.tableView_results.add_maincoll.triggered.connect(
            lambda: self.download_related_features(
                self.frame_query.tableView_results.index))

        self.dwc_left.listView_collections.index_changed.connect(
            self.update_coll_list)
        self.dwc_left.tableView_downloaded.added_new_doc.connect(
            self.check_new_doc)

        self.frame_query.tableView_results.open_dunya_triggered.connect(
            self.open_player)
        self.dwc_left.tableView_downloaded.open_dunya_triggered.connect(
            self.open_player_collection)
        self.frame_query.tableView_results.add_to_collection.connect(
            self.add_received_doc)
        self.dwc_left.tableView_downloaded.set_result_checked.connect(
            self.check_query_table)

    def _set_combobox_attributes(self):
        self.frame_query.frame_attributes.\
            comboBox_melodic.add_items(self.makams)
        self.frame_query.frame_attributes.comboBox_form.add_items(self.forms)
        self.frame_query.frame_attributes.comboBox_rhythm.add_items(self.usuls)
        self.frame_query.frame_attributes.\
            comboBox_composer.add_items(self.composers)
        self.frame_query.frame_attributes.\
            comboBox_performer.add_items(self.performers)
        self.frame_query.frame_attributes.\
            comboBox_instrument.add_items(self.instruments)

    def _set_collections(self):
        conn, c = database.connect(add_main=True)
        database._add_docs_to_maincoll(conn, c)

        colls = database.get_collections(c)
        self.dwc_left.listView_collections.add_collections(
            [coll[0] for coll in colls])
        conn.close()

    def query(self):
        self.recordings = []
        self.work_count = 0
        self.frame_query.recording_model.clear_items()
        self.frame_query.frame_attributes.toolButton_query.setEnabled(False)
        self.frame_query.lineEdit_filter.setEnabled(True)
        self.frame_query.tableView_results.setEnabled(True)
        self.frame_query.tableView_results.horizontal_header.show()

        mid = self.frame_query.frame_attributes.comboBox_melodic.get_attribute_id()
        fid = self.frame_query.frame_attributes.comboBox_form.get_attribute_id()
        uid = self.frame_query.frame_attributes.comboBox_rhythm.get_attribute_id()
        cmbid = self.frame_query.frame_attributes.comboBox_composer.get_attribute_id()
        ambid = self.frame_query.frame_attributes.comboBox_performer.get_attribute_id()

        q_thread = QueryThread(parent=self)
        q_thread.mid = mid
        q_thread.fid = fid
        q_thread.uid = uid
        q_thread.cmbid = cmbid
        q_thread.ambid = ambid

        self.q_threads.append(q_thread)

        self.progress_bar.setVisible(True)
        q_thread.start()

    def set_progress_number(self, progress_number):
        self.progress_number = progress_number.status

    def append_recording(self, rec_mbid):
        self.recordings.append(str(rec_mbid))
        self.dwc_left.tableView_downloaded.recordings = self.recordings

    def work_received(self, work):
        self.work_count += 1
        self.progress_bar.update_progress_bar(self.work_count,
                                              self.progress_number)
        self.frame_query.recording_model.add_recording(work.work)
        self.frame_query.tableView_results.resizeColumnToContents(1)
        self.frame_query.tableView_results.setColumnWidth(0, 28)

    def change_combobox_backgrounds(self, status):
        combobox_status = status.results
        color_palette = {0: '', 1: '#D9F4DD', 2: '#F4D1D0'}
        self.frame_query.frame_attributes.comboBox_melodic.change_background(
            color=color_palette[combobox_status[0]])
        self.frame_query.frame_attributes.comboBox_form.change_background(
            color=color_palette[combobox_status[1]])
        self.frame_query.frame_attributes.comboBox_rhythm.change_background(
            color=color_palette[combobox_status[2]])
        self.frame_query.frame_attributes.comboBox_composer.change_background(
            color=color_palette[combobox_status[3]])
        self.frame_query.frame_attributes.comboBox_performer.change_background(
            color=color_palette[combobox_status[4]])

    def query_finished(self):
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("")
        self.frame_query.frame_attributes.toolButton_query.setEnabled(True)
        self.q_threads = []

    def download_related_features(self, index):
        source_index = self.frame_query.tableView_results.model().mapToSource(index)
        self.recid = self.recordings[source_index.row()]

    def open_player_collection(self, index):
        coll = str(self.dwc_left.listView_collections.currentItem().text())
        conn, c = database.connect()
        try:
            docid = database.get_nth_row(c, coll, index.row())[0]
            conn.close()
            player = PlayerMainWindow(docid=docid, parent=self)
            player.show()
        except:
            QMessageBox.information(self, "Cannot open the player!")

    def open_player(self, index):
        if not self.q_threads:
            model_index = self.frame_query.tableView_results.model().mapToSource(index)
            recid = self.recordings[model_index.row()]

            player = PlayerMainWindow(docid=recid, parent=self)
            player.show()
        else:
            QMessageBox.information(self, "QMessageBox.information()",
                                    "Player can not be opened until querying "
                                    "finishes")

    def update_coll_list(self, coll):
        conn, c = database.connect()
        raw = database.fetch_collection(c, coll)
        self.dwc_left.tableView_downloaded.coll = coll
        self.dwc_left.tableView_downloaded.create_table([item[0] for item in raw])
        self.dwc_left.change_downloaded_text(coll)

    def add_received_doc(self, coll, index):
        conn, c = database.connect()
        source_index = self.frame_query.tableView_results.model().mapToSource(index)
        docid = self.recordings[source_index.row()]
        if database.add_doc_to_coll(conn, c, docid, coll):
            self.dwc_left.tableView_downloaded.add_item(docid)
            self.dwc_left.tableView_downloaded.indexes[self.recordings[source_index.row()]] = \
                self.dwc_left.tableView_downloaded.rowCount() - 1
            self.check_new_doc([docid])

    def check_new_doc(self, docs):
        download = []
        for docid in docs:
            if not os.path.isdir(os.path.join(DOCS_PATH, str(docid))):
                download.append(str(docid))
        d_thread = utilities.DocThread(self.queue,
                                       self.dwc_left.tableView_downloaded.set_progress_bar)
        if download:
            self.d_threads.append(d_thread)
            d_thread.start()

            for doc in download:
                self.queue.put(doc)
            self.queue.put(None)  # tells the workers to shut down

    def check_query_table(self, docid):
        try:
            row = self.recordings.index(docid)
            self.frame_query.tableView_results.model().sourceModel().set_checked([row])
        except:
            pass


app = QApplication(sys.argv)
mainwindow_makam = MainWindowMakam()
mainwindow_makam.show()
app.exec_()
