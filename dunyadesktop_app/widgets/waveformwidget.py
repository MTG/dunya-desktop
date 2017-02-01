from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np

from .widgetutilities import downsample_plot

pg.setConfigOptions(useOpenGL=True)
pg.setConfigOptions(useWeave=True)
# pg.setConfigOptions(crashWarning=True)

WAVEFORM_PEN = (20, 170, 100, 80)
WAVEFORM_BRUSH = pg.mkBrush((50, 255, 255, 45))
WAVEFORM_VLINE = pg.mkPen((255, 40, 35, 150), cosmetic=True, width=2)


class WaveformRegionItem(pg.LinearRegionItem):
    clicked = pyqtSignal()

    def __init__(self, values=[0, 1], orientation=None, brush=None,
                 movable=True, bounds=None):
        pg.LinearRegionItem.__init__(self, values=values, brush=brush,
                                     orientation=orientation, movable=movable,
                                     bounds=bounds)

    def mouseClickEvent(self, ev):
        self.clicked.emit()
        super(WaveformRegionItem, self).mouseClickEvent(ev)

    def mouseDragEvent(self, ev):
        self.clicked.emit()
        super(WaveformRegionItem, self).mouseDragEvent(ev)


class WaveformWidget(GraphicsLayoutWidget):
    def __init__(self):
        GraphicsLayoutWidget.__init__(self, parent=None)

        self._set_size_policy()
        self.limit = 900  # maximum number of samples to be plotted
        self.samplerate = 44100.

    def _set_size_policy(self):
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(50)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        # self.setMinimumSize(QSize(0, 100))
        # self.setMaximumSize(QSize(16777215, 50))
        self.setFocusPolicy(Qt.NoFocus)
        self.setAcceptDrops(False)
        self.centralWidget.setContentsMargins(0, 0, 0, 0)
        self.centralWidget.setSpacing(0)

    def plot_waveform(self, raw_audio):
        self.waveform = self.centralWidget.addPlot()
        self.waveform.hideAxis(axis='bottom')
        self.waveform.hideAxis(axis='left')

        # disabling the mouse events and menu events
        self.waveform.setMouseEnabled(x=False, y=False)
        self.waveform.setMenuEnabled(False)

        # downsampling the given plot array
        self.visible = downsample_plot(raw_audio, self.limit)
        self.ratio = len(raw_audio) / float(len(self.visible))
        self.waveform.clearPlots()
        self.waveform.plot(self.visible, connect='finite', pen=WAVEFORM_PEN)
        self.waveform.resetTransform()
        self._add_elements_to_plot(len(self.visible), np.min(self.visible),
                                   np.max(self.visible))

    def _add_elements_to_plot(self, len_plot, min_audio, max_audio):
        pos_wf_x_max = len_plot / 25.
        self.region_wf = WaveformRegionItem([0, pos_wf_x_max],
                                            brush=WAVEFORM_BRUSH,
                                            bounds=[0., len_plot])

        self.vline_wf = pg.ROI([0, min_audio], [0, max_audio - min_audio],
                               angle=0, pen=WAVEFORM_VLINE)
        self.waveform.addItem(self.region_wf)
        self.waveform.addItem(self.vline_wf)

    def get_waveform_region(self):
        pos_wf_x_min, pos_wf_x_max = self.region_wf.getRegion()
        x_min = (pos_wf_x_min * self.ratio) / self.samplerate
        x_max = (pos_wf_x_max * self.ratio) / self.samplerate
        return x_min, x_max

    def change_wf_region(self, x_start, x_end):
        x_start = (x_start * self.samplerate) / self.ratio
        x_end = (x_end * self.samplerate) / self.ratio
        self.region_wf.setRegion([x_start, x_end])
