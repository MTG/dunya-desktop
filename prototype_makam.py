import compmusic.dunya.makam
import time
from PyQt4 import QtCore, QtGui


# setting the token
compmusic.dunya.conn.set_token('***REMOVED***')


class CheckableComboBox(QtGui.QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
            print "item is unchecked"
        else:
            item.setCheckState(QtCore.Qt.Checked)
            print "item is checked"


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        # table
        self.proxy_model = QtGui.QSortFilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)

        # group box
        self.group_box = QtGui.QGroupBox("Turkish-Makam Score Collection")

        # source view
        self.source_view = QtGui.QTreeView()
        self.source_view.setRootIsDecorated(False)
        self.source_view.setAlternatingRowColors(True)

        # sorting table
        self.proxy_view = QtGui.QTreeView()
        self.proxy_view.setRootIsDecorated(False)
        self.proxy_view.setAlternatingRowColors(True)
        self.proxy_view.setModel(self.proxy_model)
        self.proxy_view.setSortingEnabled(True)

        # line edit for filtering
        self.filter_makam_syntax_label = QtGui.QLabel("Filter &makam:")
        self.filter_pattern_line_edit = QtGui.QLineEdit()
        # label of line edit
        self.filter_pattern_label = QtGui.QLabel("Filter &title:")
        self.filter_pattern_label.setBuddy(self.filter_pattern_line_edit)

        # makam filtering menu
        self.filter_makam_toolbutton = QtGui.QToolButton(self)
        self.filter_makam_toolbutton.setText("Select makam")
        self.filter_makam_menu = QtGui.QMenu(self)

        # setting the filter
        self.set_makam_filter()
        self.filter_makam_syntax_label.setBuddy(self.filter_makam_toolbutton)

        '''
        # makam filtering combo box
        self.filter_makam_combo_box = CheckableComboBox()
        # fetches the makams from dunya
        self.set_makam_filter()
        self.filter_makam_syntax_label = QtGui.QLabel("Filter &makam:")
        self.filter_makam_syntax_label.setBuddy(self.filter_makam_combo_box)
        '''

        # form filtering combo box
        self.filter_form_combo_box = QtGui.QComboBox()
        # fetches the forms from dunya
        self.set_form_filter()
        self.filter_form_label = QtGui.QLabel("Filter &form:")
        self.filter_form_label.setBuddy(self.filter_form_combo_box)


        # usul filtering combo box
        self.filter_usul_combo_box = QtGui.QComboBox()
        # fetches the usuls from dunya
        self.set_usul_filter()
        self.filter_usul_label = QtGui.QLabel("Filter &usul:")
        self.filter_usul_label.setBuddy(self.filter_usul_combo_box)

        proxyLayout = QtGui.QGridLayout()
        proxyLayout.addWidget(self.filter_pattern_label, 0, 0)
        proxyLayout.addWidget(self.filter_pattern_line_edit, 0, 1, 1, 2)
        proxyLayout.addWidget(self.filter_makam_syntax_label, 1, 0)
        proxyLayout.addWidget(self.filter_makam_toolbutton, 1, 1, 1, 2)
        proxyLayout.addWidget(self.filter_form_label, 2, 0)
        proxyLayout.addWidget(self.filter_form_combo_box, 2, 1, 1, 2)
        proxyLayout.addWidget(self.filter_usul_label, 3, 0)
        proxyLayout.addWidget(self.filter_usul_combo_box, 3, 1, 1, 2)
        proxyLayout.addWidget(self.proxy_view, 5, 0, 1, 3)
        self.group_box.setLayout(proxyLayout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.group_box)
        self.setLayout(mainLayout)

        self.setWindowTitle("Turkish makam")
        self.resize(500, 450)

        self.proxy_view.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.filter_form_combo_box.setCurrentIndex(1)

    def set_makam_filter(self):

        # fetching makams from dunya
        makams = compmusic.dunya.makam.get_makams()

        for makam in makams:
            action = self.filter_makam_menu.addAction(makam['name'])
            action.setCheckable(True)

        self.filter_makam_toolbutton.setMenu(self.filter_makam_menu)
        self.filter_makam_toolbutton.setPopupMode(QtGui.QToolButton.InstantPopup)

        '''
        for xx, makam in enumerate(makams):
            self.filter_makam_combo_box.addItem(makam['name'])

            item = self.filter_makam_combo_box.model().item(xx, 0)
            item.setCheckState(QtCore.Qt.Unchecked)
        self.filter_makam_combo_box.model().sort(0)
        '''

    def set_form_filter(self):
        # fetching forms from dunya
        forms = compmusic.dunya.makam.get_forms()

        for form in forms:
            self.filter_form_combo_box.addItem(form['name'])
        self.filter_form_combo_box.addItem("ALL")
        self.filter_form_combo_box.model().sort(0)

    def set_usul_filter(self):
        # fetching forms from dunya
        usuls = compmusic.dunya.makam.get_usuls()

        for form in usuls:
            self.filter_usul_combo_box.addItem(form['name'])
        self.filter_usul_combo_box.addItem("ALL")
        self.filter_usul_combo_box.model().sort(0)

    def create_score_model(self):
        model = QtGui.QStandardItemModel(0, 2, parent)
        model.setHeaderData(0, QtCore.Qt.Horizontal, "Subject")

        return model

    def addMail(self, model, subject, sender, date):
        model.insertRow(0)
        model.setData(model.index(0, 0), subject)
        model.setData(model.index(0, 1), sender)
        model.setData(model.index(0, 2), date)

    def set_source_model(self, model):
        self.proxy_model.setSourceModel(model)
        self.source_view.setModel(model)


def add_score(model, title, composer):
    model.insertRow(0)
    model.setData(model.index(0, 0), title)
    model.setData(model.index(0, 1), composer)


def create_score_model(parent):
    model = QtGui.QStandardItemModel(0, 2, parent)

    model.setHeaderData(0, QtCore.Qt.Horizontal, "Title")
    model.setHeaderData(1, QtCore.Qt.Horizontal, "Composer")

    works = compmusic.dunya.makam.get_works()

    for work in works:
        if work['composers']:
            add_score(model, work['title'], work['composers'][0]['name'])

    return model

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.set_source_model(create_score_model(window))
    window.show()
    sys.exit(app.exec_())