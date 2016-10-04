from PyQt4 import QtGui, QtCore
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg


class MelodyWidget(GraphicsLayoutWidget):
    def __init__(self):
        GraphicsLayoutWidget.__init__(self, parent=None)

    def set_size_policy(self):
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                       QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
