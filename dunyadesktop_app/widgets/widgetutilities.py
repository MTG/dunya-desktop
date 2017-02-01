import copy
import json

import numpy as np
import os
from essentia.standard import MonoLoader

from cultures.makam import utilities
from widgets.playerframe import DOCS_PATH


def convert_str(string):
    return u''.join(string).encode('utf-8').strip()


def set_css(widget, css_path):
    try:
        with open(css_path) as f:
            css = f.read()
        widget.setStyleSheet(css)
    except IOError:
        pass


def downsample_plot(plot_array, ds_limit):
    # Decide by how much we should downsample
    ds = int(len(plot_array) / ds_limit) + 1

    if ds == 1:
        # Small enough to display with no intervention.
        return plot_array
    else:
        # Here convert data into a down-sampled array suitable for
        # visualizing. Must do this piecewise to limit memory usage.
        samples = 1 + (len(plot_array) // ds)
        visible = np.zeros(samples * 2, dtype=plot_array.dtype)
        source_ptr = 0
        target_ptr = 0

        # read data in chunks of ~1M samples
        chunk_size = (1000000 // ds) * ds
        while source_ptr < len(plot_array) - 1:
            chunk = plot_array[source_ptr:min(len(plot_array),
                                              source_ptr + chunk_size)]
            source_ptr += len(chunk)
            # reshape chunk to be integral multiple of ds
            chunk = chunk[:(len(chunk) // ds) * ds].reshape(len(chunk) // ds,
                                                            ds)
            # compute max and min
            chunk_max = chunk.max(axis=1)
            chunk_min = chunk.min(axis=1)

            # interleave min and max into plot data to preserve
            # envelope shape
            visible[target_ptr:target_ptr + chunk.shape[0] * 2:2] = chunk_min
            visible[1 + target_ptr:1 + target_ptr + chunk.shape[0] * 2:2] = \
                chunk_max
            target_ptr += chunk.shape[0] * 2
        plot_y = visible[:target_ptr]
        plot_y[-1] = np.nan

    return plot_y


def read_audio(audio_path):
    raw_audio = np.array(MonoLoader(filename=audio_path)())
    len_audio = len(raw_audio)
    min_audio = np.min(raw_audio)
    max_audio = np.min(raw_audio)
    return raw_audio, len_audio, min_audio, max_audio


def load_pitch(pitch_path):
    pitch_data = json.load(open(pitch_path))
    pp = np.array(pitch_data['pitch'])

    time_stamps = pp[:, 0]
    pitch_curve = pp[:, 1]
    pitch_plot = copy.copy(pitch_curve)
    pitch_plot[pitch_plot < 20] = np.nan

    samplerate = pitch_data['sampleRate']
    hopsize = pitch_data['hopSize']

    max_pitch = np.max(pitch_curve)
    min_pitch = np.min(pitch_curve)

    return time_stamps, pitch_plot, max_pitch, min_pitch, samplerate, hopsize


def load_pd(pd_path):
    pd = json.load(open(pd_path))
    vals = pd["vals"]
    bins = pd["bins"]
    return vals, bins


def load_tonic(tonic_path):
    tnc = json.load(open(tonic_path))
    try:
        return [tnc['value']]
    except KeyError:
        return [work['value'] for work in tnc.values()]


def get_feature_paths(recid):
    doc_folder = os.path.join(DOCS_PATH, recid)
    (full_names, folders, names) = \
        utilities.get_filenames_in_dir(dir_name=doc_folder, keyword='*.json')

    paths = {'audio_path': os.path.join(doc_folder, recid + '.mp3')}
    for xx, name in enumerate(names):
        paths[name.split('.json')[0]] = full_names[xx]
    return paths


def load_notes(notes_path):
    notes = json.load(open(notes_path))
    return notes
