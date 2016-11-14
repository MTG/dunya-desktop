import os
import os.path
import json

from compmusic.dunya.makam import (get_makams, get_forms, get_usuls,
                                   get_composers, get_artists, get_instruments)
from compmusic.dunya.docserver import (document, get_document_as_json, get_mp3)
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
    steps = QtCore.pyqtSignal(int)
    step_completed = QtCore.pyqtSignal()
    feautures_downloaded = QtCore.pyqtSignal()

    # checking existance of documents folder in culture
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    def __init__(self, queue, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.queue = queue
        
    def run(self):
        while True:
            arg = self.queue.get()
            if arg is None:
                print('Shutting down')
                return 
            self.download(arg)
    
    def download(self, docid):
        if docid:
            DOC_FOLDER = os.path.join(self.FOLDER, docid)
            if not os.path.exists(DOC_FOLDER):
                os.makedirs(DOC_FOLDER)

            # feature list
            features = document(docid)['derivedfiles']
            try:
                m_path = os.path.join(DOC_FOLDER, docid + '.mp3')
                if not os.path.exists(m_path):
                    # for now, all tokens have permission to download
                    # audio files
                    mp3 = get_mp3(docid)
                    open(m_path, 'w').write(mp3)
            except:
                pass

            num_f = (sum([len(features[key]) for key in features]))
            self.steps.emit(num_f)

            for thetype in ['audioanalysis', 'jointanalysis']:
                for subtype in features[thetype]:
                    f_path = os.path.join(DOC_FOLDER, thetype + '--' + subtype
                                          + '.json')
                    if not os.path.exists(f_path):
                        try:
                            feature = get_document_as_json(docid, thetype,
                                                           subtype)
                            if feature:
                                json.dump(feature, open(f_path, 'w'))
                        except:
                            pass
                    self.step_completed.emit()
            self.feautures_downloaded.emit()
