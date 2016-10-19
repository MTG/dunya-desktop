import time
import copy

from PyQt4 import QtGui, QtCore
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np


class MelodyWidget(GraphicsLayoutWidget):
    def __init__(self):
        self.start = time.time()

        GraphicsLayoutWidget.__init__(self, parent=None)
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

    def plot_melody(self, pitch_data, len_raw_audio, samplerate):
        self.pitch_data = pitch_data
        pitch = np.array(pitch_data['pitch'])

        y_axis = pg.AxisItem('left')
        y_axis.enableAutoSIPrefix(enable=False)

        self.zoom_selection = self.layout.addPlot(title="Zoom selection",
                                                  axisItems={'left': y_axis})
        self.zoom_selection.setMouseEnabled(x=False, y=False)
        self.zoom_selection.setMenuEnabled(False)

        time_stamps = pitch[:, 0]
        pitch_curve = pitch[:, 1]
        pitch_plot = copy.copy(pitch_curve)
        pitch_plot[pitch_plot < 20] = np.nan
        salience = pitch[:, 2]

        self.curve = self.zoom_selection.plot(time_stamps, pitch_plot,
                                              pen=None,
                                              #connect='finite',
                                              #pen=pg.mkPen(
                                              #    color=(217, 217, 226, 180),
                                              #    width=1.5),
                                              #shadowPen=pg.mkPen((70, 70, 30),
                                              #                   width=7,
                                              #                   cosmetic=True),
                                              symbol='o',
                                              symbolSize=1.5,
                                              symbolBrush=pg.mkBrush(222, 244, 237),
                                              symbolPen=None,
                                              )
        self.zoom_selection.setAutoVisible(y=True)
        self.zoom_selection.setLabel(axis="bottom", text="Time", units="sec")
        self.zoom_selection.setLabel(axis="left", text="Frequency", units="Hz",
                                     unitPrefix=False)

        #salience_plot = []
        # salience normalization
        #salience_factor = max(pitch) / max(salience)
        #[salience_plot.append(i * salience_factor) for i in salience]

        # salience plot
        #self.zoom_selection.plot(time_stamps, salience_plot, pen=None,
        #                        symbol='t', symbolPen=None,
        #                        downsampleMethod='subsample',
        #                        symbolSize=4, symbolBrush=(20, 170, 100, 18),
        #                        fillLevel=0, fillBrush=(100, 100, 255, 20))

        self.addItem(self.zoom_selection)
        self.add_elements_to_plot(pitch_curve)

        self.zoom_selection.setXRange(0, len_raw_audio / (samplerate * 20.))
        self.zoom_selection.setYRange(20, max(pitch_curve), update=False)

        timer = QtCore.QTimer()
        timer.singleShot(1,
                         lambda: self.zoom_selection.setDownsampling(
                             ds=True, auto=True, mode='mean'))
        return pitch_curve

    def plot_histogram(self, pd, pitch):
        self.histogram = self.layout.addPlot(row=0, col=1, title="Histogram")
        self.histogram.setMouseEnabled(x=False, y=False)
        self.histogram.setMenuEnabled(False)
        self.histogram.setMaximumWidth(150)
        self.histogram.setContentsMargins(0, 0, 0, 40)
        self.histogram.setAutoVisible(y=True)

        self.histogram.hideAxis(axis="left")
        self.histogram.hideAxis(axis="bottom")

        y = np.array(pd['bins'])
        y[y == 0] = np.nan

        self.histogram.plot(x=pd["vals"],
                            y=pd["bins"],
                            shadowPen=pg.mkPen((70, 70, 30),
                                               width=5,
                                               cosmetic=True)
                            #pen=pg.mkPen((240, 205, 0, 100),
                            #             width=1))
                            )
        #self.histogram.setShadowPen(pg.mkPen((70, 70, 30),
        #                                     width=6, cosmetic=True))

        self.histogram.setYRange(0, max(pitch), padding=0)
        self.histogram.setXRange(0, max(pd["vals"]), padding=0)

        self.histogram.setLabel(axis="right", text="Frequency (Hz)")
        self.hline_histogram = pg.ROI([0, 0], [0, max(pd['bins'])],
                                      angle=-90,
                                      pen=pg.mkPen((255, 40, 35, 150),
                                                   # cosmetic=True,
                                                   width=1))
        self.histogram.addItem(self.hline_histogram)

        self.histogram.setDownsampling(ds=True, auto=True, mode='mean')
        self.addItem(self.histogram)

    def add_elements_to_plot(self, pitch):
        self.curve_point = pg.CurvePoint(self.curve)
        self.zoom_selection.addItem(self.curve_point)

        #self.arrow = pg.ArrowItem(angle=90)
        #self.arrow.setParentItem(self.curve_point)
        #self.zoom_selection.addItem(self.arrow)

        self.vline = pg.ROI([0, 0], [0, max(pitch)], angle=0,
                            pen=pg.mkPen((255, 40, 35, 150), # cosmetic=True,
                                         width=1))
        self.zoom_selection.addItem(self.vline)

    def set_zoom_selection_area(self, pos_wf_x_min, pos_wf_x_max, samplerate):
        x_min = pos_wf_x_min / samplerate
        x_max = pos_wf_x_max / samplerate
        self.zoom_selection.setXRange(x_min, x_max, padding=0)

        #self.zoom_selection.setDownsampling(ds=True, auto=True, mode='mean')
        #if len(self.pitch_data['pitch'][
        #       int(pos_wf_x_min / 128.):int(pos_wf_x_max / 128.)]) >= 10000:
        #    self.zoom_selection.setDownsampling(ds=True, auto=True,
        #                                        mode='peak')

    def set_zoom_selection_area_hor(self, min_freq, max_freq):
        self.zoom_selection.setYRange(min_freq, max_freq, padding=0)
        self.histogram.setYRange(min_freq, max_freq, padding=0)
