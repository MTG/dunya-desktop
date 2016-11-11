import os
import platform

from PyQt4 import QtGui, QtCore

from combobox import ComboBox

# platform dependent margins/spacings
if platform.system() == 'Linux':
    MARGIN = 2
    SPACING = 3
    SPACE = 3
else:  # now, only for mac
    MARGIN = 5
    SPACING = 5
    SPACE = 7

# css paths
QUERY_ICON = ":/compmusic/icons/magnifying-glass.png"
CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                        'audioattframe.css')
CSS_BUTTON = os.path.join(os.path.dirname(__file__), '..', 'ui_files', 'css',
                          'toolbutton.css')


class AudioAttFrame(QtGui.QFrame):
    """Frame contains the comboboxes of attributes (such as makams, forms,
    etc) and query button"""

    def __init__(self, QWidget_parent=None):
        QtGui.QFrame.__init__(self, QWidget_parent)

        self._set_size_attributes()

        layout = QtGui.QGridLayout(self)
        self._set_layout(layout)
        self._retranslate_status_tips()

        if platform.system() != 'Linux':
            self._set_css(self, CSS_PATH)
        self._set_css(self.toolButton_query, CSS_BUTTON)
        self.toolButton_query.setDisabled(True)

        # signals
        self.comboBox_melodic.currentIndexChanged.connect(self.set_toolbutton)
        self.comboBox_form.currentIndexChanged.connect(self.set_toolbutton)
        self.comboBox_rhythm.currentIndexChanged.connect(self.set_toolbutton)
        self.comboBox_composer.currentIndexChanged.connect(self.set_toolbutton)
        self.comboBox_performer.currentIndexChanged.connect(
            self.set_toolbutton)
        self.comboBox_instrument.currentIndexChanged.connect(
            self.set_toolbutton)

    def _set_size_attributes(self):
        """Sets the size policies of frame"""
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                        QtGui.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameShadow(QtGui.QFrame.Raised)
        self.setLineWidth(1)

    def _set_layout(self, layout):
        """Sets the size policies of layout and initializes the comoboxes and
        query button."""
        layout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        layout.setMargin(MARGIN)
        layout.setSpacing(SPACING)

        # combo boxes
        # melodic structure
        self.comboBox_melodic = ComboBox(self)
        layout.addWidget(self.comboBox_melodic, 0, 0, 1, 1)

        # form structure
        self.comboBox_form = ComboBox(self)
        layout.addWidget(self.comboBox_form, 0, 2, 1, 1)

        # rhythmic structure
        self.comboBox_rhythm = ComboBox(self)
        layout.addWidget(self.comboBox_rhythm, 0, 4, 1, 1)

        # composer
        self.comboBox_composer = ComboBox(self)
        layout.addWidget(self.comboBox_composer, 1, 0, 1, 1)
        self.comboBox_composer.set_placeholder_text('Composer')

        # performer
        self.comboBox_performer = ComboBox(self)
        layout.addWidget(self.comboBox_performer, 1, 2, 1, 1)
        self.comboBox_performer.set_placeholder_text('Performer')

        # instrument
        self.comboBox_instrument = ComboBox(self)
        layout.addWidget(self.comboBox_instrument, 1, 4, 1, 1)
        self.comboBox_instrument.set_placeholder_text('Instrument')

        # spacers between the comboboxes
        spacer_item1 = QtGui.QSpacerItem(SPACE, 20, QtGui.QSizePolicy.Minimum,
                                         QtGui.QSizePolicy.Fixed)

        spacer_item2 = QtGui.QSpacerItem(SPACE, 20, QtGui.QSizePolicy.Minimum,
                                         QtGui.QSizePolicy.Fixed)

        if platform.system() != 'Linux':
            spacer_item3 = QtGui.QSpacerItem(SPACE, 20,
                                             QtGui.QSizePolicy.Minimum,
                                             QtGui.QSizePolicy.Fixed)
            layout.addItem(spacer_item3, 1, 5, 1, 1)

        layout.addItem(spacer_item1, 1, 1, 1, 1)
        layout.addItem(spacer_item2, 1, 3, 1, 1)

        # query button and layout
        self.horizontalLayout_query = QtGui.QHBoxLayout()
        self.horizontalLayout_query.setSpacing(0)

        self.toolButton_query = QtGui.QToolButton(self)
        self.toolButton_query.setFixedSize(QtCore.QSize(50, 50))
        icon_query = QtGui.QIcon()
        icon_query.addPixmap(QtGui.QPixmap(QUERY_ICON),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_query.setIcon(icon_query)
        self.toolButton_query.setIconSize(QtCore.QSize(25, 25))
        self.horizontalLayout_query.addWidget(self.toolButton_query)
        layout.addLayout(self.horizontalLayout_query, 0, 6, 2, 1)

    def _retranslate_status_tips(self):
        """Sets the status tips of comboboxes and query button"""
        self.comboBox_melodic.setStatusTip("Select melodic attribute")
        self.comboBox_form.setStatusTip("Select form attribute")
        self.comboBox_rhythm.setStatusTip("Select rhythm attribute")
        self.comboBox_composer.setStatusTip("Select composer")
        self.comboBox_performer.setStatusTip("Select performer")
        self.comboBox_instrument.setStatusTip("Select instrument")

        self.toolButton_query.setStatusTip("Query your selection")

    def set_toolbutton(self):
        """Checks the comboboxes and enables/disables the query button"""
        index_melodic = self.comboBox_melodic.currentIndex()
        index_form = self.comboBox_form.currentIndex()
        index_rhythm = self.comboBox_rhythm.currentIndex()
        index_composer = self.comboBox_composer.currentIndex()
        index_performer = self.comboBox_performer.currentIndex()
        index_instrument = self.comboBox_instrument.currentIndex()

        if index_melodic is -1 and index_form is -1 and index_rhythm is -1 \
                and index_composer is -1 and index_performer is -1 and \
                        index_instrument is -1:
            self.toolButton_query.setDisabled(True)
        else:
            self.toolButton_query.setEnabled(True)

    @staticmethod
    def _set_css(obj, css_path):
        """Sets the css"""
        with open(css_path) as f:
            css = f.read()
        obj.setStyleSheet(css)
