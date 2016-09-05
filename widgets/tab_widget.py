from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class TabWidget(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.set_font()
        self.set_css()

    def set_font(self):
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)

    def set_css(self):
        with open("../ui_files/css/tabwidget.css") as f:
            css = f.read()
        self.setStyleSheet(css)


class TabWidgetMakam(TabWidget):
    def __init__(self, parent=None):
        super(TabWidgetMakam, self).__init__(parent)
        self.add_tabs()

    def add_tabs(self):
        # score tab
        self.tab_score = QtGui.QWidget()
        self.addTab(self.tab_score, _fromUtf8(""))

        # audio tab
        self.tab_audio = QtGui.QWidget()
        self.addTab(self.tab_audio, _fromUtf8(""))
