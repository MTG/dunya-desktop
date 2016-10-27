from PyQt4 import QtGui

#from mainui_design import MainWindowDesign
from general_design import GeneralMainDesign


class MainWindowMakamDesign(GeneralMainDesign):
    def __init__(self):
        # setting the interface
        GeneralMainDesign.__init__(self)

        self._set_main_label()
        self._set_score_tab()
        self._retranslate_ui_elements()

    def _set_main_label(self):
        self.dwc_top.label_corpus.setText('<html><head/><body><p align="center"><span style=" font-size:15pt; color:#C1C1C1;">Ottoman-Turkish Makam Music Corpus</span></p></body></html>')

    def _set_score_tab(self):
        self.tab_score = QtGui.QWidget()
        self.frame_query.tabWidget.addTab(self.tab_score, "")

    def _retranslate_ui_elements(self):
        self.frame_query.tabWidget.setTabText(
            self.frame_query.tabWidget.indexOf(self.tab_score),
            "Score Collection")

        self.frame_query.frame_attributes.comboBox_melodic.set_placeholder_text('Makam')
        self.frame_query.frame_attributes.comboBox_form.set_placeholder_text('Form')
        self.frame_query.frame_attributes.comboBox_rhythm.set_placeholder_text('Usul')

# uncomment to test the interface
import sys
app = QtGui.QApplication(sys.argv)
dialog = MainWindowMakamDesign()
dialog.show()
app.exec_()
