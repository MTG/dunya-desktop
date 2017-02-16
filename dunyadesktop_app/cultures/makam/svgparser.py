import xml.etree.ElementTree as ET


def initialize_svg(path):
    tree = ET.parse(path)
    return tree, tree.getroot()


def change_color(path, tree, root, note_id, color):
    for child in root.iter('{http://www.w3.org/2000/svg}a'):
        try:
            if child.attrib['id'] == 'note-' + str(note_id):
                note = child.find('{http://www.w3.org/2000/svg}path')
                note.set('fill', color)
        except KeyError:
            pass

    tree.write(path)
