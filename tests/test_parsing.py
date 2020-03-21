import unittest
import lxml

from lxml.builder import E
from context import parsing


class TestParsing(unittest.TestCase):

    def test_preprocess(self):
        with open('data/CHANGELOG.md', 'r') as f:
            output = parsing.preprocess_changelog(f)
        self.assertIsInstance(output, str, "Should have returned string")

    def test_parse_changelog_text(self):
        with open('data/CHANGELOG.md', 'r') as f:
            text = "".join(f.readlines())
            output = parsing.parse_changelog_text(text)
        self.assertIsInstance(output, lxml.etree._Element, "Should have returned an lxml.etree._Element")

    def test_parse_changelog_etree(self):
        changelog_etree = E.changelog(
            E.h1('Changelog'),
            E.p('This is the introduction text. It ', E.i('explains'), ' something ', E.b('vital')),
            E.h2('[Unreleased]'),
            E.h3('Changed'),
            E.ul(
                E.li('[ABC-123] This has changed')
            ),
            E.h2('[1.0.0]'),
            E.h3('Added'),
            E.ul(
                E.li('[DEF-456] This was added')
            ),
            E.h3('Changed'),
            E.ul(
                E.li('[GHI-789] X was changed to Y'),
                E.li('[JKL-011] Something was changed')
            )
        )
        output = parsing.parse_changelog_etree(changelog_etree)
        expected = {
            '[Unreleased]': {
                'Changed': ['[ABC-123] This has changed']},
            '[1.0.0]': {
                'Added': ['[DEF-456] This was added'],
                'Changed': ['[GHI-789] X was changed to Y', '[JKL-011] Something was changed']
            }
        }
        self.assertDictEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
