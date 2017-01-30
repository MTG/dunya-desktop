from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


class Playback:
    def __init__(self):
        self.player = QMediaPlayer()

        self.player.mediaStatusChanged.connect(self.status_changed)
    def set_source(self, audio_path):
        url = QUrl.fromLocalFile(audio_path)
        media = QMediaContent(url)
        self.player.setNotifyInterval(35)
        self.player.setMedia(media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def status_changed(self, status):
        if status == 7:
            self.player.pause()