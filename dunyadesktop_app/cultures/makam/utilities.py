import compmusic.dunya.makam
from dunyadesktop_app.utilities.utilities import *


def get_attributes():
    makams = compmusic.dunya.makam.get_makams()
    sort_dictionary(makams, 'name')

    forms = compmusic.dunya.makam.get_forms()
    sort_dictionary(forms, 'name')

    usuls = compmusic.dunya.makam.get_usuls()
    sort_dictionary(usuls, 'name')

    composers = compmusic.dunya.makam.get_composers()
    sort_dictionary(composers, 'name')

    performers = compmusic.dunya.makam.get_artists()
    sort_dictionary(performers, 'name')

    instruments = compmusic.dunya.makam.get_instruments()
    sort_dictionary(instruments, 'name')

    return makams, forms, usuls, composers, performers, instruments
