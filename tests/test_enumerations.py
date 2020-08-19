# -*- coding: utf-8 -*-

"""

test smallparts.l10n.enumerations

"""

import unittest

from smallparts.l10n import enumerations
from smallparts.l10n import languages


class TestSimple(unittest.TestCase):

    """Check the l10n.enumerations module"""

    def test_unsupported_language_spacing_rules(self):
        """Unsupported language in apply_spacing_rules"""
        self.assertRaisesRegex(
            ValueError,
            r"^Language \'.+?\' not supported!$",
            enumerations.apply_spacing_rules,
            ',',
            lang='UNKNOWN')

    def test_spacing_rule_empty(self):
        """Spacing rule: empty string"""
        self.assertEqual(
            enumerations.apply_spacing_rules('', lang=languages.EN),
            '')

    def test_spacing_rule_punctuation_english(self):
        """Spacing rule: english punctuation"""
        self.assertEqual(
            enumerations.apply_spacing_rules('/', lang=languages.EN),
            '/')
        self.assertEqual(
            enumerations.apply_spacing_rules('!', lang=languages.EN),
            '! ')

    def test_spacing_rule_punctuation_french(self):
        """Spacing rule: french punctuation"""
        self.assertEqual(
            enumerations.apply_spacing_rules('!', lang=languages.FR),
            ' ! ')

    def test_english(self):
        """English enumerations"""
        source_list = ['cats', 'dogs', 'horses']
        self.assertEqual(
            enumerations.enumeration(
                source_list, enumerations.AND, lang=languages.EN),
            'cats, dogs and horses')

    def test_german(self):
        """German enumerations"""
        source_list = [1, 2, 3, 4, 5, 6]
        self.assertEqual(
            enumerations.enumeration(
                source_list, enumerations.EITHER, lang=languages.DE),
            'entweder 1, 2, 3, 4, 5 oder 6')

    def test_pardon_my_french(self):
        """French enumerations"""
        source_list = ['dieu', 'maître']
        self.assertEqual(
            enumerations.enumeration(
                source_list, enumerations.NEITHER, lang=languages.FR),
            'ni dieu ni maître')

    def test_defaults(self):
        """Default values for separators"""
        source_list = [1, 2, 3, 4, 5, 6]
        self.assertEqual(
            enumerations.enumeration(
                source_list, enumerations.AND, lang='__test__'),
            '1,2,3,4,5,6')

    def test_unsupported_language_enum(self):
        """Unsupported language"""
        source_list = [1, 2, 3, 4]
        self.assertRaisesRegex(
            ValueError,
            r"^Language \'.+?\' not supported!$",
            enumerations.enumeration,
            source_list,
            enumerations.AND,
            lang='UNSUPPORTED')

    def test_missing_definition(self):
        """Missing definition (partially provided translation)"""
        source_list = [1, 2, 3, 4]
        self.assertRaisesRegex(
            ValueError,
            r"^No \'.+?\' translation available for \'.+?\'!$",
            enumerations.enumeration,
            source_list,
            enumerations.NEITHER,
            lang='__test__')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
