from PyQt4 import QtGui

from .mainui_design import MainWindowDesign
from .utilities import utilities


class MainWindowMakamDesign(MainWindowDesign):
    def __init__(self):
        # setting the interface
        MainWindowDesign.__init__(self)

        self._set_main_label()
        self._set_score_tab()
        self._retranslate_ui_elements()

    def _set_main_label(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_main.setText("Turkish Makam Music Corpora")
        self.label_main.setFont(font)

    def _set_score_tab(self):
        self.tab_score = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_score, utilities._fromUtf8(""))

    def _retranslate_ui_elements(self):
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_score),
            utilities._translate("MainWindow", "Score Collection", None))

        self.frame_attributes.comboBox_melodic.set_placeholder_text('Makam')
        self.frame_attributes.comboBox_form.set_placeholder_text('Form')
        self.frame_attributes.comboBox_rhythm.set_placeholder_text('Usul')

# uncomment to test the interface
'''
app = QtGui.QApplication(sys.argv)
dialog = MainMakam()
dialog.show()
app.exec_()
'''