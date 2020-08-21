# -*- coding: utf-8 -*-

"""

test smallparts.l10n.time_indications

"""

import unittest

from smallparts.l10n import languages
from smallparts.l10n import time_indications


class TestSimple(unittest.TestCase):

    """Test the l10n.time_indications module"""

    def test_unsupported_language(self):
        """Unsupported language"""
        self.assertRaisesRegex(
            ValueError,
            r"^Language \'.+?\' not supported!$",
            time_indications.format_component,
            seconds=7,
            lang='UNSUPPORTED')

    def test_missing_argument(self):
        """Missing time component"""
        self.assertRaises(
            ValueError,
            time_indications.format_component)

    def test_default_language(self):
        """Default (english) time components"""
        self.assertEqual(
            time_indications.format_component(seconds=7),
            '7 seconds')

    def test_german(self):
        """German time components"""
        self.assertEqual(
            time_indications.format_component(hours=19,
                                              lang=languages.DE),
            '19 Stunden')

    def test_pardon_my_french(self):
        """French time components"""
        self.assertEqual(
            time_indications.format_component(weeks=1,
                                              lang=languages.FR),
            '1 semaine')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
