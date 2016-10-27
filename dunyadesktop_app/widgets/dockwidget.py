import os

from PyQt4 import QtGui, QtCore

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
                            'css', 'listview.css')

CSS_TOOLBUTTON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                              'css', 'toolbutton_collection.css')

CSS_TABLEVIEW_DOWNLOADED = os.path.join(os.path.dirname(__file__), '..',
                                        'ui_files', 'css',
                                        'tableview_downloaded.css')


class DockWidget(QtGui.QDockWidget):
    def __init__(self, min_width, min_height, max_width, max_height):
        QtGui.QDockWidget.__init__(self)
        self._set_dockwidget(min_width, min_height, max_width, max_height)

    def _set_dockwidget(self, min_width, min_height, max_width, max_height):
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
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self._set_widget()
        #self._set_css(self, CSS_DOCKWIDGET)

        self.vertical_layout = QtGui.QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(4, 0, 0, 0)
        self.vertical_layout.setSpacing(0)  # check it

        self.frame_collection = QtGui.QFrame(self)
        self._set_frame()

        self.vertical_layout3 = QtGui.QVBoxLayout(self.frame_collection)
        self.vertical_layout3.setContentsMargins(2, 5, 3, 2)
        self.vertical_layout3.setSpacing(7)  # check it

        self.label_collections = QtGui.QLabel(self.frame_collection)
        self.label_collections.setIndent(15)  # check it
        self.label_collections.setTextInteractionFlags(
            QtCore.Qt.NoTextInteraction)
        self._set_css(self.label_collections, CSS_LABEL_COLLECTION)
        self.vertical_layout3.addWidget(self.label_collections)

        # listview (seperate it)
        self.listView_collections = QtGui.QListView(self.frame_collection)
        self._set_css(self.listView_collections, CSS_LISTVIEW)
        self.listView_collections.setViewMode(QtGui.QListView.ListMode)
        self.vertical_layout3.addWidget(self.listView_collections)
        self.vertical_layout.addWidget(self.frame_collection)

        # toolbutton
        self.toolButton_collection = QtGui.QToolButton(self)
        self._set_toolbutton()
        self.vertical_layout.addWidget(self.toolButton_collection)

        self.frame_downloaded = QtGui.QFrame(self)
        self._set_frame_downloaded()

        self.vertical_layout4 = QtGui.QVBoxLayout(self.frame_downloaded)
        self.vertical_layout4.setContentsMargins(3, 5, 3, 2)
        self.label_downloaded = QtGui.QLabel(self.frame_downloaded)
        self._set_label_downloaded()
        self.vertical_layout4.addWidget(self.label_downloaded)

        self.tableView_downloaded = QtGui.QTableView(self.frame_downloaded)
        self._set_css(self.tableView_downloaded, CSS_TABLEVIEW_DOWNLOADED)
        self.vertical_layout4.addWidget(self.tableView_downloaded)
        self.vertical_layout.addWidget(self.frame_downloaded)
        self.retranslateUi()

    def _set_widget(self):
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


class DockWidgetContentsTop(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.horizontal_layout = QtGui.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(2, 0, 4, 0)
        self.horizontal_layout.setSpacing(5)  # check it

        spacer = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Fixed)

        self.horizontal_layout.addItem(spacer)

        self.label_corpus = QtGui.QLabel(self)
        self._set_label_corpus()
        self.horizontal_layout.addWidget(self.label_corpus)

        spacer2 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Expanding,
                                    QtGui.QSizePolicy.Fixed)
        self.horizontal_layout.addItem(spacer2)

        self.label_username = QtGui.QLabel(self)
        self.label_username.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.horizontal_layout.addWidget(self.label_username)

        self.line = QtGui.QFrame(self)
        self._set_line()
        self.horizontal_layout.addWidget(self.line)

        self.label_status = QtGui.QLabel(self)
        self._set_labelstatus()
        self.horizontal_layout.addWidget(self.label_status)
        self.retranslateUi()

    def _set_label_corpus(self):
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
        sizepolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        sizepolicy.setHorizontalStretch(0)
        sizepolicy.setVerticalStretch(0)
        sizepolicy.setHeightForWidth(
            self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(sizepolicy)

    def retranslateUi(self):
        self.label_username.setText("<html><head/><body><p align=\"right\"><span style=\" font-weight:600; color:#7c7c7c;\">user.name</span></p></body></html>")
        self.label_status.setText('<html><head/><body><p><span style=" font-size:10pt; color:#73ff7c;">online</span></p></body></html>')
        self.label_corpus.setText('<html><head/><body><p align="center"><span style=" font-size:15pt; color:#C1C1C1;">CORPUS</span></p></body></html>')
