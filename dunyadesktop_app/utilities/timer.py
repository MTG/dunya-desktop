from PyQt4 import QtCore


class TimerThread(QtCore.QThread):
    time_out = QtCore.pyqtSignal()
    time_out_wf = QtCore.pyqtSignal()

    def __init__(self, parent=None, interval=50):
        QtCore.QThread.__init__(self)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(interval)

        self.timer_wf = QtCore.QTimer()
        self.timer_wf.setInterval(250)

        self.timer.timeout.connect(self.send_signal)
        self.timer_wf.timeout.connect(self.send_signal_wf)

    def run(self):
        self.timer.start()
        self.timer_wf.start()

    def stop(self):
        self.timer.stop()
        self.timer_wf.stop()

    def send_signal(self):
        self.time_out.emit()

    def send_signal_wf(self):
        self.time_out_wf.emit()
