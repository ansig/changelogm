import argparse

from io import BytesIO, TextIOWrapper
from pprint import pprint

from . import parsing
from . import serializing


def parse(filename, *args):
    """ Read a changelog file and write it on stdout or to a file """

    arg_parser = argparse.ArgumentParser(description="Parse a changelog file")
    arg_parser.add_argument('FORMAT', choices=['json', 'html', 'markdown'], help="The output format to use")
    arg_parser.add_argument('-o', '--output_file', default=None, type=str, action='store', 
        help="Path to a file where output should be written (default: stdout)")
    
    parsed_args = arg_parser.parse_args(args)

    with open(filename, 'r') as f:
        text = parsing.preprocess_changelog(f)
    etree = parsing.parse_changelog_text(text)
    changelog = parsing.parse_changelog_etree(etree)

    flo = open(parsed_args.output_file, 'w') if parsed_args.output_file else TextIOWrapper(BytesIO(), encoding='utf-8')

    try:
        if parsed_args.FORMAT == 'json':
            serializing.serialize_json(changelog, flo)
        elif parsed_args.FORMAT == 'html':
            serializing.serialise_html(etree, flo)
        elif parsed_args.FORMAT == 'markdown':
            serializing.serialise_markdown(etree, flo)
        
        if not parsed_args.output_file:
            flo.seek(0)
            for line in flo:
                print(line.rstrip('\n'))
    
    finally:
        flo.close()


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
