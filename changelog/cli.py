from pprint import pprint

from . import parsing
from . import serializing

def read(filename, *args):
    """ Display a changelog file """
    with open(filename, 'r') as f:
        text = parsing.preprocess_changelog(f)
    etree = parsing.parse_changelog_text(text)
    changelog = parsing.parse_changelog_etree(etree)
    pprint(changelog)


def add(*args):
    """ Update a changelog file with a new entry """
    print("Adding...")

def remove(*args):
    """ Remove an entry from a changelog file """
    print("Removing...")

def release(*args):
    """ Change the 'Upcoming' section to a version """
    print("Releasing...")

def check(*args):
    """ Verify some fact about the changelog file """
    print("Verifying...")
