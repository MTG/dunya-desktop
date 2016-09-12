import sys
from cultures import token

from PyQt4 import QtGui, QtCore
from mainui_design_makam import MainWindowMakamDesign

token.set_token()

# gazel and taksim uuids
GAZEL = u'a1d59289-ea72-4050-9253-01ca12bb5556'
TAKSIM = u'b4658cef-f3cd-4ced-a534-1dd0a0d5b2de'


class MainWindowMakam(MainWindowMakamDesign):
    def __init__(self):
        MainWindowMakamDesign.__init__(self)


app = QtGui.QApplication(sys.argv)
mainwindow_makam = MainWindowMakam()
mainwindow_makam.show()
app.exec_()
