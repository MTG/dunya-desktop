import xml.etree.ElementTree as ET


def initialize_svg(path):
    tree = ET.parse(path)
    return tree, tree.getroot()

SVG_NS = '{http://www.w3.org/2000/svg}'


def change_color(path, tree, root, note_id, color):
    note_id = 'note-' + str(note_id)
    for a in root.findall(SVG_NS + 'a'):
        if 'id' in a.attrib:
            if a.attrib['id'] == note_id:
                note_color_parameter = a.find(SVG_NS + 'path')
                note_color_parameter.set('fill', color)
    tree.write(path)


def get_note_indexes(path, root):
    notes = {}
    for a in root.findall(SVG_NS + 'a'):
        if 'id' in a.attrib:
            index = a.attrib['id'].split('note-')[-1]
            notes[index] = path
    return notes
