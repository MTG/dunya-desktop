import sys

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
        self.setStyleSheet("background-color: rgb(253, 255, 222);")

    def set_svg(self, path):
        self.svg_path = path
        self.tree, self.root = initialize_svg(path)
        self.load(self.svg_path)

    def update_note(self, svg_path, note_index):
        if self.svg_path != svg_path:
            self.svg_path = svg_path
            self.set_svg(self.svg_path)
            change_color(self.svg_path, self.tree, self.root, self.note_index,
                         'black')

        if self.note_index != note_index:
            change_color(self.svg_path, self.tree, self.root, self.note_index,
                         'black')
            self.note_index = note_index
            change_color(self.svg_path, self.tree, self.root, note_index, 'red')
            self.load(self.svg_path)

    def closeEvent(self, QCloseEvent):
        change_color(self.svg_path, self.tree, self.root, self.note_index,
                     'black')

class ScoreDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setStyleSheet("background-color: rgb(253, 255, 222);")
        layout = QVBoxLayout(self)
        self.score_widget = ScoreWidget(self)
        layout.addWidget(self.score_widget)


'''
app = QApplication(sys.argv)
scr = ScoreDialog()
scr.show()
scr.show_score('/Users/hsercanatli/Documents/codes/dunya-desktop/dunyadesktop_app/cultures/scores/ac003195-9ea0-4d8e-8420-2d6c269e98f6/scoresvg--2.svg')

app.exec_()
'''