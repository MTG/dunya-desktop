from PyQt4 import QtGui
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg


class WaveformWidget(GraphicsLayoutWidget):
    def __init__(self):
        GraphicsLayoutWidget.__init__(self, parent=None)
        self._set_waveform()

        self.layout = pg.GraphicsLayout()
        self._set_layout()

        self.waveform = self.addPlot(title='Waveform')
        self.waveform.setDownsampling(auto=True)
        self.waveform.hideAxis(axis='bottom')
        self.waveform.hideAxis(axis='left')

        self.waveform.setMaximumHeight(100)
        self.waveform.setMouseEnabled(x=False, y=False)


    def _set_waveform(self):
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                        QtGui.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(100)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)

    def _set_layout(self):
        self.layout = pg.GraphicsLayout(border=(100, 100, 100))
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
