import pyglet.media


class AudioPlayback:
    def __init__(self):
        # fname and arraging the source
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
        print("pressed play")
        self.player.play()

    def pause(self):
        self.player.pause()

    def seek(self, time):
        self.player.seek(time=time)
