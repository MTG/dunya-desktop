from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtSvg import QSvgWidget

from cultures.makam.svgparser import change_color, initialize_svg


class ScoreWidget(QSvgWidget):
    def __init__(self, parent=None):
        QSvgWidget.__init__(self, parent=parent)
        self.__set_design()
        self.note_index = 0
        self.svg_path = ''

    def __set_design(self):
        self.setStyleSheet('background-color: #F4ECD7;')
        self.setFixedSize(450, 300)

    def set_svg(self, path):
        self.svg_path = path
        self.tree, self.root = initialize_svg(path)
        self.load(self.svg_path)

    def update_note(self, svg_path, note_index):
        if not hasattr(self, 'tree'):
            self.set_svg(svg_path)

        if self.svg_path != svg_path:
            change_color(self.svg_path, self.tree, self.root, self.note_index,
                         'black')
            self.set_svg(svg_path)

        if self.note_index != note_index:
            change_color(self.svg_path, self.tree, self.root, self.note_index,
                         'black')
            self.note_index = note_index
            change_color(self.svg_path, self.tree, self.root, note_index,
                         'red')
            self.load(self.svg_path)

    def close_event(self):
        if hasattr(self, 'tree'):
            change_color(self.svg_path, self.tree, self.root, self.note_index,
                         'black')
