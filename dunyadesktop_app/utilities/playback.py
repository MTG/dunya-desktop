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
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.playback = AudioPlayback()

    def run(self):
        self.playback.play()

    def stop(self):
        self.playback.pause()
