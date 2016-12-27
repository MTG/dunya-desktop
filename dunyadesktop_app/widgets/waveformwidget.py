from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QSize, Qt
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np

pg.setConfigOptions(useOpenGL=True)


class WaveformWidget(GraphicsLayoutWidget):
    def __init__(self):
        GraphicsLayoutWidget.__init__(self, parent=None)

        self.layout = pg.GraphicsLayout()
        self._set_size_policy()

    def _set_size_policy(self):
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(50)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setMinimumSize(QSize(0, 50))
        self.setMaximumSize(QSize(16777215, 50))
        self.setFocusPolicy(Qt.NoFocus)
        self.setAcceptDrops(False)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def plot_waveform(self, raw_audio, len_audio, min_audio, max_audio):
        self.waveform = self.layout.addPlot()
        self.waveform.hideAxis(axis='bottom')
        self.waveform.hideAxis(axis='left')

        self.waveform.setMaximumHeight(200)
        self.waveform.setMouseEnabled(x=False, y=False)
        self.waveform.setMenuEnabled(False)

        raw_audio += np.abs(np.min(raw_audio))

        self.waveform.setDownsampling(auto=True, mode='peak')
        self.waveform.plot(y=raw_audio, connect='finite',
                           pen=(20, 170, 100, 90),
                           clipToView=True)
        self.layout.addItem(self.waveform)
        self._add_elements_to_plot(len_audio, np.max(raw_audio))

        self.addItem(self.layout)

    def _add_elements_to_plot(self, len_audio, max_audio):
        pos_wf_x_max = len_audio / 25.
        self.region_wf = pg.LinearRegionItem([0, pos_wf_x_max],
                                             brush=pg.mkBrush((50, 255, 255, 45)),
                                             bounds=[0., len_audio])
        self.vline_wf = pg.ROI([0, 0], [0, max_audio], angle=0,
                               pen=pg.mkPen((255, 40, 35, 150), cosmetic=True,
                                            width=1))
        self.waveform.addItem(self.vline_wf)
        self.waveform.addItem(self.region_wf)
