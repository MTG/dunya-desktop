import sys
from PyQt4 import QtGui
from mainui_design import MainWindow
from utilities import utilities


class MainMakam(MainWindow):
    def __init__(self):
        # setting the interface
        MainWindow.__init__(self)

        self._set_score_tab()
        self._retranslate_ui_elements()

    def _set_score_tab(self):
        print "meh"
        self.tab_score = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_score, utilities._fromUtf8(""))

    def _retranslate_ui_elements(self):
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabWidget.tab_score),
            utilities._translate("MainWindow", "Score", None))


app = QtGui.QApplication(sys.argv)
dialog = MainMakam()
dialog.show()
app.exec_()
