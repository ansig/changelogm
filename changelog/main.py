import os
import sys
import argparse
import textwrap

from . import cli


def _commands_desc(names):
    epilog_lines = ["Available commands:"]
    text_wrapper = textwrap.TextWrapper(width=70, initial_indent=' * ', subsequent_indent='     ')
    for n in names:
        f = getattr(cli, n)
        epilog_lines.append(text_wrapper.fill("{} -{}".format(f.__name__, f.__doc__)))
    epilog_lines.append("\nFor more info on each command run: changelog COMMAND help")
    return '\n'.join(epilog_lines)


def main():

    names = [name for name in dir(cli) if not name.startswith('_') and name != "main"]

    arg_parser = argparse.ArgumentParser(
        description="A CLI for the Changelog Manager tool", 
        epilog=_commands_desc(names), 
        formatter_class=argparse.RawDescriptionHelpFormatter)
    arg_parser.add_argument("-f", "--filename", type=str, action='store', default="CHANGELOG.md", 
        help="path to the changelog file to operate on (default: CHANGELOG.md)")
    arg_parser.add_argument("COMMAND", type=str, help="name of the CLI function to run")
    args, command_args = arg_parser.parse_known_args()

    if args.COMMAND not in names:
        print("Error: no such command: '{}'\n".format(args.COMMAND))
        print(_commands_desc(names))
        sys.exit(1)

    f = getattr(cli, args.COMMAND)
    f(args.filename, *command_args)
