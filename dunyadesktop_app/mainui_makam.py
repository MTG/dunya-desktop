from __future__ import absolute_import
import sys

from PyQt4 import QtGui

from compmusic.dunya import makam

from cultures import apiconfig
from cultures.makam import utilities
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

        self.frame_attributes.toolButton_query.clicked.connect(self.query)

    def _set_combobox_attributes(self):
        self.frame_attributes.comboBox_melodic.add_items(self.makams)
        self.frame_attributes.comboBox_form.add_items(self.forms)
        self.frame_attributes.comboBox_rhythm.add_items(self.usuls)
        self.frame_attributes.comboBox_composer.add_items(self.composers)
        self.frame_attributes.comboBox_performer.add_items(self.performers)
        self.frame_attributes.comboBox_instrument.add_items(self.instruments)

    def query(self):
        mid = self.frame_attributes.comboBox_melodic.get_attribute_id()
        fid = self.frame_attributes.comboBox_form.get_attribute_id()
        uid = self.frame_attributes.comboBox_rhythm.get_attribute_id()
        cmbid = self.frame_attributes.comboBox_performer.get_attribute_id()
        ambid = self.frame_attributes.comboBox_composer.get_attribute_id()

        print makam.get_works_by_query(mid, uid, fid, cmbid, ambid)


app = QtGui.QApplication(sys.argv)
mainwindow_makam = MainWindowMakam()
mainwindow_makam.show()
app.exec_()
