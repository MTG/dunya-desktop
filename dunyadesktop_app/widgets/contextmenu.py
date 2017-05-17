import os

from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtGui import QIcon
from utilities import database

DUNYA_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'dunya.svg')


class CollectionAction(QAction):
    def __init__(self, name, parent=None):
        QAction.__init__(self, name, parent)
        self.triggered.connect(self._send_coll)

    def _send_coll(self):
        self.parent()._send_request_to_parent(self.text())


class RCMenu(QMenu):
    def __init__(self, parent=None):
        QMenu.__init__(self, parent)
        self._add_actions()


        self.open_dunya.triggered.connect(self._send_player_request)

    def _add_actions(self):
        self.open_dunya = QAction("Open on Player", self)
        self.open_dunya.setIcon(QIcon(DUNYA_ICON))
        self.addAction(self.open_dunya)

        self.addSeparator()
        collections_menu = self.addMenu('Add to collection')

        conn, c = database.connect()
        collections = database.get_collections(c)

        for coll in collections:
            act = CollectionAction(str(coll[0]), self)
            collections_menu.addAction(act)
        conn.close()

    def _send_request_to_parent(self, coll):
        self.parent().send_to_db(str(coll))

    def _send_player_request(self):
        self.parent().send_rec()

    def return_selected_row_indexes(self):
        try:
            indexes = self.parent().selectedIndexes()
            user_rows = list(set([ind.row() for ind in indexes]))
            return user_rows
        except:
            return
