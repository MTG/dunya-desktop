import numpy

from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtCore import QSize
import pyqtgraph as pg

CURSOR_PEN = pg.mkPen((255, 40, 35, 150), cosmetic=True, width=3)


class NoteModelAxis(pg.AxisItem):
    def __init__(self, note_models, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        super(pg.AxisItem, self).tickStrings(values, scale, spacing)


class HistogramDialog(QDialog):
    def __init__(self):
        super(HistogramDialog, self).__init__()
        self.setMinimumSize(QSize(500, 325))
        self.setContentsMargins(0, 0, 0, 0)

        self.hist_widget = pg.PlotWidget(self)
        l = QVBoxLayout(self)
        l.addWidget(self.hist_widget)
        l.setContentsMargins(0, 0, 0, 0)

    def plot_histogram(self, bins, vals):
        axis = NoteModelAxis('bottom')
        self.hist_widget.plot(bins, vals, fillLevel=0, brush=(0,0,255,150),
                              axisItems = {'bottom':axis})
        self.max_val = numpy.max(vals)
        self.__set_plot()

    def __set_plot(self):
        self.hist_widget.setMouseEnabled(x=False, y=False)
        self.hist_widget.setMenuEnabled(False)

        self.hline_histogram = pg.ROI(pos=[0, 0], size=[0, self.max_val], angle=0,
                                      pen=CURSOR_PEN)
        self.hist_widget.addItem(self.hline_histogram)

    def update_histogram(self, pitch):
        self.hline_histogram.setPos(pitch, 0)
