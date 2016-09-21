import sys
import os.path

from PyQt4 import QtGui, QtCore

import ui_files.resources_rc

ICON_COMPMUSIC = os.path.join(os.path.dirname(__file__), 'ui_files',
                                'icons', 'compmusic-logo-white.svg')
CSS_PATH = os.path.join(os.path.dirname(__file__), 'ui_files', 'css',
                        'splashscreen.css')


class SplashScreen(QtGui.QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.SplashScreen)

        self.setFixedSize(680, 380)

        self._set_css()

    def _set_css(self):
        with open(CSS_PATH) as f:
            css = f.read()
        self.setStyleSheet(css)


app = QtGui.QApplication(sys.argv)
dialog = SplashScreen()
dialog.show()
app.exec_()