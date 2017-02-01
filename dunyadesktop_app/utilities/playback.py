from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QThread


class Playback(QMediaPlayer):
    def __init__(self, parent=None):
        QMediaPlayer.__init__(self, parent=parent)
        self.mediaStatusChanged.connect(self.status_changed)

    def set_source(self, audio_path):
        url = QUrl.fromLocalFile(audio_path)
        media = QMediaContent(url)
        self.setNotifyInterval(35)
        self.setMedia(media)

    def status_changed(self, status):
        if status == 7:
            self.player.pause()