from PyQt4 import QtCore
from compmusic.dunya import makam


class QueryThread(QtCore.QThread):
    fetching_completed = QtCore.pyqtSignal(dict)
    progress_number = QtCore.pyqtSignal(int)
    query_completed = QtCore.pyqtSignal()
    combobox_results = QtCore.pyqtSignal(list)

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

    def check_attribute_existence(self, combobox_index):
        if len(self.data['works']) > 0 or len(self.recordings) > 0:
            self.combobox_status[combobox_index] = 1
        else:
            self.combobox_status[combobox_index] = 2

    def run(self):
        self.recordings = []
        self.works = []
        check_list = [self.mid, self.fid, self.uid, self.cmbid, self.ambid]
        self.combobox_status = [0, 0, 0, 0, 0, 0]

        if self.check_selection():
            iteration = iter([self.mid, self.fid, self.uid,
                              self.cmbid, self.ambid])
            selection = next(i for i, s in enumerate(iteration) if s)

            if selection is 0:
                self.data = makam.get_makam(self.mid)
                self.recordings = [rec for rec in self.data['taksims']]
                self.recordings += [rec for rec in self.data['gazels']]
                self.check_attribute_existence(0)

            elif selection is 1:
                self.data = makam.get_form(self.fid)
                self.check_attribute_existence(1)

            elif selection is 2:
                self.data = makam.get_usul(self.uid)
                self.check_attribute_existence(2)

            elif selection is 3:
                self.data = makam.get_composer(self.cmbid)
                self.check_attribute_existence(3)

            elif selection is 4:
                self.data = makam.get_artist(self.ambid)
                self.check_attribute_existence(4)

            else:
                self.data = makam.get_instrument(self.iid)
                self.check_attribute_existence(5)

            self.works = [work for work in self.data['works']]

        else:
            self.works = makam.get_works_by_query(mid=self.mid, uid=self.uid,
                                                  fid=self.fid,
                                                  cmbid=self.cmbid,
                                                  ambid=self.ambid)
            selected_indexes = [i for i, j in enumerate(check_list) if
                                j != '']

            if len(self.works) > 0:
                for i in selected_indexes:
                    self.combobox_status[i] = 1
            else:
                for i in selected_indexes:
                    self.combobox_status[i] = 2

        self.combobox_results.emit(self.combobox_status)
        self.progress_number.emit(len(self.works))
        self.fetch_recordings()
        self.query_completed.emit()
