import unittest
import lxml

from lxml.builder import E
from io import StringIO
from context import serializing


class TestParsing(unittest.TestCase):

    def test_serialize_markdown(self):
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
        output = StringIO()
        serializing.serialise_markdown(changelog_etree, output)

        expected = """# Changelog

This is the introduction text. It *explains* something **vital**

## [Kommande]

### Ändrat
- [ABC-123] Detta har ändrats

## [1.0.0]

### Tillagt
- [DEF-456] Detta har lagts till

### Ändrat
- [GHI-789] Och detta
- [JKL-011] Ändrat detta
"""
        self.assertEqual(output.getvalue(), expected)


if __name__ == '__main__':
    unittest.main()
