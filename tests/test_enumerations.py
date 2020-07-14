# -*- coding: utf-8 -*-

"""

test smallparts.l10n.enumerations

"""

import unittest

from smallparts.l10n import enumerations
from smallparts.l10n import languages


class TestSimple(unittest.TestCase):

    """Check the module"""

    def test_english(self):
        """Check english enumerations"""
        source_list = ['cats', 'dogs', 'horses']
        self.assertEqual(
            enumerations.enumeration(
                source_list, enumerations.AND, lang=languages.EN),
            'cats, dogs and horses')

    def test_german(self):
        """Check german enumerations"""
        source_list = [1, 2, 3, 4, 5, 6]
        self.assertEqual(
            enumerations.enumeration(
                source_list, enumerations.EITHER, lang=languages.DE),
            'entweder 1, 2, 3, 4, 5 oder 6')

    def test_pardon_my_french(self):
        """Check french enumerations"""
        source_list = ['dieu', 'maître']
        self.assertEqual(
            enumerations.enumeration(
                source_list, enumerations.NEITHER, lang=languages.FR),
            'ni dieu ni maître')

    def test_unsupported_language(self):
        """Check unsupported language"""
        source_list = [1, 2, 3, 4]
        self.assertRaisesRegex(
            ValueError,
            r"^Language \'.+?\' not supported!$",
            enumerations.enumeration,
            source_list,
            enumerations.AND,
            lang='UNKNOWN')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
