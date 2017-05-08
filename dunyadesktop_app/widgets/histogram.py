from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtCore import QSize
import pyqtgraph as pg


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
        self.hist_widget.plot(bins, vals, fillLevel=0, brush=(0,0,255,150))
        self.__set_plot()

    def __set_plot(self):
        self.hist_widget.setMouseEnabled(x=False, y=False)
        self.hist_widget.setMenuEnabled(False)
