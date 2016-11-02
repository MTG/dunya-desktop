import os
import os.path
import json

import compmusic.dunya.makam
from compmusic.dunya.docserver import document, get_document_as_json
from PyQt4 import QtCore


def sort_dictionary(dictionary, key):
    """sorts the given dictionary according to the keys"""
    return sorted(dictionary, key=lambda k: k[key])

def get_attributes():
    makams = compmusic.dunya.makam.get_makams()
    makams = sort_dictionary(makams, 'name')

    forms = compmusic.dunya.makam.get_forms()
    forms = sort_dictionary(forms, 'name')

    usuls = compmusic.dunya.makam.get_usuls()
    usuls = sort_dictionary(usuls, 'name')

    composers = compmusic.dunya.makam.get_composers()
    composers = sort_dictionary(composers, 'name')

    performers = compmusic.dunya.makam.get_artists()
    performers = sort_dictionary(performers, 'name')

    instruments = compmusic.dunya.makam.get_instruments()
    instruments = sort_dictionary(instruments, 'name')

    return makams, forms, usuls, composers, performers, instruments


class FeatureDownloaderThread(QtCore.QThread):
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

            features = document(self.docid)['derivedfiles']
            for thetype in features:
                for subtype in features[thetype]:
                    feature_path = os.path.join(DOC_FOLDER, thetype + '--'
                                                + subtype + '.json')
                    if not os.path.exists(feature_path):
                        try:
                            feature = get_document_as_json(self.docid, thetype,
                                                           subtype)
                            if feature:
                                json.dump(feature, open(feature_path, 'w'))
                        except:
                            pass