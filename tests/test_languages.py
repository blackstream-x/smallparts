# -*- coding: utf-8 -*-

"""

test smallparts.l10n.languages

"""

import unittest

from smallparts.l10n import languages


class TestSimple(unittest.TestCase):

    """Check the l10n.languages module"""

    def test_unsupported_language(self):
        """Message: unsupported language"""
        self.assertEqual(
            languages.missing_translation('xw'),
            "Language 'xw' not supported!")

    def test_missing_translation(self):
        """Message: missing translation for a supported language"""
        self.assertEqual(
            languages.missing_translation('de'),
            "No 'de' translation available yet!")


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
