from PyQt4 import QtCore
import pyglet.media


class AudioPlayback:
    def __init__(self):
        self.player = pyglet.media.Player()

    def set_source(self, audio_path):
        source = pyglet.media.load(audio_path)
        self.player.queue(source)

    def get_pos_sample(self):
        return self.player.time * 44100.

    def get_pos_seconds(self):
        return self.player.time

    def is_playing(self):
        return self.player.playing

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def seek(self, time):
        self.player.seek(time=time)


class AudioPlaybackThread(QtCore.QThread):
    time_out = QtCore.pyqtSignal()
    time_out_wf = QtCore.pyqtSignal()

    def __init__(self, timer_pitch=50, timer_wf=300):
        QtCore.QThread.__init__(self)
        self.playback = AudioPlayback()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(timer_pitch)

        self.timer_wf = QtCore.QTimer()
        self.timer_wf.setInterval(timer_wf)

        self.timer.timeout.connect(self.send_signal)
        self.timer_wf.timeout.connect(self.send_signal_wf)

    def run(self):
        self.timer.start()
        self.timer_wf.start()
        self.playback.play()

    def pause(self):
        self.timer.stop()
        self.timer_wf.stop()
        self.playback.pause()

    def send_signal(self):
        self.time_out.emit()

    def send_signal_wf(self):
        self.time_out_wf.emit()