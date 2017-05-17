import os

from PyQt5.QtWidgets import (QDockWidget, QSizePolicy, QWidget, QVBoxLayout,
                             QFrame, QLabel, QToolButton, QHBoxLayout,
                             QSpacerItem, QDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize, Qt

from .table import TableWidget, TableViewCollections, DialogCollTable
from .listwidget import CollectionsWidget
from .newcollectiondialog import NewCollectionDialog
from utilities import database

COMPMUSIC_LOGO = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                              'icons', 'compmusic_white.svg')


class DockWidget(QDockWidget):
    """Dockwidget for the main window"""

    def __init__(self, min_width, min_height, max_width, max_height):
        QDockWidget.__init__(self)
        self._set_dockwidget(min_width, min_height, max_width, max_height)

    def _set_dockwidget(self, min_width, min_height, max_width, max_height):
        """Sets the size policies of the dock widget"""
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QSize(min_width, min_height))
        self.setMaximumSize(QSize(max_width, max_height))
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setAllowedAreas(Qt.NoDockWidgetArea)
        self.setTitleBarWidget(QWidget(None))


class DockWidgetContentsLeft(QWidget):
    """Contains the contents of the dock widget on the left side of the main
    window"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # self._set_widget()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 15, 15, 15)
        # layout.setSpacing(10)  # check it

        self.frame_collection = QFrame(self)
        self._set_frame()

        layout_3 = QVBoxLayout(self.frame_collection)
        layout_3.setContentsMargins(2, 5, 3, 2)
        layout_3.setSpacing(4)  # check it

        self.label_collections = QLabel(self.frame_collection)
        self.label_collections.setIndent(15)  # check it
        self.label_collections.setTextInteractionFlags(Qt.NoTextInteraction)
        layout_3.addWidget(self.label_collections)

        self.listView_collections = CollectionsWidget()
        layout_3.addWidget(self.listView_collections)
        layout.addWidget(self.frame_collection)

        # toolbutton
        self.toolButton_collection = QToolButton(self)
        self._set_toolbutton(self.toolButton_collection)
        layout_3.addWidget(self.toolButton_collection)

        self.frame_downloaded = QFrame(self)
        self._set_frame_downloaded()

        layout_4 = QVBoxLayout(self.frame_downloaded)
        layout_4.setContentsMargins(3, 5, 3, 2)

        layout_5 = QHBoxLayout()
        self.button_colltable = QToolButton(self)
        self._set_toolbutton(self.button_colltable)
        self.button_colltable.setText('Open Table')
        self.label_downloaded = QLabel(self.frame_downloaded)
        self._set_label_downloaded()

        layout_5.addWidget(self.label_downloaded)
        layout_5.addWidget(self.button_colltable)
        layout_4.addLayout(layout_5)

        self.tableView_downloaded = TableWidget()
        layout_4.addWidget(self.tableView_downloaded)
        layout.addWidget(self.frame_downloaded)
        self.retranslateUi()

        # signals
        self.toolButton_collection.clicked.connect(self.new_collection)
        self.button_colltable.clicked.connect(self._open_coll_table)

    def _open_coll_table(self):
        current_coll = self.listView_collections.currentItem()
        if current_coll:
            self.coll_dialog = DialogCollTable(self)
            self.coll_dialog.label_collection.setText(current_coll.text())

            conn, c = database.connect()
            collection = database.fetch_collection(c, current_coll.text())
            self.coll_dialog.model.add_score(collection)
            conn.close()

            self.coll_dialog.show()

    def _set_widget(self):
        """Sets the size policies."""
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding,
                                  QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMaximumSize(QSize(500, 16777215))

    def _set_frame(self):
        """Sets the size policies of the frame."""
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding,
                                  QSizePolicy.Preferred)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(
        #    self.frame_collection.sizePolicy().hasHeightForWidth())
        self.frame_collection.setSizePolicy(size_policy)
        # self.frame_collection.setMinimumSize(QSize(0, 200))
        # self.frame_collection.setMaximumSize(QSize(16777215, 200))
        # self.frame_collection.setBaseSize(QSize(10, 10))
        self.frame_collection.setFrameShape(QFrame.Box)
        # self.frame_collection.setFrameShadow(QFrame.Raised)

    def _set_toolbutton(self, button):
        """Sets the size policies of the new collection button."""
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(size_policy)
        button.setMinimumSize(QSize(0, 30))
        button.setMaximumSize(QSize(16777215, 30))

        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        button.setAutoRaise(True)
        button.setArrowType(Qt.NoArrow)

    def _set_frame_downloaded(self):
        """Sets the size policies of the downloaded features frame."""
        self.frame_downloaded = QFrame(self)
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding,
                                  QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.frame_downloaded.sizePolicy().hasHeightForWidth())
        self.frame_downloaded.setSizePolicy(size_policy)
        self.frame_downloaded.setMinimumSize(QSize(0, 150))
        self.frame_downloaded.setBaseSize(QSize(0, 100))
        self.frame_downloaded.setFrameShape(QFrame.StyledPanel)
        self.frame_downloaded.setFrameShadow(QFrame.Raised)

    def _set_label_downloaded(self):
        """Sets the label 'Downloaded'."""
        font = QFont()
        font.setFamily("Garuda")
        self.label_downloaded.setFont(font)
        self.label_downloaded.setIndent(15)

    def retranslateUi(self):
        self.label_collections.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD "
                                       "HTML 4.0//EN\" "
                                       "\"http://www.w3.org/TR/REC-html40"
                                       "/strict.dtd\">\n "
                                       "<html><head><meta name=\"qrichtext\" "
                                       "content=\"1\" /><style "
                                       "type=\"text/css\">\n "
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" "
                                       "font-family:\'Ubuntu\'; "
                                       "font-size:11pt; font-weight:400; "
                                       "font-style:normal;\">\n "
                                       "<p style=\" margin-top:12px; "
                                       "margin-bottom:12px; margin-left:0px; "
                                       "margin-right:0px; "
                                       "-qt-block-indent:0; "
                                       "text-indent:0px;\"><span style=\" "
                                       "font-size:10pt; "
                                       "color:#878787;\">COLLECTIONS</span"
                                       "></p></body></html>")
        self.toolButton_collection.setText("New Collection")
        self.label_downloaded.setText("<html><head/><body><p><span style=\" "
                                      "font-size:10pt; "
                                      "color:#878787;\">DOWNLOADED "
                                      "FEATURES</span></p></body></html>")

    def new_collection(self):
        n_coll = NewCollectionDialog(self)
        n_coll.exec_()

    def change_downloaded_text(self, name):
        self.label_downloaded.setText("<html><head/><body><p><span style=\" "
                                      "font-size:10pt; color:#878787;\">{"
                                      "0}</span></p></body></html>".format(
            name))
        self._set_label_downloaded()
        self.label_collections.setIndent(15)  # check it
        self.label_collections.setTextInteractionFlags(Qt.NoTextInteraction)

    def update_collection_widget(self):
        conn, c = database.connect(add_main=True)
        database._add_docs_to_maincoll(conn, c)

        colls = database.get_collections(c)
        self.listView_collections.update_list([coll[0] for coll in colls])
        conn.close()


class DockWidgetContentsTop(QWidget):
    """Contains the contents of the dock widget on the top side of the main
        window"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 0, 4, 0)
        layout.setSpacing(5)  # check it

        spacer = QSpacerItem(20, 50, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer)

        compmusic_logo = QLabel()
        compmusic_logo.setText(
            '''<img src='{0}' width=70>'''.format(COMPMUSIC_LOGO))

        layout.addWidget(compmusic_logo)

        self.label_corpus = QLabel()
        self._set_label_corpus()
        layout.addWidget(self.label_corpus)

        spacer2 = QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer2)

        self.label_username = QLabel()
        self.label_username.setContextMenuPolicy(Qt.NoContextMenu)
        layout.addWidget(self.label_username)

        self.line = QFrame()
        self._set_line()
        layout.addWidget(self.line)

        self.label_status = QLabel()
        self._set_labelstatus()
        layout.addWidget(self.label_status)
        self.retranslate_ui()

    def _set_label_corpus(self):
        """Sets the label"""
        font = QFont()
        font.setFamily("Garuda")
        self.label_corpus.setFont(font)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHeightForWidth(
            self.label_corpus.sizePolicy().hasHeightForWidth())
        self.label_corpus.setSizePolicy(size_policy)
        self.label_corpus.setMinimumSize(QSize(300, 30))
        self.label_corpus.setMaximumSize(QSize(700, 30))

    def _set_line(self):
        """Vertical line between the status and username"""
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(size_policy)
        self.line.setMinimumSize(QSize(0, 20))
        self.line.setLineWidth(1)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

    def _set_labelstatus(self):
        """Sets the size policy of label status"""
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(size_policy)

    def retranslate_ui(self):
        self.label_username.setText("<html><head/><body><p "
                                    "align=\"right\"><span style=\" "
                                    "font-weight:600; "
                                    "color:#7c7c7c;\">user.name</span></p"
                                    "></body></html>")
        self.label_status.setText('<html><head/><body><p><span style=" '
                                  'font-size:10pt; '
                                  'color:#73ff7c;">online</span></p></body'
                                  '></html>')
        self.label_corpus.setText('<html><head/><body><p '
                                  'align="center"><span style=" '
                                  'font-size:15pt; '
                                  'color:#C1C1C1;">CORPUS</span></p></body'
                                  '></html>')
