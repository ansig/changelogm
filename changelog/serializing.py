import json
from lxml import etree as ET
from io import BytesIO


def _decorate_text(el):
    inner_text = "".join(el.itertext())
    for ch in el.getchildren():
        if ch.tag in ['b', 'strong']:
            inner_text = inner_text.replace(ch.text, "**{}**".format(ch.text))
        elif ch.tag in ['i', 'em']:
            inner_text = inner_text.replace(ch.text, "*{}*".format(ch.text))
        elif ch.tag in ['pre', 'code']:
            inner_text = inner_text.replace(ch.text, "`{}`".format(ch.text))
        elif ch.tag == 'a':
            inner_text = inner_text.replace(ch.text, "[{}]({})".format(ch.text, ch.get('href')))
    return inner_text


def _render_element(el):
    text = _decorate_text(el)
    if el.tag == 'h1':
        text = "# {}".format(text)
    elif el.tag == 'h2':
        text = "## {}".format(text)
    elif el.tag == 'h3':
        text = "### {}".format(text)
    elif el.tag == 'li':
        text = "- {}".format(text)
    
    if el.tag in ['p', 'h2', 'h3']:
        text = "\n{}".format(text)

    return text


def serialise_markdown(etree_root, flo):
    for el in etree_root:
        if el.tag == 'ul':
            for ch in el.getchildren():
                flo.write("{}\n".format(_render_element(ch)))
        else:
            flo.write("{}\n".format(_render_element(el)))


def serialize_json(changelog_as_dict, flo):
    json.dump(changelog_as_dict, flo, indent=4)


def serialise_html(etree_root, flo, page_title="Changelog"):
    html = ET.Element('html')
    head = ET.SubElement(html, 'head')
    title = ET.SubElement(head, 'title')
    title.text = page_title
    body = ET.SubElement(html, 'body')
    for el in etree_root:
        body.append(el)
    flo.write(ET.tostring(html, method='html', pretty_print=True, encoding='unicode'))
