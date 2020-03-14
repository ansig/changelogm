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
            E.h2('[Kommande]'),
            E.h3('Ändrat'),
            E.ul(
                E.li('[ABC-123] Detta har ändrats')
            ),
            E.h2('[1.0.0]'),
            E.h3('Tillagt'),
            E.ul(
                E.li('[DEF-456] Detta har lagts till')
            ),
            E.h3('Ändrat'),
            E.ul(
                E.li('[GHI-789] Och detta'),
                E.li('[JKL-011] Ändrat detta')
            )
        )
        output = parsing.parse_changelog_etree(changelog_etree)
        expected = {
            '[Kommande]': {
                'Ändrat': ['[ABC-123] Detta har ändrats']},
            '[1.0.0]': {
                'Tillagt': ['[DEF-456] Detta har lagts till'],
                'Ändrat': ['[GHI-789] Och detta', '[JKL-011] Ändrat detta']
            }
        }
        self.assertDictEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
