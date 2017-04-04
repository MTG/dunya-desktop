import os
import logging

import unicodedata
import re

logger = logging.getLogger("dunya")

from . import conn
from . import docserver

def get_recordings():
    """ Get a list of makam recordings in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing recording information::

        {"mbid": Musicbrainz recording id,
         "title": Title of the recording
        }

    For additional information about each recording use :func:`get_recording`.

    """
    return conn._get_paged_json("api/makam/recording")

def get_recording(rmbid):
    """ Get specific information about a recording.

    :param rmbid: A recording mbid

    :returns: mbid, title, releases, performers, work.

         ``artists`` includes performance relationships
         attached to the recording, the release, and the release artists.

    """
    return conn._dunya_query_json("api/makam/recording/%s" % rmbid)

def get_artists():
    """ Get a list of makam artists in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing artist information::

        {"mbid": Musicbrainz artist id,
        "name": Name of the artist}

    For additional information about each artist use :func:`get_artist`

    """
    return conn._get_paged_json("api/makam/artist")

def get_artist(ambid):
    """ Get specific information about an artist.

    :param ambid: An artist mbid
    :returns: mbid, name, releases, instruments.

         ``releases``, ``instruments`` and ``recordings`` include
         information from recording- and release-level
         relationships, as well as release artists

    """
    return conn._dunya_query_json("api/makam/artist/%s" % ambid)

def get_composers():
    """ Get a list of makam composers in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing composers information::

        {"mbid": Musicbrainz composer id,
        "name": Name of the composer}

    For additional information about each composer use :func:`get_composer`

    """
    return conn._get_paged_json("api/makam/composer")

def get_composer(cmbid):
    """ Get specific information about an composer.

    :param cmbid: A composer mbid
    :returns: mbid, name, works, lyric_works

         ``works`` contains a list of works that the composer has written.
         ``lyric_works`` are works where they were lyricist.

    """
    return conn._dunya_query_json("api/makam/composer/%s" % cmbid)

def get_releases():
    """ Get a list of makam releases in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing release information::

        {"mbid": Musicbrainz release id,
         "title": title of the release
        }

    For additional information about each release use :func:`get_release`

    """
    return conn._get_paged_json("api/makam/release")

def get_release(cmbid):
    """ Get specific information about a release.

    :param cmbid: A release mbid
    :returns: mbid, title, artists, tracks.

         ``artists`` includes performance relationships attached
         to the recordings, the release, and the release artists.

    """
    return conn._dunya_query_json("api/makam/release/%s" % cmbid)

def get_works():
    """ Get a list of makam works in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing work information::

        {"mbid": Musicbrainz work id,
         "name": work name
        }

    For additional information about each work use :func:`get_work`.

    """
    return conn._get_paged_json("api/makam/work")

def get_work(wmbid):
    """ Get specific information about a work.

    :param wmbid: A work mbid
    :returns: mbid, title, composers, makams, forms, usuls, recordings

    """
    return conn._dunya_query_json("api/makam/work/%s" % wmbid)

def get_instruments():
    """ Get a list of makam instruments in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing instrument information::

        {"id": instrument id,
         "name": Name of the instrument
        }

    For additional information about each instrument use :func:`get_instrument`

    """
    return conn._get_paged_json("api/makam/instrument")

def get_instrument(iid):
    """ Get specific information about an instrument.

    :param iid: An instrument id
    :returns: id, name, artists.

         ``artists`` includes artists with recording- and release-
         level performance relationships of this instrument.

    """
    return conn._dunya_query_json("api/makam/instrument/%s" % str(iid))

def get_forms():
    """ Get a list of makam forms in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing form information::

        {"uuid": form uuid,
         "name": Name of the form
        }

    For additional information about each form use :func:`get_form`

    """
    return conn._get_paged_json("api/makam/form")

def get_form(fid):
    """ Get specific information about a form.

    :param fid: A form id or uuid
    :returns: uuid, name, works.
    """
    return conn._dunya_query_json("api/makam/form/%s" % str(fid))

def get_makams():
    """ Get a list of makam makams in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing makam information::

        {"uuid": makam uuid,
         "name": Name of the makam
        }

    For additional information about each makam use :func:`get_makam`

    """
    return conn._get_paged_json("api/makam/makam")

def get_makam(mid):
    """ Get specific information about a makam.

    :param mid: A makam id or uuid
    :returns: uuid, name, works, taksims, gazels.

    the ``taksims`` and ``gazels`` lists are of recordings.
    """
    return conn._dunya_query_json("api/makam/makam/%s" % str(mid))

def get_usuls():
    """ Get a list of makam usuls in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing usul information::

        {"uuid": usul uuid,
         "name": Name of the usul
        }

    For additional information about each usul use :func:`get_usul`

    """
    return conn._get_paged_json("api/makam/usul")

def get_symbtrs():
    """ Get a list of musicbrainz id - symbtr mappings in the database.
    This function will automatically page through API results.

    returns: A list of dictionaries containing symbtr information::

        {"uuid": musicbrainz uuid (could be a work id or a recording id),
         "name": Name of the symbtr track
        }

    """
    return conn._get_paged_json("api/makam/symbtr")

def get_symbtr(uuid):
    """ Get a symbtr file info from id
    This function will automatically page through API results.
    
    :param uuid: A symbtr id
    
    returns: name and id of the symbtr file

    """
    return conn._dunya_query_json("api/makam/symbtr/%s" % uuid)



def get_usul(uid):
    """ Get specific information about a usul.

    :param uid: An usul id or uuid
    :returns: uuid, name, works, taksims, gazels.

    the ``taksims`` and ``gazels`` lists are of recordings. They are
    only valid for the usul ``serbest``
    """
    return conn._dunya_query_json("api/makam/usul/%s" % str(uid))

def get_works_by_query(mid='', uid='', fid='', cmbid='', ambid=''):
    """ Get the works filtered according to the input makam uuid, usul uuid
	form uuid, composer mbid and artist mbid

    :param mid: A makam id or uuid
    :param uid: An usul id or uuid
    :param fid: A form id or uuid
    :param cmbid: A composer mbid
    :param ambid: An artist mbid
    :return: A list of dictionaries containing work/s
    """
    path = 'work?usul={0}&performer={1}&form={2}&artist={3}&makam={4}'
    path = path.format(uid, ambid, fid, cmbid, mid)
    return conn._get_paged_json("api/makam/" + path)

def download_mp3(recordingid, location, slugify=False):
    """Download the mp3 of a document and save it to the specificed directory.

    :param recordingid: The MBID of the recording
    :param location: Where to save the mp3 to
    :param slugify: Boolean specifying whether to slugify the filepath or not
    """
    if not os.path.exists(location):
        raise Exception("Location %s doesn't exist; can't save" % location)

    recording = get_recording(recordingid)
    title = recording["title"]
    title = slugify_tr(title) if slugify else title
    title = title.replace("/", "_")

    rels = recording["releases"]
    if rels:
        release = get_release(rels[0]["mbid"])
        artists = " and ".join([a["name"] for a in release["release_artists"]])
        artists = slugify_tr(artists) if slugify else artists

        name = "%s_%s.mp3" % (artists, title)
    else:
        name = "%s.mp3" % title

    contents = docserver.get_mp3(recordingid)
    path = os.path.join(location, name)
    open(path, "wb").write(contents)
    return path

def download_release(releaseid, location, slugify=False):
    """Download the mp3s of all recordings in a release and save
    them to the specificed directory.

    :param release: The MBID of the release
    :param location: Where to save the mp3s to
    :param slugify: Boolean specifying whether to slugify the filepath or not
    """
    if not os.path.exists(location):
        raise Exception("Location %s doesn't exist; can't save" % location)

    release = get_release(releaseid)
    artists = " and ".join([a["name"] for a in release["release_artists"]])
    artists = slugify_tr(artists) if slugify else artists

    releasename = release["title"]
    releasename = slugify_tr(releasename) if slugify else releasename
    releasedir = os.path.join(location, "%s_%s" % (artists, releasename))

    if not os.path.exists(releasedir):
        os.makedirs(releasedir)

    for r in release["recordings"]:
        rid = r["mbid"]
        title = r["title"]
        title = slugify_tr(title) if slugify else title
        title = title.replace("/", "_")

        track = r["track"]
        contents = docserver.get_mp3(rid)
        name = "%d_%s_%s.mp3" % (track, artists, title)
        path = os.path.join(releasedir, name)
        open(path, "wb").write(contents)

def slugify_tr(value):

    value_slug = value.replace('\u0131', 'i')
    value_slug = unicodedata.normalize('NFKD', value_slug).encode('ascii', 'ignore').decode('ascii')
    value_slug = re.sub('[^\w\s-]', '', value_slug).strip()

    return re.sub('[-\s]+', '-', value_slug)
