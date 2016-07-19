from PyQt4 import QtGui


def sort_dictionary(dictionary, key):
    """sorts the given dictionary according to the keys"""
    dictionary = sorted(dictionary, key=lambda k: k[key])
    return dictionary


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
