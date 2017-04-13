import os

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStatusBar, \
    QSizePolicy, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore

from widgets.dockwidget import DockWidget, DockWidgetContentsLeft, \
    DockWidgetContentsTop
from widgets.queryframe import QueryFrame
from widgets.progressbar import ProgressBar


DUNYA_ICON = os.path.join(os.path.dirname(__file__), 'ui_files', 'icons',
                          'dunya-desktop.svg')


class GeneralMainDesign(QMainWindow):
    """General design of the main window"""
    def __init__(self, QWidgetParent=None):
        QMainWindow.__init__(self, QWidgetParent)
        self._set_main_window()
        self.centralwidget = QWidget(self)

        layout = QVBoxLayout(self.centralwidget)
        layout.setContentsMargins(0, 0, 2, 0)
        layout.setSpacing(0)

        # query frame
        self.frame_query = QueryFrame()
        self._set_frame()
        layout.addWidget(self.frame_query)

        self.setCentralWidget(self.centralwidget)

        # status bar
        self.statusbar = QStatusBar(self)
        self._set_status_bar()
        self.setStatusBar(self.statusbar)

        self.progress_bar = ProgressBar(self)
        self.statusbar.addPermanentWidget(self.progress_bar)
        self.progress_bar.setVisible(False)

        self.dw_top = DockWidget(460, 90, 20000, 50)
        self.dwc_top = DockWidgetContentsTop()
        self.dw_top.setWidget(self.dwc_top)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.dw_top)

        # dockwidget collection (left side)
        self.dw_collections = DockWidget(350, 620, 700, 20000)
        self.dwc_left = DockWidgetContentsLeft(self)
        self.dw_collections.setWidget(self.dwc_left)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                           self.dw_collections)

        QtCore.QMetaObject.connectSlotsByName(self)

    def _set_main_window(self):
        """Sets the size policies of the main window"""
        self.resize(1000, 750)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(1000, 750))

        # main window icon
        self.setWindowIcon(QIcon(DUNYA_ICON))
        self.setWindowTitle('Dunya Desktop')

    def _set_frame(self):
        self.frame_query.setFrameShape(QFrame.StyledPanel)
        self.frame_query.setFrameShadow(QFrame.Raised)

    def _set_status_bar(self):
        self.statusbar.setMinimumSize(QtCore.QSize(0, 18))
        font = QFont()
        font.setPointSize(9)
        self.statusbar.setFont(font)
