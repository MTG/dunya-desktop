import os
import os.path
import json
import fnmatch
import urllib

from compmusic.dunya.makam import (get_makams, get_forms, get_usuls,
                                   get_composers, get_artists, get_instruments)
from compmusic.dunya.docserver import (document, get_document_as_json, get_mp3)
from compmusic.dunya.conn import HTTPError
from PyQt5.QtCore import QObject, QThread, pyqtSignal

FOLDER = os.path.join(os.path.dirname(__file__), '..', 'documents')


def is_dunya_up():
    try:
        status = urllib.urlopen("http://dunya.compmusic.upf.edu/").getcode()
        if not status is 200:
            return False
        else:
            return True
    except IOError:
        return False

def get_filenames_in_dir(dir_name, keyword='*.mp3', skip_foldername='',
                         match_case=True, verbose=None):
    names = []
    folders = []
    fullnames = []

    if verbose:
        print(dir_name)

    # check if the folder exists
    if not os.path.isdir(dir_name):
        if verbose:
            print("> Directory doesn't exist!")
        return [], [], []

    # if the dir_name finishes with the file separator,
    # remove it so os.walk works properly
    dir_name = dir_name[:-1] if dir_name[-1] == os.sep else dir_name

    # walk all the subdirectories
    for (path, dirs, files) in os.walk(dir_name):
        for f in files:
            has_key = (fnmatch.fnmatch(f, keyword) if match_case else
                       fnmatch.fnmatch(f.lower(), keyword.lower()))
            if has_key and skip_foldername not in path.split(os.sep)[1:]:
                try:
                    folders.append(unicode(path, 'utf-8'))
                except TypeError:  # already unicode
                    folders.append(path)
                try:
                    names.append(unicode(f, 'utf-8'))
                except TypeError:  # already unicode
                    names.append(path)
                fullnames.append(os.path.join(path, f))

    if verbose:
        print("> Found " + str(len(names)) + " files.")
    return fullnames, folders, names


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


class ResultObj(QObject):
    def __init__(self, docid, step, n_progress):
        QObject.__init__(self)

        self.docid = docid
        self.step = step
        self.n_progress = n_progress


class DocThread(QThread):
    """Downloads the available features from Dunya-backend related with the
    given docid"""

    FOLDER = os.path.join(os.path.dirname(__file__), '..', 'documents')
    step_completed = pyqtSignal(object)

    # checking existance of documents folder in culture
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    def __init__(self, queue, callback, parent=None):
        QThread.__init__(self, parent)
        self.queue = queue
        self.step_completed.connect(callback)

    def run(self):
        while True:
            arg = self.queue.get()
            if arg is None:
                return
            self.download(arg)

    def download(self, docid):
        if docid:
            doc_folder = os.path.join(self.FOLDER, docid)
            if not os.path.exists(doc_folder):
                os.makedirs(doc_folder)

            # feature list
            try:
                features = document(docid)['derivedfiles']
            except HTTPError:
                print(docid, 'is not found')
                return

            try:
                m_path = os.path.join(doc_folder, docid + '.mp3')
                if not os.path.exists(m_path):
                    # for now, all tokens have permission to download
                    # audio files
                    mp3 = get_mp3(docid)
                    open(m_path, 'w').write(mp3)
            except:
                pass

            num_f = (sum([len(features[key]) for key in ['audioanalysis',
                                                         'jointanalysis']]))

            count = 0
            for thetype in ['audioanalysis', 'jointanalysis']:
                for subtype in features[thetype]:
                    f_path = os.path.join(doc_folder,
                                          thetype + '--' + subtype + '.json')
                    if not os.path.exists(f_path):
                        try:
                            feature = get_document_as_json(docid, thetype,
                                                           subtype)
                            if feature:
                                json.dump(feature, open(f_path, 'w'))
                        except:
                            pass
                    count += 1
                    self.step_completed.emit(ResultObj(docid, count, num_f))


def check_doc(docid):
    """Checks if all the features are downloaded correctly or not"""
    docid = str(docid)
    if os.path.exists(os.path.join(FOLDER, docid)):
        docid = str(docid)
        fullnames, folders, names = \
            get_filenames_in_dir(os.path.join(FOLDER, docid), '*.json')

        features = {}
        for name in names:
            try:
                features[name.split('--')[0]].append(name.split('--')[1])
            except KeyError:
                features[name.split('--')[0]] = []
                features[name.split('--')[0]].append(name.split('--')[1])

        try:
            num_features = sum([len(features[key]) for key in features])
            if num_features == 10 or num_features == 22:
                return True
            else:
                return False
        except:
            return False
    else:
        return False
