import os

from PyQt4 import QtGui

CSS_PROGRESS = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                            'css', 'progressbar.css')


class ProgressBar(QtGui.QProgressBar):
    def __init__(self, parent=None):
        QtGui.QProgressBar.__init__(self, parent)
        self.setGeometry(30, 40, 200, 25)
        self._set_css(self, CSS_PROGRESS)
        self.setToolTip('Downloading...')

    def update_progress_bar(self, index, work_number):
        """Updates the progressbar while querying"""

        progress = (float(index) / work_number) * 100
        self.setTextVisible(True)
        self.setFormat("{0}/{1}".format(index, work_number))
        self.setValue(progress)

    @staticmethod
    def _set_css(obj, css_path):
        with open(css_path) as f:
            css = f.read()
        obj.setStyleSheet(css)
