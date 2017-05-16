import os
import platform
import json
import sys

from PyQt5.QtWidgets import (QToolButton, QTableView, QAbstractItemView,
                             QAction, QHeaderView, QTableWidget, QDialog,
                             QTableWidgetItem, QLabel, QPushButton, qApp,
                             QVBoxLayout, QLineEdit)
from PyQt5.QtCore import pyqtSignal, Qt, QPersistentModelIndex, QSize
from PyQt5.QtGui import QFont, QCursor, QIcon, QPixmap

from utilities import database, corpusbasestatistics
from cultures.makam import utilities as makam_utilities
from widgets.playerframe import load_pd, load_tonic
from .progressbar import ProgressBar
from .contextmenu import RCMenu
from .widgetutilities import set_css, convert_str
from .models.recordingmodel import CollectionTableModel
from .models.proxymodel import SortFilterProxyModel


if platform.system() == 'Linux':
    FONT_SIZE = 9
else:
    FONT_SIZE = 12


DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'cultures',
                         'documents')
DUNYA_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'dunya.svg')
CHECK_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'tick-inside-circle.svg')
QUEUE_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                          'icons', 'add-to-queue-button.svg')
DOWNLOAD_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                             'icons', 'download.svg')
COMPMUSIC_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                              'icons', 'compmusic_white.png')
PLAY_ICON = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                              'icons', 'playback', 'play-button_gray.svg')
CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files',
                        'style.qss')


class DownloadButton(QToolButton):
    def __init__(self, parent=None):
        QToolButton.__init__(self, parent)
        # self.clicked.connect(self.download_clicked)

    def download_clicked(self):
        pass
        # print('clicked')
        # print(self.parent())
        # print(self.parent().pos())


class TableView(QTableView):
    open_dunya_triggered = pyqtSignal(object)
    add_to_collection = pyqtSignal(str, object)

    def __init__(self, *__args):
        QTableView.__init__(self, *__args)

        # setting the table for no edit and row selection
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setMouseTracking(True)
        self.horizontalHeader().setStretchLastSection(True)
        font = QFont()
        font.setPointSize(13)
        self.horizontalHeader().setFont(font)

        # hiding the vertical headers
        self.verticalHeader().hide()

        # arranging the artist column for being multi-line
        self.setWordWrap(True)
        self.setTextElideMode(Qt.ElideMiddle)

        self._last_index = QPersistentModelIndex()
        self.viewport().installEventFilter(self)

        self._set_font()

    def _set_font(self):
        """Sets the font of the table"""
        font = QFont()
        font.setPointSize(FONT_SIZE)
        self.setFont(font)

    def contextMenuEvent(self, event):
        """Pops up the context menu when the right button is clicked."""
        try:
            if self.selectionModel().selection().indexes():
                for index in self.selectionModel().selection().indexes():
                    row, column = index.row(), index.column()
            self.index = index

            menu = RCMenu(self)
            menu.popup(QCursor.pos())

            self.selected_indexes = menu.return_selected_row_indexes()
            menu.overall_hist_action.triggered.connect(
                self._compute_overall_histograms)
        except UnboundLocalError:
            pass

    def _compute_overall_histograms(self):
        coll_widget =  self.parent().parent().listView_collections
        coll = str(coll_widget.currentItem().text())

        conn, c = database.connect()
        histograms = {}
        for row in self.selected_indexes:
            mbid = str(database.get_nth_row(c, coll, row)[0])
            pd_path = os.path.join(DOCS_PATH, mbid,
                                   'audioanalysis--pitch_distribution.json')
            tnc_path = os.path.join(DOCS_PATH, mbid,
                                   'audioanalysis--tonic.json')
            vals, bins = load_pd(pd_path)
            tonic = load_tonic(tnc_path)
            histograms[mbid] = [[vals, bins], tonic]
        corpusbasestatistics.compute_overall_histogram(histograms)

    def send_rec(self):
        """Emits 'open_dunya_triggered' signal and the current index to open
        the player"""
        if self.index:
            self.open_dunya_triggered.emit(self.index)
            self.index = None

    def get_selected_rows(self):
        """Returns the current selected rows in the table."""
        selected_rows = []
        for item in self.selectionModel().selectedRows():
            if item.row() not in selected_rows:
                selected_rows.append(item)
        return selected_rows

    def send_to_db(self, coll):
        """Emits 'add_to_collection' signal to add the selected rows to the
        database"""
        if self.index:
            self.add_to_collection.emit(coll, self.index)
            self.index = None


class TableViewResults(TableView):
    """Table view widget of query results."""

    def __init__(self, parent=None):
        TableView.__init__(self)
        self.setSortingEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)

        self.horizontal_header = self.horizontalHeader()
        self._set_horizontal_header()

        self.add_maincoll = QAction("Add to main collection", self)
        self.setColumnWidth(0, 10)

        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def _set_menu(self):
        self.add_maincoll = QAction("Add to main collection", self)

        self.menu.addSeparator()

        self.open_dunya = QAction("Open on Player", self)
        self.open_dunya.setIcon(QIcon(DUNYA_ICON))

    def _set_horizontal_header(self):
        self.horizontal_header.setStretchLastSection(True)
        self.horizontal_header.hide()
        self.horizontal_header.setResizeMode(QHeaderView.Fixed)


class TableViewCollections(TableView):
    def __index__(self, parent=None):
        TableView.__init__(self)
        self.setSortingEnabled(True)
        self.setDragDropMode(QAbstractItemView.NoDragDrop)

        self.horizontal_header = self.horizontalHeader()
        self.setSelectionMode(QAbstractItemView.SingleSelection)


class TableWidget(QTableWidget, TableView):
    added_new_doc = pyqtSignal(list)
    open_dunya_triggered = pyqtSignal(object)
    set_result_checked = pyqtSignal(str)

    def __init__(self):
        QTableWidget.__init__(self)
        TableView.__init__(self)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)

        self._set_columns()
        self.setDisabled(True)

        self.recordings = []
        self.indexes = {}
        self.coll = ''

    def _set_columns(self):
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Status', 'Title'])
        self.horizontalHeader().setResizeMode(QHeaderView.Fixed)

    def dropMimeData(self, p_int, p_int_1, QMimeData, Qt_DropAction):
        self.last_drop_row = p_int
        return True
        # self.last_drop_row = self.rowCount()
        # return True

    def dropEvent(self, event):
        # The QTableWidget from which selected rows will be moved
        sender = event.source()

        # Default dropEvent method fires dropMimeData with appropriate
        # parameters (we're interested in the row index).
        super(QTableWidget, self).dropEvent(event)
        # Now we know where to insert selected row(s)
        drop_row = self.last_drop_row
        selected_rows = sender.get_selected_rows()

        selected_rows_index = [item.row() for item in selected_rows]

        # if sender == receiver (self), after creating new empty rows selected
        # rows might change their locations
        sel_rows_offsets = [0 if self != sender or srow < drop_row
                            else len(selected_rows_index) for srow in
                            selected_rows_index]
        selected_rows_index = [row + offset for row, offset
                               in zip(selected_rows_index, sel_rows_offsets)]

        # copy content of selected rows into empty ones
        docs = []
        conn, c = database.connect()
        for i, srow in enumerate(selected_rows):
            source_index = sender.model().mapToSource(srow)
            if database.add_doc_to_coll(
                    conn, c, self.recordings[source_index.row()], self.coll):
                # index in the source model
                index = sender.model().mapToSource(selected_rows[i])
                # item in the source model
                item = sender.model().sourceModel().item(index.row(), 1)

                if item:
                    self.add_item(item.text())

                    docs.append(self.recordings[source_index.row()])
                    self.indexes[self.recordings[source_index.row()]] = \
                        self.rowCount() - 1
                    # sender.model().sourceModel().set_checked(
                    # [selected_rows_index[i]])
        if docs:
            self.added_new_doc.emit(docs)
        event.accept()

    def add_item(self, text):
        self.insertRow(self.rowCount())
        self.set_status(self.rowCount() - 1, 0)
        source = QTableWidgetItem(text)
        self.setItem(self.rowCount() - 1, 1, source)

    def create_table(self, coll):
        # first cleans the table, sets the columns and enables the widget
        self.setRowCount(0)

        self._set_columns()
        self.setEnabled(True)

        for i, item in enumerate(coll):
            set_check = False
            path = os.path.join(DOCS_PATH, item,
                                'audioanalysis--metadata.json')

            if makam_utilities.check_doc(item):
                metadata = json.load(open(path))
                cell = QTableWidgetItem(metadata['title'])
                set_check = 1
            else:
                print("Needs to be downloaded {0}".format(item))
                cell = QTableWidgetItem(item)

            self.insertRow(self.rowCount())
            self.setItem(i, 1, cell)
            self.setColumnWidth(0, 60)

            if set_check is 1:
                self.set_status(self.rowCount()-1, 1)
            else:
                self.set_status(self.rowCount()-1, 2)

    def set_progress_bar(self, status):
        docid = status.docid
        step = status.step
        n_progress = status.n_progress

        self.setCellWidget(self.indexes[docid], 0, ProgressBar(self))
        progress_bar = self.cellWidget(self.indexes[docid], 0)

        if progress_bar:
            if not step == n_progress:
                progress_bar.update_progress_bar(step, n_progress)
            else:
                self.set_status(self.indexes[docid], 1)
                self.refresh_row(docid)

    def set_status(self, raw, exist=None):
        item = QLabel()
        item.setAlignment(Qt.AlignCenter)

        if exist is 0:
            icon = QPixmap(QUEUE_ICON).scaled(20, 20, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)
            item.setPixmap(icon)
            item.setToolTip('Waiting in the download queue...')

        if exist is 1:
            icon = QPixmap(CHECK_ICON).scaled(20, 20, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)
            item.setPixmap(icon)
            item.setToolTip('All the features are downloaded...')

        if exist is 2:
            item = QPushButton(self)
            item.setToolTip('Download')
            item.setIcon(QIcon(DOWNLOAD_ICON))
            item.clicked.connect(self.download_clicked)

        self.setCellWidget(raw, 0, item)

    def download_clicked(self):
        click_me = qApp.focusWidget()
        index = self.indexAt(click_me.pos())
        if index.isValid():
            row = index.row()
            if sys.version_info[0] == 2:
                docid = convert_str(self.item(row, 1).text())
            else:
                docid = self.item(row, 1).text()

            self.set_status(row, 0)
            self.indexes[docid] = row
            self.added_new_doc.emit([docid])

    def refresh_row(self, docid):
        """checks the status and the title columns of given row"""
        row = self.indexes[docid]
        if self.item(row, 1):
            if makam_utilities.check_doc(docid):
                self.set_status(row, exist=1)

                title = json.load(open(os.path.join(
                    DOCS_PATH, docid,
                    'audioanalysis--metadata.json')))['title']
                item = QTableWidgetItem(title)
                self.setItem(row, 1, item)
                self.set_result_checked.emit(docid)
            else:
                self.set_status(row, 2)


class DialogCollTable(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent=parent)
        self.setMinimumSize(QSize(1200, 600))
        layout = QVBoxLayout(self)

        self.label_collection = QLabel()
        self.label_collection.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_collection)

        self.lineedit_filter = QLineEdit(self)
        layout.addWidget(self.lineedit_filter)

        self.coll_table = TableViewCollections(self)
        layout.addWidget(self.coll_table)

        self.model = CollectionTableModel()

        self.proxy_model = SortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(-1)

        self.coll_table.setModel(self.proxy_model)

        # signals
        self.lineedit_filter.textChanged.connect(self._lineedit_changed)

    def _lineedit_changed(self):
        self.proxy_model.filter_table(self.lineedit_filter.text())

    def _set_line_edit(self):
        self.lineedit_filter.setPlaceholderText('Type here to filter')

    def closeEvent(self, QCloseEvent):
        self.model.clear_items()


class TablePlaylist(TableWidget, TableViewCollections):

    def __init__(self):
        TableWidget.__init__(self)
        TableViewCollections.__init__(self)
        self.setEnabled(True)
        self.setDragDropMode(QAbstractItemView.NoDragDrop)
        self._set_columns()
        set_css(self, CSS_PATH)
        self.items = {}

    def _set_columns(self):
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['', 'Title', 'Artists'])
        self.horizontalHeader().setResizeMode(QHeaderView.Fixed)

    def add_recordings(self, recording):
        for index, mbid in enumerate(recording):
            metadata = CollectionTableModel._get_metadata(self, mbid[0], index)
            self._add_item(metadata)

    def _add_item(self, metadata):
        self.insertRow(self.rowCount())

        # add play button
        play_button = QToolButton(self)
        play_button.setIcon(QIcon(PLAY_ICON))
        self.setCellWidget(self.rowCount()-1, 0, play_button)
        self.setItem(self.rowCount()-1, 1, self._make_item(metadata['title']))
        self.setItem(self.rowCount()-1, 2, self._make_item(metadata['artists']))

    def _make_item(self, text):
        return QTableWidgetItem(text)
