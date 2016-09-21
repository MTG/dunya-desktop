from __future__ import print_function
from PyQt4 import QtCore
from compmusic.dunya import makam


class QueryThread(QtCore.QThread):
    completed = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.stopped = False

        self.mid = None
        self.uid = None
        self.fid = None
        self.cmbid = None
        self.ambid = None

        self.works = None

    def run(self):
        self.works = makam.get_works_by_query(mid=self.mid, uid=self.uid,
                                              fid=self.fid, cmbid=self.cmbid,
                                              ambid=self.ambid)
        for xx, work in enumerate(self.works):
            print(xx, work)
