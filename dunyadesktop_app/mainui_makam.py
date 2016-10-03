from __future__ import print_function
from __future__ import absolute_import
import sys
import webbrowser

from PyQt4 import QtGui, QtCore

from cultures import apiconfig
from cultures.makam import utilities
from cultures.makam.query import QueryThread
from mainui_design_makam import MainWindowMakamDesign

apiconfig.set_token()
#apiconfig.set_hostname()


class MainWindowMakam(MainWindowMakamDesign):
    def __init__(self):
        MainWindowMakamDesign.__init__(self)

        (self.makams, self.forms, self.usuls, self.composers,
         self.performers, self.instruments) = utilities.get_attributes()
        self._set_combobox_attributes()

        self.frame_attributes.comboBox_instrument.setDisabled(True)
        self.recordings = []
        self.work_count = 0
        self.progress_number = 0
        self.thread_query = QueryThread()
        self.thread_feature_downloader = utilities.FeatureDownloaderThread()

        # signals
        self.frame_attributes.toolButton_query.clicked.connect(self.query)

        self.thread_query.combobox_results.connect(
            self.change_combobox_backgrounds)
        self.thread_query.progress_number.connect(self.set_progress_number)
        self.thread_query.query_completed.connect(self.query_finished)
        self.thread_query.fetching_completed.connect(self.work_received)

        self.recording_model.rec_fetched.connect(self.append_recording)

        self.lineEdit_filter.textChanged.connect(
            lambda:self.proxy_model.filtering_the_table(
                self.lineEdit_filter.text()))
        self.tableView_results.doubleClicked.connect(self.show_on_mb)
        self.tableView_results.open_dunya.triggered.connect(
            lambda:self.download_related_features(self.tableView_results.index))

        self.thread_feature_downloader.feautures_downloaded.connect(
            self.open_player)

    def _set_combobox_attributes(self):
        self.frame_attributes.comboBox_melodic.add_items(self.makams)
        self.frame_attributes.comboBox_form.add_items(self.forms)
        self.frame_attributes.comboBox_rhythm.add_items(self.usuls)
        self.frame_attributes.comboBox_composer.add_items(self.composers)
        self.frame_attributes.comboBox_performer.add_items(self.performers)
        self.frame_attributes.comboBox_instrument.add_items(self.instruments)

    def query(self):
        self.recordings = []
        self.work_count = 0
        self.recording_model.clear_items()
        self.frame_attributes.toolButton_query.setEnabled(False)
        self.lineEdit_filter.setEnabled(True)
        self.tableView_results.setEnabled(True)
        self.tableView_results.horizontal_header.show()

        mid = self.frame_attributes.comboBox_melodic.get_attribute_id()
        fid = self.frame_attributes.comboBox_form.get_attribute_id()
        uid = self.frame_attributes.comboBox_rhythm.get_attribute_id()
        cmbid = self.frame_attributes.comboBox_composer.get_attribute_id()
        ambid = self.frame_attributes.comboBox_performer.get_attribute_id()

        self.thread_query.mid = mid
        self.thread_query.fid = fid
        self.thread_query.uid = uid
        self.thread_query.cmbid = cmbid
        self.thread_query.ambid = ambid

        self.progress_bar.setVisible(True)
        self.thread_query.start()

    def set_progress_number(self, progress_number):
        self.progress_number = progress_number

    def append_recording(self, rec_mbid):
        self.recordings.append(str(rec_mbid.toUtf8()))

    def work_received(self, work):
        self.work_count += 1
        self.progress_bar.update_progress_bar(self.work_count,
                                              self.progress_number)
        self.recording_model.add_recording(work)
        self.tableView_results.resizeColumnToContents(1)
        self.tableView_results.setColumnWidth(0, 28)

    def change_combobox_backgrounds(self, combobox_status):
        color_palette = {0: '', 1: '#D9F4DD', 2: '#F4D1D0'}
        self.frame_attributes.comboBox_melodic.change_background(
            color=color_palette[combobox_status[0]])
        self.frame_attributes.comboBox_form.change_background(
            color=color_palette[combobox_status[1]])
        self.frame_attributes.comboBox_rhythm.change_background(
            color=color_palette[combobox_status[2]])
        self.frame_attributes.comboBox_composer.change_background(
            color=color_palette[combobox_status[3]])
        self.frame_attributes.comboBox_performer.change_background(
            color=color_palette[combobox_status[4]])

    def query_finished(self):
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("")
        self.frame_attributes.toolButton_query.setEnabled(True)

    def show_on_mb(self):
        index = self.tableView_results.model().mapToSource(
            self.tableView_results.currentIndex())

        #webbrowser.open(url=u"https://musicbrainz.org/recording/{0}".
        #                format(self.recordings[index.row()]))
    def download_related_features(self, index):
        source_index = self.tableView_results.model().mapToSource(index)
        recid = self.recordings[source_index.row()]
        self.thread_feature_downloader.recid = recid
        self.thread_feature_downloader.run()

    def open_player(self, pitch, pd):
        pass


app = QtGui.QApplication(sys.argv)
mainwindow_makam = MainWindowMakam()
mainwindow_makam.show()
app.exec_()
