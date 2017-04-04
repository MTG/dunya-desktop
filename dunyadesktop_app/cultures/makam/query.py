from ..dunya import makam
from PyQt5.QtCore import QThread, QObject, pyqtSignal


class WorkObject(QObject):
    def __init__(self, work):
        QObject.__init__(self)
        self.work = work


class ComboboxResultsObject(QObject):
    def __init__(self, results):
        QObject.__init__(self)
        self.results = results


class ProgressBarStatusObject(QObject):
    def __init__(self, status):
        QObject.__init__(self)
        self.status = status


class CompletedObject(QObject):
    def __init__(self, status):
        QObject.__init__(self)
        self.status = status


class QueryThread(QThread):
    fetching_completed = pyqtSignal(object)
    progress_number = pyqtSignal(object)
    query_completed = pyqtSignal(object)
    combobox_results = pyqtSignal(object)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.stopped = False

        self.mid = None
        self.uid = None
        self.fid = None
        self.cmbid = None
        self.ambid = None
        self.iid = None

        self.parent = self.parent()
        self.fetching_completed.connect(self.parent.work_received)
        self.combobox_results.connect(self.parent.change_combobox_backgrounds)
        self.progress_number.connect(self.parent.set_progress_number)
        self.query_completed.connect(self.parent.query_finished)

    def check_selection(self):
        iteration = iter([self.mid, self.fid, self.uid,
                          self.cmbid, self.ambid])
        return any(iteration) and not any(iteration)

    def fetch_recordings(self):
        for work in self.works:
            w = makam.get_work(work['mbid'])
            self.fetching_completed.emit(WorkObject(w))

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

        combobox_status = ComboboxResultsObject(self.combobox_status)
        progressbar_status = ProgressBarStatusObject(len(self.works))
        completed = CompletedObject(True)

        self.combobox_results.emit(combobox_status)
        self.progress_number.emit(progressbar_status)
        self.fetch_recordings()
        self.query_completed.emit(completed)
