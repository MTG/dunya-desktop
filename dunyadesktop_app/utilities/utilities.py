from __future__ import absolute_import

from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _from_utf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


def sort_dictionary(dictionary, key):
    """sorts the given dictionary according to the keys"""
    return sorted(dictionary, key=lambda k: k[key])


def set_combobox(combobox, attribute):
    """Sets the given comboboxes"""
    combobox.setEditable(True)
    combobox.setInsertPolicy(QtGui.QComboBox.NoInsert)

    for elememt in attribute:
        combobox.addItem(elememt['name'])
    combobox.setCurrentIndex(-1)
    return combobox


def get_attribute_id(attribute, index):
    """Returns the mb id of the selected attributes"""
    if index is not -1:
        return attribute[index]['uuid']
    else:
        return -1


def get_attribute_id_other(attribute, index):
    """Returns the mb id of the selected attributes"""
    if index is not -1:
        return attribute[index]['mbid']
    else:
        return -1
