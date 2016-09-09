from PyQt4 import QtGui


class ProgressBar(QtGui.QProgressBar):
    def __init__(self, parent=None):
        QtGui.QProgressBar.__init__(self, parent)
        self.setGeometry(30, 40, 200, 25)