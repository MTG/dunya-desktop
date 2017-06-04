import os

from PyQt5.QtWidgets import QRadioButton, QWidget, QVBoxLayout, QGroupBox
from PyQt5.QtCore import pyqtSignal

from cultures.makam.utilities import get_filenames_in_dir

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'scores')


class RadioButtonAdaptive(QRadioButton):
    def __init__(self, parent):
        QRadioButton.__init__(self, parent)
        self.clicked.connect(self._button_clicked)

    def _button_clicked(self):
        name_synthesis = self.text()
        parent = self.parent().parent()
        parent._synthesis_changed(name_synthesis)


class FeatureWidgetAdaptive(QWidget):
    synthesis_changed = pyqtSignal(str)

    def __init__(self, mbid, parent=None):
        QWidget.__init__(self, parent=parent)
        self.mbid = mbid
        self.group_box = QGroupBox('Synthesis', self)
        self._set_design()

    def _set_design(self):
        layout_synthesis = self._add_synthesis()
        self.group_box.setLayout(layout_synthesis)
        self.setMinimumWidth(150)

    def _add_synthesis(self):
        layout = QVBoxLayout()

        fullnames, folders, names = get_filenames_in_dir(os.path.join(
            DOCS_PATH, self.mbid))

        for name in names:
            radio_button = RadioButtonAdaptive(self)
            radio_button.setText(name.split('.mp3')[0])
            radio_button.setChecked(True)
            layout.addWidget(radio_button)
        layout.addStretch(1)
        return layout

    def _synthesis_changed(self, name):
        self.synthesis_changed.emit(name)

    def current_synthesis(self):
        children = self.group_box.children()

        for child in children:
            try:
                if child.isChecked() and child.text():
                    return child.text()
            except AttributeError:
                pass
