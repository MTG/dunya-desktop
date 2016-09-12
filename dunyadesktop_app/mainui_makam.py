import sys
from cultures import token
from cultures import makam

from PyQt4 import QtGui, QtCore
from mainui_design_makam import MainWindowMakamDesign

token.set_token()


class MainWindowMakam(MainWindowMakamDesign):
    def __init__(self):
        MainWindowMakamDesign.__init__(self)


app = QtGui.QApplication(sys.argv)
mainwindow_makam = MainWindowMakam()
mainwindow_makam.show()
app.exec_()
