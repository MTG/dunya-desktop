import sys
from cultures import apiconfig
from cultures.makam import utilities

from PyQt4 import QtGui
from mainui_design_makam import MainWindowMakamDesign

apiconfig.set_token()
apiconfig.set_hostname()

class MainWindowMakam(MainWindowMakamDesign):
    def __init__(self):
        MainWindowMakamDesign.__init__(self)

        (self.makams, self.usuls, self.forms, self.composers,
         self.performers, self.instruments) = utilities.get_attributes()
        self._set_combobox_attributes()

    def _set_combobox_attributes(self):
        self.frame_attributes.comboBox_melodic.add_items(self.makams)
        self.frame_attributes.comboBox_form.add_items(self.forms)
        self.frame_attributes.comboBox_rhythm.add_items(self.usuls)
        self.frame_attributes.comboBox_composer.add_items(self.composers)
        self.frame_attributes.comboBox_performer.add_items(self.performers)
        self.frame_attributes.comboBox_instrument.add_items(self.instruments)

app = QtGui.QApplication(sys.argv)
mainwindow_makam = MainWindowMakam()
mainwindow_makam.show()
app.exec_()
