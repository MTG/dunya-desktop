from PyQt4 import QtGui, QtCore


class PlayerFrame(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent=parent)

        self._set_size_policy()
        self._set_visualization()

        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.setMaximumHeight(40)

        self.toolbutton_play = QtGui.QToolButton(self)
        self.toolbutton_pause = QtGui.QToolButton(self)
        self._set_buttons()

        self.slider = QtGui.QSlider(self)
        self._set_slider()

    def _set_size_policy(self):
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

    def _set_visualization(self):
        self.setStyleSheet("QFrame{\n"
                                        "border: 0.5px solid white;\n"
                                        "border-radius: 4px;\n"
                                        "padding: 2px;\n"
                                        "background-color: rgb(25, 25,25);\n"
                                        "}")

        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameShadow(QtGui.QFrame.Raised)

    def _set_buttons(self):
        self.toolbutton_play.setMinimumSize(QtCore.QSize(50, 15))
        self.toolbutton_play.setStyleSheet("QToolButton {\n"
                                           "border: none;\n"
                                           "background: transparent;\n"
                                           "}\n"
                                           "\n"
                                           "")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/compmusic/icons/play.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolbutton_play.setIcon(icon)
        self.toolbutton_play.setIconSize(QtCore.QSize(20, 20))
        self.toolbutton_play.setObjectName("toolButton_play")
        self.horizontalLayout.addWidget(self.toolbutton_play)

        self.toolbutton_pause.setMinimumSize(QtCore.QSize(50, 15))
        self.toolbutton_pause.setStyleSheet("QToolButton {\n"
                                            "border: none;\n"
                                            "background: transparent;\n"
                                            "}\n"
                                            "")

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/compmusic/icons/pause.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolbutton_pause.setIcon(icon1)
        self.toolbutton_pause.setIconSize(QtCore.QSize(20, 20))
        self.horizontalLayout.addWidget(self.toolbutton_pause)

    def _set_slider(self):
        self.slider.setStyleSheet(
            "QSlider::groove:horizontal {\n"
            "border: 1px solid #999999;\n"
            "height: 2px;"
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);\n"
            "margin: 2px 0;\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal {\n"
            "background: solid black;\n"
            "border: 1px solid black;\n"
            "width: 5px;\n"
            "margin: -2px 0;"
            "border-radius: 3px;\n"
            "}")

        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalLayout.addWidget(self.slider)
