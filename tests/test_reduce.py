# -*- coding: utf-8 -*-

"""

test smallparts.text.reduce

"""

import unittest

from smallparts.text import reduce


class TestSimple(unittest.TestCase):

    """Check the module"""

    def test_ascii_check(self):
        """Check ascii replacements"""
        self.assertRaises(
            ValueError,
            reduce.check_ascii_replacement,
            'ẞ',
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

    def test_reduce_invalid_characters(self):
        """Empty replacements for C1 controls"""
        conversion_table = reduce.ConversionTable(reduce.LATIN)
        self.assertEqual(
            conversion_table.reduce_character('\x81'),
            '')

    def test_basic_latin_to_ascii(self):
        """Basic latin conversion results"""
        self.assertEqual(
            reduce.latin_to_ascii('Hélène Müller'),
            'Helene Muller')

    def test_german_latin_to_ascii(self):
        """German conversion results"""
        self.assertEqual(
            reduce.latin_to_ascii('Hélène Müller',
                                  reduce.GERMAN_OVERRIDES),
            'Helene Mueller')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
