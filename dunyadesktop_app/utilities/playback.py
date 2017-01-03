from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, pyqtSignal


class Player:
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()

    def __init__(self):
        self.player = QMediaPlayer()

    def set_source(self, audio_path):
        url = QUrl.fromLocalFile(audio_path)
        media = QMediaContent(url)
        self.player.setNotifyInterval(25)
        self.player.setMedia(media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()


'''''
#from PyQt4 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
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


class AudioPlaybackThread(QThread):
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()

    def __init__(self, timer_pitch=50):
        QThread.__init__(self)
        #self.timer_pitch = timer_pitch
        self.playback = AudioPlayback()
        self.playback_pos = 0.

        #self.timer = QTimer()
        #self.timer.setInterval(timer_pitch)
        #self.timer.timeout.connect(self.send_signal)

    def run(self):
        self.playback.play()
        self.play_clicked.emit()

    def pause(self):
        self.playback.pause()
        self.pause_clicked.emit()
'''''