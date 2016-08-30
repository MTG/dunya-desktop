from PyQt4 import QtGui


class ComboBox(QtGui.QComboBox):
    def __init__(self, attribute):

        QtGui.QComboBox.__init__(self)
        self.setEditable(True)
        self.setInsertPolicy(QtGui.QComboBox.NoInsert)

        self.attribute = attribute
        self.set_combobox()

    def set_combobox(self):
        """Add attributes to  combobox"""
        for element in self.attribute:
            self.addItem(element['name'])
            print element['name']
        self.setCurrentIndex(-1)

    def get_attribute_id(attribute, index):
        """Returns the mb id of the selected attributes"""
        if index is not -1:
            return attribute[index]['uuid']
        else:
            return -1