from __future__ import absolute_import

from PyQt4 import QtGui


class ProgressBar(QtGui.QProgressBar):
    def __init__(self, parent=None):
        QtGui.QProgressBar.__init__(self, parent)
        self.setGeometry(30, 40, 200, 25)

    def update_progress_bar(self, index, work_number):
        """Updates the progressbar while querying"""

        progress = (float(index) / work_number) * 100
        self.setTextVisible(True)
        self.setFormat("{0}/{1}".format(index, work_number))
        self.setValue(progress)