def convert_str(string):
    return u''.join(string).encode('utf-8').strip()

def set_css(widget, css_path):
    try:
        with open(css_path) as f:
            css = f.read()
        widget.setStyleSheet(css)
    except IOError:
        pass