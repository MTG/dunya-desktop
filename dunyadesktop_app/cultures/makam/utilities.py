import os
import os.path
import json

from compmusic.dunya.makam import (get_makams, get_forms, get_usuls,
                                   get_composers, get_artists, get_instruments)
from compmusic.dunya.docserver import (document, get_document_as_json)
from PyQt4 import QtCore


def sort_dictionary(dictionary, key):
    """sorts the given dictionary according to the keys"""
    return sorted(dictionary, key=lambda k: k[key])


def get_attributes():
    """Downloads the attributes"""
    makams = get_makams()
    makams = sort_dictionary(makams, 'name')

    forms = get_forms()
    forms = sort_dictionary(forms, 'name')

    usuls = get_usuls()
    usuls = sort_dictionary(usuls, 'name')

    composers = get_composers()
    composers = sort_dictionary(composers, 'name')

    performers = get_artists()
    performers = sort_dictionary(performers, 'name')

    instruments = get_instruments()
    instruments = sort_dictionary(instruments, 'name')

    return makams, forms, usuls, composers, performers, instruments


class DocThread(QtCore.QThread):
    """Downloads the available features from Dunya-backend related with the
    given docid"""

    FOLDER = os.path.join(os.path.dirname(__file__), '..', 'documents')
    feautures_downloaded = QtCore.pyqtSignal(dict, dict)

    # checking existance of documents folder in culture
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.docid = ''

    def run(self):
        if self.docid:
            DOC_FOLDER = os.path.join(self.FOLDER, self.docid)
            if not os.path.exists(DOC_FOLDER):
                os.makedirs(DOC_FOLDER)

            # feature list
            features = document(self.docid)['derivedfiles']
            for thetype in features:
                for subtype in features[thetype]:
                    f_path = os.path.join(DOC_FOLDER, thetype + '--' + subtype
                                          + '.json')
                    if not os.path.exists(f_path):
                        try:
                            feature = get_document_as_json(self.docid, thetype,
                                                           subtype)
                            if feature:
                                json.dump(feature, open(f_path, 'w'))
                        except:
                            pass
