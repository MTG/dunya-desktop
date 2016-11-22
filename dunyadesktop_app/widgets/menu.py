import os

from PyQt4 import QtGui, QtCore
from dunyadesktop_app.utilities import database


CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'menu.css')
DUNYA_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'dunya.svg')


class RCMenu(QtGui.QMenu):
    def __init__(self, parent=None):
        QtGui.QMenu.__init__(self, parent)
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

        collections_menu = self.addMenu('Collections')

        self.add_maincoll = QtGui.QAction("Add to main collection", self)
        collections_menu.addAction(self.add_maincoll)
        collections_menu.addSeparator()

        conn, c = database.connect()
        collections = database.get_collections(c)

        for coll in collections:
            act = QtGui.QAction(str(coll[0]), self)
            collections_menu.addAction(act)
        conn.close()
