import sys
import os
import os.path
import json
import fnmatch

if sys.version_info[0] == 2:
    import urllib
else:
    import urllib.request as urllib

from ..dunya.makam import (get_makams, get_forms, get_usuls,
                                   get_composers, get_artists, get_instruments)
from ..dunya.docserver import (document, get_document_as_json, get_mp3)
from ..dunya.conn import HTTPError
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import numpy as np

FOLDER = os.path.join(os.path.dirname(__file__), '..', 'scores')


def has_symbtr(workid):
    print(workid)
    try:
        doc = document(workid)
        if 'score' in doc['derivedfiles'].keys():
            return True
        else:
            return False
    except HTTPError:
        return False


def is_dunya_up():
    try:
        status = urllib.urlopen("http://dunya.compmusic.upf.edu/").getcode()
        if status is not 200:
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
                    folders.append(str(path))
                except TypeError:  # already unicode
                    folders.append(path)
                try:
                    names.append(str(f))
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

    FOLDER = os.path.join(os.path.dirname(__file__), '..', 'scores')
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
            self.doc_folder = os.path.join(self.FOLDER, docid)
            if not os.path.exists(self.doc_folder):
                os.makedirs(self.doc_folder)

            # feature list
            try:
                features = document(docid)['derivedfiles']
            except HTTPError:
                print(docid, 'is not found')
                return

            if 'score' in features:
                self._download_score(docid)

            if 'scoreanalysis' in features:
                self._download_metadata(docid)

            if 'synthesis' in features:
                self._download_synthesis(docid)

            self.step_completed.emit(ResultObj(docid, 0, 0))

    def _download_synthesis(self, docid):
        parts = document(docid)['derivedfiles']['synthesis']['mp3']['numparts']
        for i in np.arange(1, parts + 1):
            mp3 = get_document_as_json(docid, 'synthesis', 'mp3', part=i)
            mp3_file = 'synthesis--' + str(i) + '.mp3'
            synthesis_path = os.path.join(self.doc_folder, mp3_file)
            open(synthesis_path, 'wb').write(mp3)

        onset_feature = get_document_as_json(docid, 'synthesis', 'onsets')
        onset_file = 'onsets.json'
        onset_path = os.path.join(self.doc_folder, onset_file)
        json.dump(onset_feature, open(onset_path, 'w'))

    def _download_metadata(self, docid):
        f_path = os.path.join(self.doc_folder, 'scoreanalysis--metadata.json')
        if not os.path.exists(f_path):
            try:
                feature = get_document_as_json(docid, 'scoreanalysis',
                                               'metadata')
                if feature:
                    json.dump(feature, open(f_path, 'w'), indent=4)
            except:
                pass

    def _download_score(self, docid):
        try:
            parts = \
                document(docid)['derivedfiles']['score']['score']['numparts']

            for i in np.arange(1, parts + 1):
                score = get_document_as_json(docid, 'score', 'score', part=i)
                score_file = 'scoresvg--' + str(i) + '.svg'
                score_path = os.path.join(self.doc_folder, score_file)
                open(score_path, 'w').write(score)
        except:
            pass


def check_doc(docid):
    """Checks if all the features are downloaded correctly or not"""
    docid = str(docid)
    score_folder = os.path.join(FOLDER, '..', 'scores', docid)
    if os.path.exists(score_folder):
        fullnames_mp3, folders, names = get_filenames_in_dir(score_folder,
                                                             '*.mp3')

        fullnames_svg, folders, names = get_filenames_in_dir(score_folder,
                                                             '*.svg')

        fullnames_json, folders, names = get_filenames_in_dir(score_folder,
                                                              '*.json')
        if fullnames_mp3 and fullnames_svg and fullnames_json:
            return True
        else:
            return False
    else:
        return False
