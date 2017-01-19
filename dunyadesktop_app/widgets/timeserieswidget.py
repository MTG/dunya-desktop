from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np

from PyQt5.QtWidgets import QSizePolicy

pg.setConfigOptions(useOpenGL=True)
pg.setConfigOptions(useWeave=True)


class TonicLine(pg.InfiniteLine):
    movable = False
    angle = 0
    label_opts = {'position': 0.1, 'color': (200, 200, 100),
                 'fill': (200, 200, 200, 50), 'movable': True}

    def __init__(self, value, label):
        pg.InfiniteLine.__init__(self, pos=value, angle=self.angle,
                                 movable=self.movable,
                                 labelOpts=self.label_opts)


class TimeSeriesWidget(GraphicsLayoutWidget):
    def __init__(self, parent=None):
        GraphicsLayoutWidget.__init__(self, parent)
        self.layout = pg.GraphicsLayout()
        self._set_size_policy()
        self.limit = 600

        # flags
        self.is_pitch_plotted = False

    def _set_size_policy(self):
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def add_1d_view(self):
        x_axis = pg.AxisItem('bottom')
        x_axis.enableAutoSIPrefix(enable=False)
        x_axis.setGrid(100)

        y_axis = pg.AxisItem('left')
        y_axis.enableAutoSIPrefix(enable=False)

        self.zoom_selection = self.layout.addPlot(title="Zoom selection",
                                                  axisItems={'left': y_axis,
                                                             'bottom': x_axis})
        self.zoom_selection.setMouseEnabled(x=False, y=False)
        self.zoom_selection.setMenuEnabled(False)
        self.zoom_selection.setDownsampling(auto=True, mode='mean')

        self.layout.addItem(self.zoom_selection)
        self.vline = pg.ROI([0, 0], [0, 20000], angle=0,
                            pen=pg.mkPen((255, 40, 35, 150), cosmetic=True,
                                         width=1))
        self.zoom_selection.addItem(self.vline)
        self.addItem(self.layout)
        self.plot_1d_region()

    def plot_pitch(self, time_stamps, pitch_plot, x_start, x_end, max_pitch):
        self.pitch_plot = pitch_plot
        pen = pg.mkPen(cosmetic=True, width=1.5, color=(30, 110, 216,))
        self.update_plot(x_start, x_end)
        self.is_pitch_plotted = True

    def plot_histogram(self, vals, bins):
        shadow_pen = pg.mkPen((70, 70, 30), width=5, cosmetic=True)
        self.histogram.plot(x=vals, y=bins, shadowPen=shadow_pen)
        self.histogram.setXRange(0, np.max(vals), padding=0)
        self.histogram.resetTransform()

    def plot_1d_region(self):
        self.histogram = self.layout.addPlot(row=0, col=1)
        self.histogram.setMouseEnabled(x=False, y=False)
        self.histogram.setMenuEnabled(False)
        self.histogram.setMaximumWidth(125)
        self.histogram.setContentsMargins(0, 0, 0, 40)
        self.histogram.setAutoVisible(y=True)
        self.histogram.hideAxis(axis="left")
        self.histogram.hideAxis(axis="bottom")
        self.histogram.setYRange(0, 20000, padding=0)
        self.histogram.setLabel(axis="right", text="Frequency (Hz)")

        hline_pen = pg.mkPen((255, 40, 35, 150), cosmetic=True, width=1.5)
        self.hline_histogram = pg.ROI([0, 0], [0, 1], angle=-90,
                                      pen=hline_pen)
        self.histogram.addItem(self.hline_histogram)

        self.region_1d = pg.LinearRegionItem(values=[0, 20000],
                                             brush=pg.mkBrush((50, 255,
                                                               255, 45)),
                                             orientation=pg.LinearRegionItem.Horizontal,
                                             bounds=[0, 20000])
        self.histogram.addItem(self.region_1d)
        self.region_1d.sigRegionChangeFinished.connect(self.change_y_axis)
        self.addItem(self.histogram)

    def change_y_axis(self):
        pos_y_min, pos_y_max = self.region_1d.getRegion()
        self.zoom_selection.setYRange(pos_y_min, pos_y_max)
        self.histogram.setYRange(pos_y_min, pos_y_max)

    def set_zoom_selection_area_hor(self, min_freq, max_freq):
        self.zoom_selection.setYRange(min_freq, max_freq, padding=0)
        self.histogram.setYRange(min_freq, max_freq, padding=0)

    def add_tonic(self, value):
        if not hasattr(self, 'tonic_line'):
            self.tonic_line = pg.InfiniteLine(pos= value, movable=False,
                                              angle=0, label='Tonic',
                                              labelOpts=
                                              {'position': 0.1,
                                               'color': (200, 200, 100),
                                               'fill': (200, 200, 200, 50),
                                               'movable': True})
            self.zoom_selection.addItem(self.tonic_line)

    def update_plot(self, start, stop):
        start *=  1/(128./44100.)
        stop *= 1/(128./44100.)
        start = int(start)
        stop = int(stop)
        # Decide by how much we should downsample
        ds = int((stop - start) / self.limit) + 1

        if ds == 1:
            # Small enough to display with no intervention.
            visible = self.pitch_plot[start:stop]
            scale = 1
        else:
            # Here convert data into a down-sampled array suitable for visualizing.
            # Must do this piecewise to limit memory usage.
            samples = 1 + ((stop - start) // ds)
            visible = np.zeros(samples * 2, dtype=self.pitch_plot.dtype)
            sourcePtr = start
            targetPtr = 0

            # read data in chunks of ~1M samples
            chunkSize = (1000000 // ds) * ds
            while sourcePtr < stop - 1:
                chunk = self.pitch_plot[sourcePtr:min(stop, sourcePtr + chunkSize)]
                sourcePtr += len(chunk)

                # reshape chunk to be integral multiple of ds
                chunk = chunk[:(len(chunk) // ds) * ds].reshape(
                    len(chunk) // ds, ds)

                # compute max and min
                chunkMax = chunk.max(axis=1)
                chunkMin = chunk.min(axis=1)

                # interleave min and max into plot data to preserve envelope shape
                visible[targetPtr:targetPtr + chunk.shape[0] * 2:2] = chunkMin
                visible[
                1 + targetPtr:1 + targetPtr + chunk.shape[0] * 2:2] = chunkMax
                targetPtr += chunk.shape[0] * 2

            self.visible = visible[:targetPtr]
            scale = ds * 0.5

        start = (start*128.)/44100
        stop = (stop*128.)/44100
        step = (stop - start) / (len(visible))

        time = np.arange(start, stop, step)

        self.zoom_selection.clearPlots()
        pen = pg.mkPen(cosmetic=True, width=1.5, color=(30, 110, 216,))
        self.zoom_selection.plot(time[0:len(visible)],
                                 visible,
                                 connect='finite',
                                 pen=pen)
        self.zoom_selection.resetTransform()

    def set_hline_pos(self, playback_pos):
        self.hline_histogram.setPos(pos=[0,self.pitch_plot[
            int(playback_pos*self.samplerate/self.hopsize)]])
