import mistune
import re
from lxml import etree as ET


def preprocess_changelog(file):
    """ Read the changelog Markdown text from the file and perform basic preprocessing before returning the text. """
    lines = []
    newline = '\n'
    previous = None
    for current in file:
        if re.match("^##+.+", current) and previous != newline:
            raise Exception("Headers of level 2 or higher must be preceded by a blank line but the following was not: {}".format(line))
        lines.append(current)
        previous = current
    return "".join(lines)

def enclosed(func):
    """ Wrap the return text in enclosing elements. """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return "<changelog>\n{}</changelog>".format(res)
    return wrapper

def parse_changelog_text(text):
    """ Return an ElementTree structure from the given Markdown text. """
    assert type(text) == str, "The parameter 'text' must be a string"
    xhtml_string = _render_markdown(text)
    return _parse_xhtml(xhtml_string)

@enclosed
def _render_markdown(text):
    """ Render the given Markdown text as xhtml. """
    parser = mistune.Markdown(escape=True, hard_wrap=True, use_xhtml=True, parse_block_html=True, parse_inline_html=True)
    xhtml_string = parser(text)
    return xhtml_string

def _parse_xhtml(text):
    """ Parse the given xhtml text into a ElementTree and return the root Element. """
    root = ET.fromstring(text)
    return root

def _validate_section(title):
    if not re.fullmatch("\[(\d+\.\d+\.\d+|Unreleased)\]", title):
        raise Exception("Section title must be version number or 'Unreleased' enclosed in brackets ([n.n.n] or [Unreleased]) but was: {}".format(title))

def _validate_subsection(title):
    allowed_sections = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]
    if title not in allowed_sections:
        raise Exception("Subsection title '{}' is not one of: {}".format(title, allowed_sections))

def _validate_list_item(text):
    if not re.match("^\[[A-Z]+\-[0-9]+\]\s.+$", text):
        raise Exception("List items must be ONE line that starts with ticket number enclosed in brackets ([ABC-123]) and is followed by some text but was: '{}'".format(text))

def parse_changelog_etree(etree_root):
    """ Parse the changelog ElementTree and return a dictionary of all changes it contains. The contents of each change is sanitized (e.g. formatting is removed). """
    
    assert len(etree_root) > 1, "The changes must at least contain one row"

    title_element = etree_root[0]
    if title_element.tag != 'h1':
        raise Exception("The first element in the changes must be a h1 title")

    found_introduction = False
    for el in title_element.itersiblings():
        if el.tag in ['p', 'pre', 'ul']:
            found_introduction = True
            continue
        elif el.tag == 'h2':
            if not found_introduction:
                raise Exception("Found section '{}' before introduction".format(el.text))
            break
        else:
            raise Exception("Found unexpected element in introduction: {}".format(el.tag))

    changes = {}
    section_elems = etree_root.xpath('h2')
    for section_element in section_elems:
        section = section_element.text
        _validate_section(section)
        if section in changes:
            raise Exception("Section already exists: {}".format(section))
        changes[section] = {}
        subsection = None
        for el in section_element.itersiblings(preceding=False):
            if el.tag == 'h3':
                subsection = el.text
                _validate_subsection(subsection)
                if subsection in changes[section]:
                    raise Exception("Subsection already exists in '{}': {}".format(changes[section], subsection))
                changes[section][subsection] = []
            elif el.tag == 'ul':
                if subsection == None:
                    raise Exception("Found list of changes before any subsection")
                for ch in el.getchildren():
                    text = "".join(ch.itertext())
                    _validate_list_item(text)
                    changes[section][subsection].append(text)
            elif el.tag == 'h3' or el.tag == 'h2':
                break
            else:
                raise Exception("Found unexpected element in section '{}': {}".format(section, el.tag))
    return changes
