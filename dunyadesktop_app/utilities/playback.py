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
        self.player.setNotifyInterval(35)
        self.player.setMedia(media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()
