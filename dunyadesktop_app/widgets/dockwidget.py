import os

from PyQt4 import QtGui, QtCore

from table import TableWidget
from listwidget import CollectionsWidget
from newcollectiondialog import NewCollectionDialog

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


class DockWidget(QtGui.QDockWidget):
    """Dockwidget for the main window"""
    def __init__(self, min_width, min_height, max_width, max_height):
        QtGui.QDockWidget.__init__(self)
        self._set_dockwidget(min_width, min_height, max_width, max_height)

    def _set_dockwidget(self, min_width, min_height, max_width, max_height):
        """Sets the size policies of the dock widget"""
        sizepolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                       QtGui.QSizePolicy.Minimum)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizepolicy)
        self.setMinimumSize(QtCore.QSize(min_width, min_height))
        self.setMaximumSize(QtCore.QSize(max_width, max_height))
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        self.setTitleBarWidget(QtGui.QWidget(None))


class DockWidgetContentsLeft(QtGui.QWidget):
    """Contains the contents of the dock widget on the left side of the main
    window"""
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self._set_widget()

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(4, 0, 0, 0)
        layout.setSpacing(0)  # check it

        self.frame_collection = QtGui.QFrame(self)
        self._set_frame()

        layout_3 = QtGui.QVBoxLayout(self.frame_collection)
        layout_3.setContentsMargins(2, 5, 3, 2)
        layout_3.setSpacing(7)  # check it

        self.label_collections = QtGui.QLabel(self.frame_collection)
        self.label_collections.setIndent(15)  # check it
        self.label_collections.setTextInteractionFlags(
            QtCore.Qt.NoTextInteraction)
        self._set_css(self.label_collections, CSS_LABEL_COLLECTION)
        layout_3.addWidget(self.label_collections)

        self.listView_collections = CollectionsWidget()
        layout_3.addWidget(self.listView_collections)
        layout.addWidget(self.frame_collection)

        # toolbutton
        self.toolButton_collection = QtGui.QToolButton(self)
        self._set_toolbutton()
        layout.addWidget(self.toolButton_collection)

        self.frame_downloaded = QtGui.QFrame(self)
        self._set_frame_downloaded()

        layout_4 = QtGui.QVBoxLayout(self.frame_downloaded)
        layout_4.setContentsMargins(3, 5, 3, 2)
        self.label_downloaded = QtGui.QLabel(self.frame_downloaded)
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
        sizepolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                       QtGui.QSizePolicy.Preferred)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizepolicy)
        self.setMaximumSize(QtCore.QSize(500, 16777215))

    @staticmethod
    def _set_css(obj, css_path):
        with open(css_path) as f:
            css = f.read()
        obj.setStyleSheet(css)

    def _set_frame(self):
        """Sets the size policies of the frame."""
        sizepolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                       QtGui.QSizePolicy.Preferred)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(
            self.frame_collection.sizePolicy().hasHeightForWidth())
        self.frame_collection.setSizePolicy(sizepolicy)
        self.frame_collection.setMinimumSize(QtCore.QSize(0, 200))
        self.frame_collection.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame_collection.setBaseSize(QtCore.QSize(0, 0))
        self._set_css(self.frame_collection, CSS_FRAME_COLLECTION)

        self.frame_collection.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_collection.setFrameShadow(QtGui.QFrame.Raised)

    def _set_toolbutton(self):
        """Sets the size policies of the new collection button."""
        sizepolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                       QtGui.QSizePolicy.Fixed)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(
            self.toolButton_collection.sizePolicy().hasHeightForWidth())
        self.toolButton_collection.setSizePolicy(sizepolicy)
        self.toolButton_collection.setMinimumSize(QtCore.QSize(0, 30))
        self.toolButton_collection.setMaximumSize(QtCore.QSize(16777215, 30))
        self._set_css(self.toolButton_collection, CSS_TOOLBUTTON)

        self.toolButton_collection.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_collection.setAutoRaise(True)
        self.toolButton_collection.setArrowType(QtCore.Qt.NoArrow)

    def _set_frame_downloaded(self):
        """Sets the size policies of the downloaded features frame."""
        self.frame_downloaded = QtGui.QFrame(self)
        sizepolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                       QtGui.QSizePolicy.Preferred)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(
            self.frame_downloaded.sizePolicy().hasHeightForWidth())
        self.frame_downloaded.setSizePolicy(sizepolicy)
        self.frame_downloaded.setMinimumSize(QtCore.QSize(0, 150))
        self.frame_downloaded.setBaseSize(QtCore.QSize(0, 100))
        self._set_css(self.frame_downloaded, CSS_FRAME_DOWNLOADED)
        self.frame_downloaded.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_downloaded.setFrameShadow(QtGui.QFrame.Raised)

    def _set_label_downloaded(self):
        """Sets the label 'Downloaded'."""
        font = QtGui.QFont()
        font.setFamily("Garuda")
        self.label_downloaded.setFont(font)
        self.label_downloaded.setIndent(15)
        self._set_css(self.label_downloaded, CSS_LABEL_COLLECTION)

    def retranslateUi(self):
        self.label_collections.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#878787;\">COLLECTIONS</span></p></body></html>")
        self.toolButton_collection.setText("New Collection")
        self.label_downloaded.setText("<html><head/><body><p><span style=\" font-size:10pt; color:#878787;\">DOWNLOADED FEATURES</span></p></body></html>")

    def new_collection(self):
        n_coll = NewCollectionDialog()
        n_coll.exec_()

    def change_downloaded_text(self, name):
        self.label_downloaded.setText("<html><head/><body><p><span style=\" font-size:10pt; color:#878787;\">{0}</span></p></body></html>".format(name))
        self._set_label_downloaded()
        self.label_collections.setIndent(15)  # check it
        self.label_collections.setTextInteractionFlags(
            QtCore.Qt.NoTextInteraction)
        self._set_css(self.label_collections, CSS_LABEL_COLLECTION)


class DockWidgetContentsTop(QtGui.QWidget):
    """Contains the contents of the dock widget on the top side of the main
        window"""
    def __init__(self):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(2, 0, 4, 0)
        layout.setSpacing(5)  # check it

        spacer = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Fixed)
        layout.addItem(spacer)

        self.label_corpus = QtGui.QLabel(self)
        self._set_label_corpus()
        layout.addWidget(self.label_corpus)

        spacer2 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Expanding,
                                    QtGui.QSizePolicy.Fixed)
        layout.addItem(spacer2)

        self.label_username = QtGui.QLabel(self)
        self.label_username.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        layout.addWidget(self.label_username)

        self.line = QtGui.QFrame(self)
        self._set_line()
        layout.addWidget(self.line)

        self.label_status = QtGui.QLabel(self)
        self._set_labelstatus()
        layout.addWidget(self.label_status)
        self.retranslate_ui()

    def _set_label_corpus(self):
        """Sets the label"""
        font = QtGui.QFont()
        font.setFamily("Garuda")
        self.label_corpus.setFont(font)
        sizepolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding)
        #sizepolicy.setHorizontalStretch(0)
        #sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(
            self.label_corpus.sizePolicy().hasHeightForWidth())
        self.label_corpus.setSizePolicy(sizepolicy)
        self.label_corpus.setMinimumSize(QtCore.QSize(300, 30))
        self.label_corpus.setMaximumSize(QtCore.QSize(700, 30))

    def _set_line(self):
        """Vertical line between the status and username"""
        sizepolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(
            self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizepolicy)
        self.line.setMinimumSize(QtCore.QSize(0, 20))
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)

    def _set_labelstatus(self):
        """Sets the size policy of label status"""
        sizepolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(
            self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(sizepolicy)

    def retranslate_ui(self):
        self.label_username.setText("<html><head/><body><p align=\"right\"><span style=\" font-weight:600; color:#7c7c7c;\">user.name</span></p></body></html>")
        self.label_status.setText('<html><head/><body><p><span style=" font-size:10pt; color:#73ff7c;">online</span></p></body></html>')
        self.label_corpus.setText('<html><head/><body><p align="center"><span style=" font-size:15pt; color:#C1C1C1;">CORPUS</span></p></body></html>')
