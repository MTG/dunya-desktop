from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np

from .widgetutilities import downsample_plot

# Enable OpenGL and Weave to improve the performance of plotting functions.
pg.setConfigOptions(useOpenGL=True)
pg.setConfigOptions(useWeave=True)
pg.setConfigOptions(leftButtonPan=False)
# pg.setConfigOptions(crashWarning=True)


# Colors of the waveform plot, vertical line (cursor) and waveform region
# selector
WAVEFORM_PEN = (20, 170, 100, 80)  # (Red, Green, Blue, a)
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

        self.__set_size_policy()
        self.limit = 900  # maximum number of samples to be plotted
        self.samplerate = 44100.

    def __set_size_policy(self):
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setFocusPolicy(Qt.NoFocus)
        self.setAcceptDrops(False)
        self.centralWidget.setContentsMargins(0, 0, 0, 0)
        self.centralWidget.setSpacing(0)

    def plot_waveform(self, raw_audio):
        """
        Plots the given raw audio.
        :param raw_audio: List of floats.
        """
        self.waveform = self.centralWidget.addPlot()
        self.waveform.hideAxis(axis='bottom')
        self.waveform.hideAxis(axis='left')

        # disabling the mouse events and menu events
        self.waveform.setMouseEnabled(x=False, y=False)
        self.waveform.setMenuEnabled(False)

        # downsampling the given plot array
        self.visible = downsample_plot(raw_audio, self.limit)

        # ratio is used
        self.ratio = len(raw_audio) / float(len(self.visible))
        self.waveform.clearPlots()
        self.waveform.plot(self.visible, connect='finite', pen=WAVEFORM_PEN)
        self.waveform.resetTransform()
        self.__add_items_to_plot(len(self.visible), np.nanmin(self.visible),
                                 np.nanmax(self.visible))

    def __add_items_to_plot(self, len_plot, min_audio, max_audio):
        """
        Adds a region selector item and vertical line for to the waveform plot.
        :param len_plot: (int) Number of samples in plotted waveform array.
        :param min_audio: (float) The minimum value of plotted waveform array.
        :param max_audio: (float) The maximum value of plotted waveform array.
        """

        # Create a waveform region item and add it to waveform plot
        pos_wf_x_max = len_plot * 0.05  # Region item focuses on the 10% of
        # waveform plot.
        self.region_wf = WaveformRegionItem(values=[0, pos_wf_x_max],
                                            brush=WAVEFORM_BRUSH,
                                            bounds=[0., len_plot])

        # Creating a cursor with pyqtgraph.ROI.
        self.vline_wf = pg.ROI(pos=[0, min_audio],
                               size=[0, max_audio - min_audio],
                               angle=0, pen=WAVEFORM_VLINE)
        self.waveform.addItem(self.region_wf)
        self.waveform.addItem(self.vline_wf)

    @property
    def get_waveform_region(self):
        """
        Returns the current position of the waveform region item in seconds if
        the waveform region item exists.

        :return:
        """
        if hasattr(self, 'region_wf'):
            pos_wf_x_min, pos_wf_x_max = self.region_wf.getRegion()
            x_min = (pos_wf_x_min * self.ratio) / self.samplerate
            x_max = (pos_wf_x_max * self.ratio) / self.samplerate
            return x_min, x_max
        else:
            return None, None

    def change_wf_region(self, x_start, x_end):
        """
        Sets the position of the waveform region item on the waveform widget.

        :param x_start: Start point of the region item in seconds.
        :param x_end: End point of the region item in seconds.
        """
        x_start = (x_start * self.samplerate) / self.ratio
        x_end = (x_end * self.samplerate) / self.ratio
        self.region_wf.setRegion([x_start, x_end])
