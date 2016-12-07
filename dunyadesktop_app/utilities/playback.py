from PyQt4 import QtCore
import pyglet.media


class AudioPlayback:
    def __init__(self):
        self.player = pyglet.media.Player()

    def set_source(self, audio_path):
        source = pyglet.media.load(audio_path)
        self.player.queue(source)
        self.duration = self.player.source.duration - 0.5

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
    time_out = QtCore.pyqtSignal(float)

    def __init__(self, timer_pitch=50):
        QtCore.QThread.__init__(self)
        self.timer_pitch = timer_pitch
        self.playback = AudioPlayback()
        self.playback_pos = 0.

        self.timer = QtCore.QTimer()
        self.timer.setInterval(timer_pitch)
        self.timer.timeout.connect(self.send_signal)

    def run(self):
        self.timer.start()
        self.playback.play()

    def pause(self):
        self.timer.stop()
        self.playback.pause()

    def send_signal(self):
        self.playback_pos += self.timer_pitch / 1000.
        if self.playback.is_playing():
            if self.playback_pos < self.playback.get_pos_seconds():
                self.playback_pos = self.playback.get_pos_seconds()
                self.time_out.emit(self.playback_pos)

            elif self.playback_pos >= self.playback.duration:
                self.timer.stop()
                self.playback.pause()
            else:
                self.time_out.emit(self.playback_pos)
        else:
            self.timer.stop()
            self.playback.pause()