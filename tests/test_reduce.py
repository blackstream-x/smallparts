# -*- coding: utf-8 -*-

"""

test smallparts.text.reduce

"""

import unittest

from smallparts.text import reduce


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_ascii_check(self):
        """Check ascii replacements"""
        self.assertRaises(
            ValueError,
            reduce.checked_ascii,
            '{Capital ß}')

    def test_conversion_table_add_and_eq(self):
        """Addition of ConversionTables"""
        self.assertEqual(
            reduce.ConversionTable({'ä': 'ae'}) + \
                reduce.ConversionTable({'ü': 'ue'}),
            reduce.ConversionTable({'ä': 'ae', 'ü': 'ue'}))

    def test_invalid_conversion_table_addition(self):
        """Addition of an object that is neither a dict
        nor a-ConversionTable
        """
        conversion_table = reduce.ConversionTable(reduce.LATIN)
        self.assertRaises(
            TypeError,
            conversion_table.__add__,
            'unsupported (pointless)')

    def test_remove_invalid_characters(self):
        """Empty replacements for C1 controls"""
        conversion_table = reduce.ConversionTable(
            reduce.LATIN,
            remove_c1_controls=True)
        self.assertEqual(
            conversion_table.reduce_character('\x81'), '')

    def test_reduce_unknown_characters(self):
        r"""\xNN replacements for C1 controls"""
        conversion_table = reduce.ConversionTable(
            reduce.LATIN)
        self.assertEqual(
            conversion_table.reduce_character('\x81'), r'\x81')

    def test_reduce_unknown_unicode(self):
        r"""\uNNNN replacements for Unicode characters above U00ff"""
        conversion_table = reduce.ConversionTable(
            reduce.LATIN)
        self.assertEqual(
            conversion_table.reduce_text(
                'Bérurier Noir – Hélène et le sang'),
            r'Berurier Noir \u2013 Helene et le sang')

    def test_reduce_default(self):
        """Default replacements"""
        conversion_table = reduce.ConversionTable(
            reduce.LATIN,
            default_replacement='???')
        self.assertEqual(
            conversion_table.reduce_text(
                'Bérurier Noir – Hélène et le sang'),
            r'Berurier Noir ??? Helene et le sang')

    def test_reduce_punctuation(self):
        """Replacement of punctuation"""
        conversion_table = reduce.ConversionTable(
            reduce.LATIN) + reduce.PUNCTUATION
        self.assertEqual(
            conversion_table.reduce_text(
                'Bérurier Noir – Hélène et le sang'),
            'Berurier Noir - Helene et le sang')

    def test_basic_latin(self):
        """Basic latin conversion results"""
        self.assertEqual(
            reduce.latin_to_ascii('Motörhead'),
            'Motorhead')

    def test_german_latin(self):
        """German conversion results"""
        self.assertEqual(
            reduce.latin_to_ascii('Müller',
                                  reduce.GERMAN_OVERRIDES),
            'Mueller')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
