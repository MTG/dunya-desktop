import sys
import os.path

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import QtCore

from .widgets.widgetutilities import set_css

import ui_files.resources_rc

ICON_COMPMUSIC = os.path.join(os.path.dirname(__file__), 'ui_files',
                                'icons', 'compmusic-logo-white.svg')
CSS_PATH = os.path.join(os.path.dirname(__file__), 'ui_files', 'css',
                        'splashscreen.css')


class SplashScreen(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.SplashScreen)

        self.setFixedSize(680, 380)
        set_css(self, CSS_PATH)


app = QApplication(sys.argv)
dialog = SplashScreen()
dialog.show()
app.exec_()