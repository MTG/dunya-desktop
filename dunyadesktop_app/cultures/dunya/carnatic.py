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
    """ Get a list of carnatic recordings in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing recording information::

        {"mbid": Musicbrainz recording id,
         "title": Title of the recording
        }

    For additional information about each recording use :func:`get_recording`.

    """
    extra_headers = _get_collections()
    return conn._get_paged_json("api/carnatic/recording", extra_headers=extra_headers)

def get_recording(rmbid):
    """ Get specific information about a recording.

    :param rmbid: A recording mbid

    :returns: mbid, title, artists, raaga, taala, work.

         ``artists`` includes performance relationships
         attached to the recording, the release, and the release artists.

    """
    extra_headers = _get_collections()
    return conn._dunya_query_json("api/carnatic/recording/%s" % rmbid, extra_headers=extra_headers)

def get_artists():
    """ Get a list of Carnatic artists in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing artist information::

        {"mbid": Musicbrainz artist id,
        "name": Name of the artist}

    For additional information about each artist use :func:`get_artist`

    """
   
    extra_headers = _get_collections()
    return conn._get_paged_json("api/carnatic/artist", extra_headers=extra_headers)

def get_artist(ambid):
    """ Get specific information about an artist.

    :param ambid: An artist mbid
    
    :returns: mbid, name, concerts, instruments, recordings.

         ``concerts``, ``instruments`` and ``recordings`` include
         information from recording- and release-level
         relationships, as well as release artists

    """
    extra_headers = _get_collections()
    return conn._dunya_query_json("api/carnatic/artist/%s" % (ambid), extra_headers=extra_headers)

def get_concerts():
    """ Get a list of Carnatic concerts in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing concert information::

        {"mbid": Musicbrainz concert id,
         "title": title of the concert
        }

    For additional information about each concert use :func:`get_concert`

    """
    extra_headers = _get_collections()
    return conn._get_paged_json("api/carnatic/concert", extra_headers=extra_headers)

def get_concert(cmbid):
    """ Get specific information about a concert.

    :param cmbid: A concert mbid
    :returns: mbid, title, artists, tracks.

         ``artists`` includes performance relationships attached
         to the recordings, the release, and the release artists.

    """
    extra_headers = _get_collections()
    return conn._dunya_query_json("api/carnatic/concert/%s" % cmbid, extra_headers=extra_headers)

def get_works():
    """ Get a list of Carnatic works in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing work information::

        {"mbid": Musicbrainz work id,
         "name": work name
        }

    For additional information about each work use :func:`get_work`.

    """
    return conn._get_paged_json("api/carnatic/work")
    extra_headers = _get_collections()

def get_work(wmbid):
    """ Get specific information about a work.

    :param wmbid: A work mbid
        :returns: mbid, title, composers, raagas, taalas, recordings

    """
    return conn._dunya_query_json("api/carnatic/work/%s" % (wmbid))
    extra_headers = _get_collections()

def get_raagas():
    """ Get a list of Carnatic raagas in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing raaga information:

        {"uuid": raaga uuid,
         "name": name of the raaga
        }

    For additional information about each raaga use :func:`get_raaga`

    """
    return conn._get_paged_json("api/carnatic/raaga")

def get_raaga(rid):
    """ Get specific information about a raaga.

    :param rid: A raaga id or uuid

    :returns: uuid, name, artists, works, composers.

         ``artists`` includes artists with recording- and release-
         level relationships to a recording with this raaga

    """
    return conn._dunya_query_json("api/carnatic/raaga/%s" % str(rid))

def get_taalas():
    """ Get a list of Carnatic taalas in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing taala information::

        {"uuid": taala uuid,
         "name": name of the taala
        }

    For additional information about each taala use :func:`get_taala`.

    """
    return conn._get_paged_json("api/carnatic/taala")

def get_taala(tid):
    """ Get specific information about a taala.

    :param tid: A taala id or uuid
    :returns: uuid, name, artists, works, composers.

         ``artists`` includes artists with recording- and release-
         level relationships to a recording with this raaga

    """
    return conn._dunya_query_json("api/carnatic/taala/%s" % str(tid))

def get_instruments():
    """ Get a list of Carnatic instruments in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing instrument information::

        {"id": instrument id,
         "name": Name of the instrument
        }

    For additional information about each instrument use :func:`get_instrument`

    """
    return conn._get_paged_json("api/carnatic/instrument")

def get_instrument(iid):
    """ Get specific information about an instrument.

    :param iid: An instrument id
    :returns: id, name, artists.

         ``artists`` includes artists with recording- and release-
         level performance relationships of this instrument.

    """
    return conn._dunya_query_json("api/carnatic/instrument/%s" % str(iid))

def download_mp3(recordingid, location):
    """Download the mp3 of a document and save it to the specificed directory.

    :param recordingid: The MBID of the recording
    :param location: Where to save the mp3 to

    """
    if not os.path.exists(location):
        raise Exception("Location %s doesn't exist; can't save" % location)

    recording = get_recording(recordingid)
    concert = get_concert(recording["concert"][0]["mbid"])
    title = recording["title"]
    artists = " and ".join([a["name"] for a in concert["concert_artists"]])
    contents = docserver.get_mp3(recordingid)
    name = "%s - %s.mp3" % (artists, title)
    path = os.path.join(location, name)
    open(path, "wb").write(contents)
    return name

def download_concert(concertid, location):
    """Download the mp3s of all recordings in a concert and save
    them to the specificed directory.

    :param concert: The MBID of the concert
    :param location: Where to save the mp3s to

    """
    if not os.path.exists(location):
        raise Exception("Location %s doesn't exist; can't save" % location)

    concert = get_concert(concert_id)
    artists = " and ".join([a["name"] for a in concert["concert_artists"]])
    concertname = concert["title"]
    concertdir = os.path.join(location, "%s - %s" % (artists, concertname))
    for r in concert["tracks"]:
        rid = r["mbid"]
        title = r["title"]
        contents = docserver.get_mp3(rid)
        name = "%s - %s.mp3" % (artists, title)
        path = os.path.join(concertdir, name)
        open(path, "wb").write(contents)
