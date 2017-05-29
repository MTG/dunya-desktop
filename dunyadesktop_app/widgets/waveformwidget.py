from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCursor
import pyqtgraph as pg
import numpy as np

from .widgetutilities import downsample_plot

# Enable OpenGL and Weave to improve the performance of plotting functions.
pg.setConfigOptions(useOpenGL=True)
pg.setConfigOptions(useWeave=True)
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
        # Override the mouseClickEvent. Add self.clicked signal before the
        # original method. Original method is called with super() method.
        self.clicked.emit()  # emit clicked signal
        super(WaveformRegionItem, self).mouseClickEvent(ev)  # call original
        # method

    def mouseDragEvent(self, ev):
        # Override the mouseDragEvent. Add self.clicked signal before the
        # original method. Original method is called with super() method.
        self.clicked.emit()  # emit clicked signal
        super(WaveformRegionItem, self).mouseDragEvent(ev)  # call original
        # method


class SectionItem(pg.LinearRegionItem):
    hovering = pyqtSignal(str)
    item_initialized = pyqtSignal(object)

    def __init__(self, values, label_section, color):
        pg.LinearRegionItem.__init__(self, values=values, movable=False)

        for line in self.lines:
            line.setPen(pg.mkPen(None))
        self.setBrush(pg.mkBrush(color))
        self.label = label_section

        # signals
        self.item_initialized.emit(self)

    def hoverEvent(self, ev):
        if not ev.isExit():
            self.hovering.emit(self.label)
        else:
            self.hovering.emit('')


class WaveformWidget(pg.GraphicsLayoutWidget):
    def __init__(self):
        pg.GraphicsLayoutWidget.__init__(self, parent=None)

        # Set 0 margin 0 spacing to cover the whole area.
        self.centralWidget.setContentsMargins(0, 0, 0, 0)
        self.centralWidget.setSpacing(0)

        self.section_items = []

        self.limit = 900  # maximum number of samples to be plotted
        self.samplerate = 44100.


    def plot_waveform(self, raw_audio):
        """
        Plots the given raw audio.
        :param raw_audio: (list of numpy array) List of floats.
        """

        if not hasattr(self, 'waveform'):
            # add a new plot
            self.waveform = self.centralWidget.addPlot()

            # hide x and y axis
            self.waveform.hideAxis(axis='bottom')
            self.waveform.hideAxis(axis='left')

            # disable the mouse events and menu events
            self.waveform.setMouseEnabled(x=False, y=False)
            self.waveform.setMenuEnabled(False)
        self.waveform.clear()
        # downsampling the given plot array
        self.visible = downsample_plot(raw_audio, self.limit)

        # ratio is used in self.change_wf_region and self.get_waveform_region
        # methods.
        self.len = np.size(self.visible)
        self.min = np.nanmin(self.visible)
        self.max = np.nanmax(self.visible)

        self.ratio = np.size(raw_audio) / self.len
        self.waveform.plot(self.visible, connect='finite', pen=WAVEFORM_PEN)

        # add waveform region item and playback cursor
        self.__add_items_to_plot(self.len, self.min, self.max)

    def __add_items_to_plot(self, len_plot, min_audio, max_audio):
        """
        Adds a region selector item and vertical line for to the waveform plot.
        :param len_plot: (int) Number of samples in plotted waveform array.
        :param min_audio: (float) The minimum value of plotted waveform array.
        :param max_audio: (float) The maximum value of plotted waveform array.
        """

        # Create a waveform region item and add it to waveform plot
        pos_wf_x_max = len_plot * 0.05  # Region item focuses on the 5% of
        # waveform plot.

        self.region_wf = WaveformRegionItem(values=[0, pos_wf_x_max],
                                            brush=WAVEFORM_BRUSH,
                                            bounds=[0., len_plot])
        self.waveform.addItem(self.region_wf)

        # Creating a cursor with pyqtgraph.ROI
        self.vline_wf = pg.ROI(pos=[0, min_audio],
                               size=[0, max_audio - min_audio],
                               angle=0, pen=WAVEFORM_VLINE)
        self.waveform.addItem(self.vline_wf)

        # text item
        self.section_label = pg.TextItem(text='')
        self.waveform.addItem(self.section_label)

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

    def update_wf_vline(self, playback_pos_sample):
        """
        Updated the position of vertical line.
        :param playback_pos_sample: (int) Position of playback in samples.
        """
        pos = playback_pos_sample/self.ratio
        if pos <= 0:
            pos = 0
        elif pos >= self.len:
            pos = self.len

        self.vline_wf.setPos([pos, self.min])

    def wheelEvent(self, event):
        delta = event.pixelDelta().y()
        xmin, xmax = self.get_waveform_region
        distance = (xmax - xmin) * 0.03
        if delta>0:
            xmin += distance
            xmax -= distance

        elif delta<0:
            xmin -= distance
            xmax += distance

        self.change_wf_region(xmin, xmax)

    def add_section(self, time, label, title, color):
        time *= (self.samplerate/ self.ratio)
        label += "\n" + title
        section_item = SectionItem(values=time, label_section=label,
                                   color=color)
        self.section_items.append(section_item)
        self.waveform.addItem(section_item)
        section_item.hovering.connect(self.__hover_section)

    def __hover_section(self, text):
        self.section_label.setText(text)
        org_pos = self.mapFromGlobal(QCursor.pos())
        pos_x = self.len * (float(org_pos.x())/self.waveform.width())
        self.section_label.setPos(pos_x, self.max*2./3)

    def remove_sections(self):
        for item in self.section_items:
            self.waveform.removeItem(item)
        self.section_items = []