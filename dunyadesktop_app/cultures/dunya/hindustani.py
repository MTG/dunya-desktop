import os
import logging
logger = logging.getLogger("dunya")

from . import conn
from . import docserver

COLLECTIONS = None

def set_collections(collections):
    """ Set a list of collections mbid to restrict the queries.
    You must call this before you can make any other calls, otherwise 
    they won't be restricted.

    Arguments:
        collections: list of collections mbids

    """
    global COLLECTIONS
    COLLECTIONS = collections

def _get_collections():
    extra_headers = None
    if COLLECTIONS:
        extra_headers = {}
        extra_headers['Dunya-Collection'] = ','.join(COLLECTIONS)
    return extra_headers

def get_recordings():
    """ Get a list of hindustani recordings in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing recording information::

        {"mbid": Musicbrainz recording id,
        "title": Title of the recording
        }

    For additional information about each recording use :func:`get_recording`.

    """
    extra_headers = _get_collections()
    return conn._get_paged_json("api/hindustani/recording", extra_headers=extra_headers)

def get_recording(rmbid):
    """ Get specific information about a recording.

    Arguments:
    :param rmbid: A recording mbid

    :returns: mbid, title, artists, raags, taals, layas, forms and works.

         ``artists`` include performance relationships attached
         to the recording, the release, and the release artists.

    """
    extra_headers = _get_collections()
    return conn._dunya_query_json("api/hindustani/recording/%s" % rmbid, extra_headers=extra_headers)

def get_artists():
    """ Get a list of Hindustani artists in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing artist information::

        {"mbid": Musicbrainz artist id,
         "name": Name of the artist
        }

    For additional information about each artist use :func:`get_artist`.

    """
    extra_headers = _get_collections()
    return conn._get_paged_json("api/hindustani/artist", extra_headers=extra_headers)

def get_artist(ambid):
    """ Get specific information about an artist.

    Arguments:
    :param ambid: An artist mbid

    :returns: mbid, name, releases, instruments, recordings

             ``releases``, ``instruments`` and ``recordings`` include
             information from recording- and release-level
             relationships, as well as release artists

    """
    extra_headers = _get_collections()
    return conn._dunya_query_json("api/hindustani/artist/%s" % ambid, extra_headers=extra_headers)

def get_releases():
    """ Get a list of Hindustani releases in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing release information::

        {"mbid": Musicbrainz release id,
         "title": title of the release
        }

    For additional information about each release use :func:`get_release`.

    """
    extra_headers = _get_collections()
    return conn._get_paged_json("api/hindustani/release", extra_headers=extra_headers)

def get_release(cmbid):
    """ Get specific information about a release.

    :param cmbid: A release mbid
    :returns: mbid, title, artists, tracks, release artists

         ``artists`` includes performance relationships attached
         to the recordings, the release, and the release artists.

    """
    extra_headers = _get_collections()
    return conn._dunya_query_json("api/hindustani/release/%s" % cmbid, extra_headers=extra_headers)

def get_works():
    """ Get a list of Hindustani works in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing work information::

        {"mbid": Musicbrainz work id,
        "name": work name
        }

    For additional information about each work use :func:`get_work`.

    """
    extra_headers = _get_collections()
    return conn._get_paged_json("api/hindustani/work", extra_headers=extra_headers)

def get_work(wmbid):
    """ Get specific information about a work.

    :param wmbid: A work mbid
    :returns: mbid, title, recordings

    """
    extra_headers = _get_collections()
    return conn._dunya_query_json("api/hindustani/work/%s" % wmbid, extra_headers=extra_headers)

def get_raags():
    """ Get a list of Hindustani raags in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing raag information::

        {"uuid": raag uuid,
         "name": name of the raag
        }

    For additional information about each raag use :func:`get_raag`.

    """
    return conn._get_paged_json("api/hindustani/raag")

def get_raag(rid):
    """ Get specific information about a raag.
    Arguments:
    :param rid: A raag id or uuid
    :returns: uuid, name, artists, recordings, composers

             ``artists`` includes artists with recording-level
             relationships to a recording with this raag

    """
    return conn._dunya_query_json("api/hindustani/raag/%s" % str(rid))

def get_taals():
    """ Get a list of Hindustani taals in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing taal information::

        {"uuid": taal uuid,
         "name": name of the taal
        }

    For additional information about each taal use :func:`get_taal`.

    """
    return conn._get_paged_json("api/hindustani/taal")

def get_taal(tid):
    """ Get specific information about a taal.

    :param tid: A taal id or uuid
    :returns: uuid, name, recordings, composers

    """
    return conn._dunya_query_json("api/hindustani/taal/%s" % str(tid))

def get_layas():
    """ Get a list of Hindustani layas in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing laya information::

        {"id": laya id,
         "name": name of the laya
        }

    For additional information about each laya use :func:`get_laya`.

    """
    return conn._get_paged_json("api/hindustani/laya")

def get_laya(lid):
    """ Get specific information about a laya.

    :param lid: A laya id or uuid
    :returns: id, name, recordings

    """
    return conn._dunya_query_json("api/hindustani/laya/%s" % str(lid))

def get_forms():
    """ Get a list of Hindustani forms in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing form information::

        {"uuid": form  uuid,
         "name": name of the form
        }

    For additional information about each form use :func:`get_form`

    """
    return conn._get_paged_json("api/hindustani/form")

def get_form(fid):
    """ Get specific information about a form.

    :param fid: A form id or uuid
    :returns: uuid, name, artists, recordings.

         ``artists`` includes artists with recording- and release-
         level relationships to a recording with this form

    """
    return conn._dunya_query_json("api/hindustani/form/%s" % str(fid))

def get_instruments():
    """ Get a list of Hindustani instruments in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing instrument information::

        {"id": instrument id,
         "name": Name of the instrument
        }

    For additional information about each instrument use :func:`get_instrument`

    """
    return conn._get_paged_json("api/hindustani/instrument")

def get_instrument(iid):
    """ Get specific information about an instrument.

    :param iid: An instrument id
    :returns: id, name, artists

             ``artists`` includes artists with recording- and release-
             level performance relationships of this instrument.

    """
    return conn._dunya_query_json("api/hindustani/instrument/%s" % str(iid))

def download_mp3(recordingid, location):
    """Download the mp3 of a document and save it to the specificed directory.

    :param recordingid: The MBID of the recording
    :param location: Where to save the mp3 to

    """
    if not os.path.exists(location):
        raise Exception("Location %s doesn't exist; can't save" % location)

    recording = get_recording(recordingid)
    release = get_release(recording["release"][0]["mbid"])
    title = recording["title"]
    artists = " and ".join([a["name"] for a in release["release_artists"]])
    contents = docserver.get_mp3(recordingid)
    name = "%s - %s.mp3" % (artists, title)
    path = os.path.join(location, name)
    open(path, "wb").write(contents)
    return name

def download_release(release_id, location):
    """Download the mp3s of all recordings in a release and save
    them to the specificed directory.

    :param release_id: The MBID of the release
    :param location: Where to save the mp3s to

    """
    if not os.path.exists(location):
        raise Exception("Location %s doesn't exist; can't save" % location)

    release = get_release(release_id)
    artists = " and ".join([a["name"] for a in release["release_artists"]])
    releasename = release["title"]
    releasedir = os.path.join(location, "%s - %s" % (artists, releasename))
    for r in release["tracks"]:
        rid = r["mbid"]
        title = r["title"]
        contents = docserver.get_mp3(rid)
        name = "%s - %s.mp3" % (artists, title)
        path = os.path.join(releasedir, name)
        open(path, "wb").write(contents)
