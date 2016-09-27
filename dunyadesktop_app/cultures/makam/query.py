from __future__ import print_function

from PyQt4 import QtCore
from compmusic.dunya import makam


class QueryThread(QtCore.QThread):
    fetching_completed = QtCore.pyqtSignal(dict)
    progress_number = QtCore.pyqtSignal(int)
    query_completed = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.stopped = False

        self.mid = None
        self.uid = None
        self.fid = None
        self.cmbid = None
        self.ambid = None
        self.iid = None

    def check_selection(self):
        iteration = iter([self.mid, self.fid, self.uid,
                          self.cmbid, self.ambid])
        return any(iteration) and not any(iteration)

    def fetch_recordings(self):
        for work in self.works:
            self.fetching_completed.emit(makam.get_work(work['mbid']))

    def run(self):
        if self.check_selection():
            iteration = iter([self.mid, self.fid, self.uid,
                              self.cmbid, self.ambid])
            selection = next(i for i, s in enumerate(iteration) if s)

            if selection is 0:
                self.data = makam.get_makam(self.mid)
                self.recordings = [rec for rec in self.data['taksims']]
                self.recordings += [rec for rec in self.data['gazels']]
            elif selection is 1:
                self.data = makam.get_form(self.fid)
            elif selection is 2:
                self.data = makam.get_usul(self.uid)
            elif selection is 3:
                self.data = makam.get_composer(self.cmbid)
            elif selection is 4:
                self.data = makam.get_artist(self.ambid)
            else:
                self.data = makam.get_instrument(self.iid)

            self.works = [work for work in self.data['works']]

        else:
            print("more selection")
            self.works = makam.get_works_by_query(mid=self.mid, uid=self.uid,
                                                  fid=self.fid,
                                                  cmbid=self.cmbid,
                                                  ambid=self.ambid)
        self.progress_number.emit(len(self.works))
        self.fetch_recordings()
        self.query_completed.emit()