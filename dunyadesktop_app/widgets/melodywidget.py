from PyQt4 import QtGui
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg

import time


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

    def plot_melody(self, pitch_data, pd, len_raw_audio, samplerate):
        self.pitch_data = pitch_data
        self.pd = pd

        self.y_axis = pg.AxisItem('left')
        self.y_axis.enableAutoSIPrefix(enable=False)

        self.zoom_selection = self.layout.addPlot(title="Zoom selection",
                                              axisItems={'left': self.y_axis})
        self.zoom_selection.setMouseEnabled(x=False, y=False)
        self.zoom_selection.setMenuEnabled(False)

        time_stamps = []
        pitch = []
        salience = []
        for sample in self.pitch_data['pitch']:
            time_stamps.append(sample[0])
            pitch.append(sample[1])
            salience.append(sample[2])
        self.zoom_selection.plot(time_stamps, pitch, pen=None, symbol='o',
                                 symbolPen=None, symbolSize=2,
                                 symbolBrush=(30, 75, 130, 190))

        self.zoom_selection.setAutoVisible(y=True)
        self.zoom_selection.setLabel(axis="bottom", text="Time", units="sec")
        self.zoom_selection.setLabel(axis="left", text="Frequency", units="Hz",
                                     unitPrefix=False)

        self.zoom_selection.setDownsampling(ds=True, auto=True, mode='peak')

        self.addItem(self.zoom_selection)
        self.zoom_selection.setXRange(0, len_raw_audio / (samplerate * 30.),
                                      padding=0)
        self.zoom_selection.setYRange(0, max(pitch), padding=0)
        self.add_elements_to_plot()
        return time_stamps, pitch, salience

    def add_elements_to_plot(self):
        self.vline = pg.InfiniteLine(pos=0, movable=True,
                      pen=pg.mkPen((255, 40, 35, 150), width=2, cosmetic=True))
        self.zoom_selection.addItem(self.vline)

    def set_zoom_selection_area(self, pos_wf_x_min, pos_wf_x_max, samplerate):
        self.zoom_selection.setXRange(pos_wf_x_min / samplerate,
                                      pos_wf_x_max / samplerate, padding=0)

    def set_zoom_selection_area_hor(self, min_freq, max_freq):
        self.zoom_selection.setYRange(min_freq, max_freq, padding=0)
