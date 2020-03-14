def release_upcoming(etree_root, version):
    upcoming_element = get_section_element(etree_root, "[Kommande]")
    upcoming_element.text = "[{}]".format(version)

    new_upcoming_element = ET.Element('h2')
    new_upcoming_element.text = "[Kommande]"
    upcoming_element.addprevious(new_upcoming_element)
