from PyQt4 import QtGui, QtCore
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np


class MelodyWidget(GraphicsLayoutWidget):
    def __init__(self, parent=None):
        GraphicsLayoutWidget.__init__(self, parent)
        self.layout = pg.GraphicsLayout()
        self._set_size_policy()

    def _set_size_policy(self):
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                       QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def plot_melody(self, time_stamps, pitch_plot, len_raw_audio, samplerate,
                    max_pitch):
        x_axis = pg.AxisItem('bottom')
        x_axis.enableAutoSIPrefix(enable=False)

        y_axis = pg.AxisItem('left', )
        y_axis.enableAutoSIPrefix(enable=False)

        self.zoom_selection = self.layout.addPlot(title="Zoom selection",
                                                  axisItems={'left': y_axis,
                                                             'bottom': x_axis})
        self.zoom_selection.setMouseEnabled(x=False, y=False)
        self.zoom_selection.setMenuEnabled(False)
        self.zoom_selection.setDownsampling(auto=True, mode='mean')

        pen = pg.mkPen(cosmetic=True, width=1.5, color=(30, 110, 216,))
        self.curve = self.zoom_selection.plot(time_stamps, pitch_plot,
                                              connect='finite',
                                              pen=pen,
                                              clipToView=True,
                                              autoDownsample=True,
                                              downsampleMethod='subsample',
                                              antialias=False)
        self.zoom_selection.setLabel(axis="bottom", text="Time", units="sec")
        self.zoom_selection.setLabel(axis="left", text="Frequency", units="Hz",
                                     unitPrefix=False)

        self.zoom_selection.setXRange(0, len_raw_audio / samplerate * 25.,
                                      padding=0)
        self.zoom_selection.setYRange(20, max_pitch, padding=0)
        self.add_elements_to_plot(max_pitch)
        self.addItem(self.zoom_selection)

    def plot_histogram(self, vals, bins, max_pitch):
        self.histogram = self.layout.addPlot(row=0, col=1, title="Histogram")
        self.histogram.setMouseEnabled(x=False, y=False)
        self.histogram.setMenuEnabled(False)
        self.histogram.setMaximumWidth(200)
        self.histogram.setContentsMargins(0, 0, 0, 40)
        self.histogram.setAutoVisible(y=True)
        self.histogram.setDownsampling(auto=True, mode='subsample')

        self.histogram.hideAxis(axis="left")
        self.histogram.hideAxis(axis="bottom")

        shadow_pen = pg.mkPen((70, 70, 30), width=5, cosmetic=True)
        self.histogram.plot(x=vals, y=bins, downsampleMethod='subsample',
                            shadowPen=shadow_pen)

        self.histogram.setYRange(20, max_pitch, padding=0)
        self.histogram.setXRange(0, np.max(vals), padding=0)

        hline_pen = pg.mkPen((255, 40, 35, 150), cosmetic=True, width=1.5)
        self.histogram.setLabel(axis="right", text="Frequency (Hz)")
        self.hline_histogram = pg.ROI([0, 0], [0, np.max(bins)], angle=-90,
                                      pen=hline_pen)
        self.histogram.addItem(self.hline_histogram)
        self.addItem(self.histogram)

    def add_elements_to_plot(self, max_pitch):
        self.vline = pg.ROI([0, 0], [0, max_pitch], angle=0,
                            pen=pg.mkPen((255, 40, 35, 150), cosmetic=True,
                                         width=1))
        self.zoom_selection.addItem(self.vline)

    def set_zoom_selection_area(self, pos_wf_x_min, pos_wf_x_max, samplerate,
                                hopsize):
        x_min = pos_wf_x_min / samplerate
        x_max = pos_wf_x_max / samplerate
        self.zoom_selection.setXRange(x_min, x_max, padding=0)

    def set_zoom_selection_area_hor(self, min_freq, max_freq):
        self.zoom_selection.setYRange(min_freq, max_freq, padding=0)
        self.histogram.setYRange(min_freq, max_freq, padding=0)
