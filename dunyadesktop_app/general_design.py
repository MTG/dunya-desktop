import sys
import os

from PyQt4 import QtGui, QtCore

from widgets.dockwidget import DockWidget, DockWidgetContentsLeft, \
    DockWidgetContentsTop
from widgets.queryframe import QueryFrame
from widgets.progressbar import ProgressBar


CSS_MAIN = os.path.join(os.path.dirname(__file__), 'ui_files', 'css',
                        'mainui.css')
CSS_FRAME_QUERY = os.path.join(os.path.dirname(__file__), 'ui_files', 'css',
                               'frame_query.css')
CSS_STATUSBAR = os.path.join(os.path.dirname(__file__), 'ui_files', 'css',
                             'statusbar.css')

DUNYA_ICON = ":/compmusic/icons/dunya.svg"
QUERY_ICON = ":/compmusic/icons/magnifying-glass.png"


class GeneralMainDesign(QtGui.QMainWindow):
    """General design of the main window"""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self._set_main_window()
        self._set_css(self, CSS_MAIN)

        self.centralwidget = QtGui.QWidget(self)

        layout = QtGui.QVBoxLayout(self.centralwidget)
        layout.setContentsMargins(0, 0, 2, 0)
        layout.setSpacing(0)

        # query frame
        self.frame_query = QueryFrame()
        self._set_css(self.frame_query, CSS_FRAME_QUERY)
        self._set_frame()
        layout.addWidget(self.frame_query)

        self.setCentralWidget(self.centralwidget)

        # status bar
        self.statusbar = QtGui.QStatusBar(self)
        self._set_css(self.statusbar, CSS_STATUSBAR)
        self._set_status_bar()
        self.setStatusBar(self.statusbar)

        self.progress_bar = ProgressBar(self)
        self.statusbar.addPermanentWidget(self.progress_bar)
        self.progress_bar.setVisible(False)

        # dockwidget collection (left side)
        self.dw_collections = DockWidget(270, 440, 400, 20000)
        self.dwc_left = DockWidgetContentsLeft()
        self.dw_collections.setWidget(self.dwc_left)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1),
                           self.dw_collections)

        self.dw_top = DockWidget(460, 50, 20000, 50)
        self.dwc_top = DockWidgetContentsTop()
        self.dw_top.setWidget(self.dwc_top)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dw_top)

        QtCore.QMetaObject.connectSlotsByName(self)

    def _set_main_window(self):
        """Sets the size policies of the main window"""
        self.resize(1000, 600)
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                        QtGui.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(1000, 600))

        # main window icon
        icon_dunya = QtGui.QIcon()
        icon_dunya.addPixmap(QtGui.QPixmap(DUNYA_ICON),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon_dunya)
        self.setWindowTitle('Dunya Desktop')

    @staticmethod
    def _set_css(obj, css_path):
        with open(css_path) as f:
            css = f.read()
        obj.setStyleSheet(css)

    def _set_frame(self):
        self.frame_query.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_query.setFrameShadow(QtGui.QFrame.Raised)

    def _set_status_bar(self):
        self.statusbar.setMinimumSize(QtCore.QSize(0, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.statusbar.setFont(font)
