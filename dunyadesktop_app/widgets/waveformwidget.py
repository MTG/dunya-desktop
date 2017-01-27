from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np

pg.setConfigOptions(useOpenGL=True)
pg.setConfigOptions(useWeave=True)
# pg.setConfigOptions(crashWarning=True)


class WaveformRegionItem(pg.LinearRegionItem):
    clicked = pyqtSignal()

    def __init__(self, values=[0,1], orientation=None, brush=None,
                 movable=True, bounds=None):
        pg.LinearRegionItem.__init__(self, values=values,
                                     orientation=orientation, brush=brush,
                                     movable=movable, bounds=bounds)

    def mouseClickEvent(self, ev):
        self.clicked.emit()
        super(WaveformRegionItem, self).mouseClickEvent(ev)

    def mouseDragEvent(self, ev):
        self.clicked.emit()
        super(WaveformRegionItem, self).mouseDragEvent(ev)


class WaveformWidget(GraphicsLayoutWidget):
    def __init__(self):
        GraphicsLayoutWidget.__init__(self, parent=None)

        self.layout = pg.GraphicsLayout()
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
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

    def plot_waveform(self, raw_audio):
        self.raw_audio = raw_audio
        self.waveform = self.layout.addPlot()
        self.waveform.hideAxis(axis='bottom')
        self.waveform.hideAxis(axis='left')

        # self.waveform.setMaximumHeight(200)
        self.waveform.setMouseEnabled(x=False, y=False)
        self.waveform.setMenuEnabled(False)

        # self.raw_audio += np.abs(np.min(raw_audio))
        self.update_wf_plot()
        self.waveform.setDownsampling(auto=True, mode='peak')
        self.layout.addItem(self.waveform)
        self._add_elements_to_plot(len(self.visible), np.min(self.visible),
                                   np.max(self.visible))

        self.addItem(self.layout)

    def _add_elements_to_plot(self, len_audio, min_audio, max_audio):
        pos_wf_x_max = len_audio / 25.
        self.region_wf = WaveformRegionItem([0, pos_wf_x_max],
                                            brush=pg.mkBrush((50, 255,
                                                              255, 45)),
                                             bounds=[0., len_audio])

        self.vline_wf = pg.ROI([0, min_audio], [0, max_audio - min_audio],
                               angle=0, pen=pg.mkPen((255, 40, 35, 150),
                                                     cosmetic=True, width=1))
        self.waveform.addItem(self.vline_wf)
        self.waveform.addItem(self.region_wf)

    def update_wf_plot(self):
        start = 0
        stop = len(self.raw_audio)

        # Decide by how much we should downsample
        ds = int((stop - start) / self.limit) + 1

        if ds == 1:
            # Small enough to display with no intervention.
            visible = self.raw_audio[start:stop]
            # scale = 1
        else:
            # Here convert data into a down-sampled array suitable for
            # visualizing.
            # Must do this piecewise to limit memory usage.
            samples = 1 + ((stop - start) // ds)
            visible = np.zeros(samples * 2, dtype=self.raw_audio.dtype)
            source_ptr = start
            target_ptr = 0

            # read data in chunks of ~1M samples
            chunk_size = (1000000 // ds) * ds
            while source_ptr < stop - 1:
                chunk = \
                    self.raw_audio[source_ptr:min(stop, source_ptr +
                                                  chunk_size)]
                source_ptr += len(chunk)

                # reshape chunk to be integral multiple of ds
                chunk = chunk[:(len(chunk) // ds) * ds].reshape(
                    len(chunk) // ds, ds)

                # compute max and min
                chunk_max = chunk.max(axis=1)
                chunk_min = chunk.min(axis=1)

                # interleave min and max into plot data to preserve envelope
                # shape
                visible[target_ptr:target_ptr + chunk.shape[0] * 2:2] = \
                    chunk_min
                visible[1 + target_ptr:1 + target_ptr + chunk.shape[0] * 2:2] \
                    = chunk_max
                target_ptr += chunk.shape[0] * 2

            self.visible = visible[:target_ptr]
            # scale = ds * 0.5
        self.visible[-1] = np.nan
        self.waveform.clearPlots()
        self.waveform.plot(visible, connect='finite',
                           pen=(20, 170, 100, 80))
        # self.waveform.setPos(start, 0)  # shift to match starting index
        self.waveform.resetTransform()
        # self.waveform.scale(scale, 1)  # scale to match downsampling

    def get_waveform_region(self):
        pos_wf_x_min, pos_wf_x_max = self.region_wf.getRegion()
        ratio = len(self.raw_audio) / len(self.visible)
        x_min = (pos_wf_x_min * ratio) / self.samplerate
        x_max = (pos_wf_x_max * ratio) / self.samplerate
        return x_min, x_max

    def change_wf_region(self, x_start, x_end):
        ratio = len(self.raw_audio) / len(self.visible)

        x_start = (x_start * self.samplerate) / ratio
        x_end = (x_end * self.samplerate) / ratio
        self.region_wf.setRegion([x_start, x_end])
