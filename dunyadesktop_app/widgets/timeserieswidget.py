import pyqtgraph as pg
import numpy as np

from PyQt5.QtCore import pyqtSignal

from .widgetutilities import downsample_plot

# Enable OpenGL and Weave to improve the performance of plotting functions.
pg.setConfigOptions(useOpenGL=True)
pg.setConfigOptions(useWeave=True)
# pg.setConfigOptions(crashWarning=True)

CURSOR_PEN = pg.mkPen((255, 40, 35, 150), cosmetic=True, width=3)
YAXIS_BRUSH = pg.mkBrush((50, 255, 255, 45))
PITCH_PEN = pg.mkPen(cosmetic=True, width=1.5, color=(30, 110, 216,))
SHADOW_PEN = pg.mkPen((70, 70, 30), width=5, cosmetic=True)


class TimeSeriesWidget(pg.GraphicsLayoutWidget):
    sample_rate = 44100
    wheel_event = pyqtSignal(object)

    def __init__(self, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)

        # Set 0 margin 0 spacing to cover the whole area.
        self.centralWidget.setContentsMargins(0, 0, 0, 0)
        self.centralWidget.setSpacing(0)

        self.limit = 600  # maximum number of samples to be plotted
        self.rois = []

        # flags
        self.is_pitch_plotted = False
        self.is_notes_added = False

    def wheelEvent(self, ev):
        self.wheel_event.emit(ev)

    def add_1d_view(self):
        """
        Adds a 1d view to TimeSeriesWidget where you can plot and add items
        on it.
        """

        # To customize the plot axises, create new ones.
        x_axis = pg.AxisItem('bottom')  # x-axis
        x_axis.enableAutoSIPrefix(enable=False)  # Prevent automatic SI
        # prefix scaling on this axis.
        x_axis.setGrid(100)  # the alpha value of grids on x-axis

        y_axis = pg.AxisItem('left')  # x-axis
        y_axis.enableAutoSIPrefix(enable=False)  # Prevent automatic SI
        # prefix scaling on this axis.
        axis_items = {'left': y_axis, 'bottom': x_axis}

        # add plot
        self.zoom_selection = self.centralWidget.addPlot(axisItems=axis_items)

        # disable the mouse events and menu events
        self.zoom_selection.setMouseEnabled(x=False, y=False)
        self.zoom_selection.setMenuEnabled(False)

        # initialize a cursor object. Height of cursor is 20000.
        self.vline = pg.ROI(pos=[0, 0], size=[0, 20000], angle=0,
                            pen=CURSOR_PEN)
        self.zoom_selection.addItem(self.vline)  # add item to plot area

        # add y-axis region
        self.right_axis = self.centralWidget.addPlot(row=0, col=1)

        # disable the mouse events and menu events
        self.right_axis.setMouseEnabled(x=False, y=False)
        self.right_axis.setMenuEnabled(False)

        self.right_axis.setMaximumWidth(125)  # maximum width 125
        self.right_axis.setContentsMargins(0, 0, 0, 40)  # set 40 left margin

        self.right_axis.hideAxis(axis="left")  # hide left-axis
        self.right_axis.hideAxis(axis="bottom")  # hide botton-axis
        self.right_axis.setYRange(0, 20000, padding=0)
        # show right axis
        self.right_axis.setLabel(axis="right", text="Frequency (Hz)")

        # initialize a linear region item
        orientation = pg.LinearRegionItem.Horizontal  # set the item horizontal
        self.region_yaxis = pg.LinearRegionItem(values=[0, 20000],
                                                brush=YAXIS_BRUSH,
                                                orientation=orientation,
                                                bounds=[0, 20000])
        self.right_axis.addItem(self.region_yaxis)  # add item to right axis

        # set region changed signal to set y axis range in the plot
        self.region_yaxis.sigRegionChangeFinished.connect(
            self.change_yaxis_range)

    def plot_pitch(self, pitch_plot, x_start, x_end, hop_size):
        """
        Plots the given pitch_plot array.
        :param pitch_plot: (numpy array or list) List of pitch values.
        Ex: [234.5, 234,3, 234.0, ...]
        :param x_start: (int or float) Time stamp of starting point in
        seconds.
        :param x_end: (int or float) Time stamp of ending point in seconds.
        :param hop_size: (int) Hop size in samples. Ex: 128
        """
        if not self.is_pitch_plotted:  # if pitch is not plotted yet
            self.ratio = 1. / (hop_size / np.float(self.sample_rate))
            self.pitch_plot = pitch_plot

            # downsample the plot in given time stamps
            self.update_plot(start=x_start, stop=x_end, hop_size=hop_size)
            # set the flag as true after plot the pitch
            self.is_pitch_plotted = True
        else:
            # downsample the plot in given time stamps
            self.update_plot(start=x_start, stop=x_end, hop_size=hop_size)

    def update_plot(self, start, stop, hop_size):
        """
        Updates the view of the plot region with given time stamps.
        :param start: (int or float) Time stamp of starting point in seconds.
        :param stop: (int or float) Time stamp of ending point in seconds.
        :param hop_size: (int) Hop size in samples. Ex: 128
        """

        # convert the given time stamps into samples to specify the plot array
        start = int(start * self.ratio)
        stop = int(stop * self.ratio)
        plot_y = downsample_plot(self.pitch_plot[start:stop], self.limit)

        # create time stamps array for x-axis
        start = (np.float(start) * hop_size) / self.sample_rate
        stop = (np.float(stop) * hop_size) / self.sample_rate
        step = (stop - start) / (np.size(plot_y))
        plot_x = np.arange(start=start, stop=stop, step=step)
        # Sometimes the dimensions of plot_x and plot_y are not same. To fix
        # this situation, take plot_x with the same dimension of plot_y
        plot_x = plot_x[0:np.size(plot_y)]

        self.zoom_selection.clearPlots()  # clears the current plots
        self.zoom_selection.plot(x=plot_x[0:np.size(plot_y)], y=plot_y,
                                 connect='finite', pen=PITCH_PEN)

    def plot_histogram_raxis(self, vals, bins):
        """
        Plots histogram to the right axis.
        :param vals: (list or numpy array) List of valley values of histogram.
        :param bins: (list or numpy array) List of bins values of histogram
        in Hz
        """

        # shadow pen is the properties of shadow around the lines
        self.right_axis.plot(x=vals, y=bins, shadowPen=SHADOW_PEN)
        self.right_axis.setXRange(0, np.max(vals), padding=0)

        # cursor in the histogram plot.
        self.hline_histogram = pg.ROI(pos=[0, 0], size=[0, 1], angle=-90,
                                      pen=CURSOR_PEN)
        self.right_axis.addItem(self.hline_histogram)

        # Link the y-axises of pitch and histogram plots
        self.zoom_selection.setYLink(self.right_axis)

    def change_yaxis_range(self):
        """
        Changes the y-axis range according to the selected region in y-axis.
        """
        pos_y_min, pos_y_max = self.region_yaxis.getRegion()
        self.zoom_selection.setYRange(pos_y_min, pos_y_max)
        self.right_axis.setYRange(pos_y_min, pos_y_max)

    def add_tonic(self, values):
        """
        Adds tonic lines on the pitch plot.
        :param values: (list or numpy array) A sequence of tonic values in Hz.
        """
        # label options for the tonic values on the tonic line
        label_opts = {'position': 0.1, 'color': (200, 200, 100),
                      'fill': (200, 200, 200, 50), 'movable': True}

        if not hasattr(self, 'tonic_lines'):
            self.tonic_lines = []

        for value in values:
            # create infinite line
            t_line = pg.InfiniteLine(pos=value, movable=False, angle=0,
                                     label='Tonic=%.2f' % value,
                                     labelOpts=label_opts)
            # take tonic lines in a list to remove in the future
            self.tonic_lines.append(t_line)
            self.zoom_selection.addItem(t_line)  # add item to zoom selection

    def set_hist_cursor_pos(self, pos):
        """
        Sets the position of histogram in y-axis.
        :param pos: (int or float) Playback position in seconds.
        """
        pos_sample = np.int(pos * self.samplerate / self.hopsize)
        self.hline_histogram.setPos(pos=[0, self.pitch_plot[pos_sample]])

    def update_notes(self, xmin, xmax):
        start_ind = self.find_nearest_index(self.notes_start, xmin)
        end_ind = self.find_nearest_index(self.notes_end, xmax)

        self.remove_given_items(self.zoom_selection, self.rois)
        self.rois = []

        for i in range(start_ind, end_ind):
            temp_note = self.notes[i]
            roi = pg.ROI(pos=[temp_note[0], temp_note[2]],
                         size=[temp_note[1] - temp_note[0], 5])
            roi.addScaleHandle(pos=[0, 0], center=[0.5, 0.5])
            roi.addScaleHandle(pos=[1, 1], center=[0.5, 0.5])
            self.zoom_selection.addItem(roi)
            self.rois.append(roi)

    @staticmethod
    def remove_given_items(obj, items):
        """
        Removes the given items from the given object
        :param obj: pyqtgraph.GraphicsWidget object
        :param items: (list) Sequence of pyqtgraph.GraphicsObject object
        """
        for item in items:
            obj.removeItem(item)

    @staticmethod
    def find_nearest_index(n_array, value):
        index = (np.abs(n_array - value)).argmin()
        val = n_array[index]
        if value < val:
            return index
        else:
            return index + 1
