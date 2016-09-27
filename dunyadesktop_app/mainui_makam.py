from __future__ import print_function
from __future__ import absolute_import
import sys

from PyQt4 import QtGui

from cultures import apiconfig
from cultures.makam import utilities
from cultures.makam.query import QueryThread
from mainui_design_makam import MainWindowMakamDesign

apiconfig.set_token()
apiconfig.set_hostname()


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

        # signals
        self.frame_attributes.toolButton_query.clicked.connect(self.query)
        self.thread_query.progress_number.connect(self.set_progress_number)
        self.thread_query.query_completed.connect(self.test)
        self.thread_query.fetching_completed.connect(self.work_received)
        self.recording_model.rec_fetched.connect(self.append_recording)

    def _set_combobox_attributes(self):
        self.frame_attributes.comboBox_melodic.add_items(self.makams)
        self.frame_attributes.comboBox_form.add_items(self.forms)
        self.frame_attributes.comboBox_rhythm.add_items(self.usuls)
        self.frame_attributes.comboBox_composer.add_items(self.composers)
        self.frame_attributes.comboBox_performer.add_items(self.performers)
        self.frame_attributes.comboBox_instrument.add_items(self.instruments)

    def query(self):
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
        self.recordings.append(type(str(rec_mbid.toUtf8())))

    def work_received(self, work):
        self.work_count += 1
        self.progress_bar.update_progress_bar(self.work_count,
                                              self.progress_number)
        self.recording_model.add_recording(work)
        self.tableView_results.resizeColumnToContents(1)
        self.tableView_results.setColumnWidth(0, 28)

    def test(self):
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("{0}/{1}".format(index, work_number))
        self.frame_attributes.toolButton_query.setEnabled(True)
        print("yes, completed...")

app = QtGui.QApplication(sys.argv)
mainwindow_makam = MainWindowMakam()
mainwindow_makam.show()
app.exec_()
