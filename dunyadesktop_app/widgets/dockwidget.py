import os

from PyQt5.QtWidgets import (QDockWidget, QSizePolicy, QWidget, QVBoxLayout,
                             QFrame, QLabel, QToolButton, QHBoxLayout,
                             QSpacerItem)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize, Qt

from table import TableWidget
from listwidget import CollectionsWidget
from newcollectiondialog import NewCollectionDialog
from dunyadesktop_app.utilities import database

CSS_DOCKWIDGET = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                              'css', 'dockwidget.css')

CSS_LABEL_COLLECTION = os.path.join(os.path.dirname(__file__), '..',
                                    'ui_files', 'css', 'label_collection.css')

CSS_FRAME_QUERY = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                               'css', 'frame_query.css')

CSS_FRAME_DOWNLOADED = os.path.join(os.path.dirname(__file__), '..',
                                    'ui_files', 'css', 'frame_downloaded.css')

CSS_FRAME_COLLECTION = os.path.join(os.path.dirname(__file__), '..',
                                    'ui_files', 'css', 'frame_collection.css')

CSS_LISTVIEW = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                            'css', 'listwidget.css')

CSS_TOOLBUTTON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                              'css', 'toolbutton_collection.css')

CSS_TABLEVIEW_DOWNLOADED = os.path.join(os.path.dirname(__file__), '..',
                                        'ui_files', 'css',
                                        'tableview_downloaded.css')


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
        self._set_widget()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 0, 0, 0)
        layout.setSpacing(0)  # check it

        self.frame_collection = QFrame(self)
        self._set_frame()

        layout_3 = QVBoxLayout(self.frame_collection)
        layout_3.setContentsMargins(2, 5, 3, 2)
        layout_3.setSpacing(7)  # check it

        self.label_collections = QLabel(self.frame_collection)
        self.label_collections.setIndent(15)  # check it
        self.label_collections.setTextInteractionFlags(Qt.NoTextInteraction)
        self._set_css(self.label_collections, CSS_LABEL_COLLECTION)
        layout_3.addWidget(self.label_collections)

        self.listView_collections = CollectionsWidget()
        layout_3.addWidget(self.listView_collections)
        layout.addWidget(self.frame_collection)

        # toolbutton
        self.toolButton_collection = QToolButton(self)
        self._set_toolbutton()
        layout.addWidget(self.toolButton_collection)

        self.frame_downloaded = QFrame(self)
        self._set_frame_downloaded()

        layout_4 = QVBoxLayout(self.frame_downloaded)
        layout_4.setContentsMargins(3, 5, 3, 2)
        self.label_downloaded = QLabel(self.frame_downloaded)
        self._set_label_downloaded()
        layout_4.addWidget(self.label_downloaded)

        self.tableView_downloaded = TableWidget()
        layout_4.addWidget(self.tableView_downloaded)
        layout.addWidget(self.frame_downloaded)
        self.retranslateUi()

        # signals
        self.toolButton_collection.clicked.connect(self.new_collection)

    def _set_widget(self):
        """Sets the size policies."""
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding,
                                  QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMaximumSize(QSize(500, 16777215))

    @staticmethod
    def _set_css(obj, css_path):
        with open(css_path) as f:
            css = f.read()
        obj.setStyleSheet(css)

    def _set_frame(self):
        """Sets the size policies of the frame."""
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding,
                                  QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.frame_collection.sizePolicy().hasHeightForWidth())
        self.frame_collection.setSizePolicy(size_policy)
        self.frame_collection.setMinimumSize(QSize(0, 200))
        self.frame_collection.setMaximumSize(QSize(16777215, 200))
        self.frame_collection.setBaseSize(QSize(0, 0))
        self._set_css(self.frame_collection, CSS_FRAME_COLLECTION)
        self.frame_collection.setFrameShape(QFrame.StyledPanel)
        self.frame_collection.setFrameShadow(QFrame.Raised)

    def _set_toolbutton(self):
        """Sets the size policies of the new collection button."""
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.toolButton_collection.sizePolicy().hasHeightForWidth())
        self.toolButton_collection.setSizePolicy(size_policy)
        self.toolButton_collection.setMinimumSize(QSize(0, 30))
        self.toolButton_collection.setMaximumSize(QSize(16777215, 30))
        self._set_css(self.toolButton_collection, CSS_TOOLBUTTON)

        self.toolButton_collection.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon)
        self.toolButton_collection.setAutoRaise(True)
        self.toolButton_collection.setArrowType(Qt.NoArrow)

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
        self._set_css(self.frame_downloaded, CSS_FRAME_DOWNLOADED)
        self.frame_downloaded.setFrameShape(QFrame.StyledPanel)
        self.frame_downloaded.setFrameShadow(QFrame.Raised)

    def _set_label_downloaded(self):
        """Sets the label 'Downloaded'."""
        font = QFont()
        font.setFamily("Garuda")
        self.label_downloaded.setFont(font)
        self.label_downloaded.setIndent(15)
        self._set_css(self.label_downloaded, CSS_LABEL_COLLECTION)

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
                                      "0}</span></p></body></html>".format(name))
        self._set_label_downloaded()
        self.label_collections.setIndent(15)  # check it
        self.label_collections.setTextInteractionFlags(Qt.NoTextInteraction)
        self._set_css(self.label_collections, CSS_LABEL_COLLECTION)

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

        spacer = QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer)

        self.label_corpus = QLabel(self)
        self._set_label_corpus()
        layout.addWidget(self.label_corpus)

        spacer2 = QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer2)

        self.label_username = QLabel(self)
        self.label_username.setContextMenuPolicy(Qt.NoContextMenu)
        layout.addWidget(self.label_username)

        self.line = QFrame(self)
        self._set_line()
        layout.addWidget(self.line)

        self.label_status = QLabel(self)
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
