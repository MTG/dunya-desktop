import os

from PyQt4 import QtGui, QtCore
from dunyadesktop_app.utilities import database


CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'menu.css')
DUNYA_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'dunya.svg')


class CollectionAction(QtGui.QAction):
    def __init__(self, name, parent=None):
        QtGui.QAction.__init__(self, name, parent)
        self.triggered.connect(self.send_coll)

    def send_coll(self):
        self.parent()._come_signal(self.text())


class RCMenu(QtGui.QMenu):
    def __init__(self, parent=None):
        self.parent = parent
        QtGui.QMenu.__init__(self, self.parent)
        #self._set_css()
        self._add_actions()

    def _set_css(self):
        with open(CSS_PATH) as f:
            css = f.read()
        self.setStyleSheet(css)

    def _add_actions(self):
        self.open_dunya = QtGui.QAction("Open on Player", self)
        self.open_dunya.setIcon(QtGui.QIcon(DUNYA_ICON))
        self.addAction(self.open_dunya)

        self.addSeparator()
        collections_menu = self.addMenu('Add to collection')

        conn, c = database.connect()
        collections = database.get_collections(c)

        for coll in collections:
            act = CollectionAction(str(coll[0]), self)
            collections_menu.addAction(act)
        conn.close()

    def _come_signal(self, coll):
        print(coll)
