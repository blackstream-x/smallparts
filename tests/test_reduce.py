# -*- coding: utf-8 -*-

"""

test smallparts.text.reduce

"""

import unittest

from smallparts.text import reduce


class TestSimple(unittest.TestCase):

    """Check the module"""

    def test_basic_latin_to_ascii(self):
        """Check conversion results"""
        self.assertEqual(
            reduce.latin_to_ascii('Hélène Müller'),
            'Helene Muller')

    def test_german_latin_to_ascii(self):
        """Check conversion results"""
        self.assertEqual(
            reduce.latin_to_ascii('Hélène Müller',
                                  reduce.GERMAN_OVERRIDES),
            'Helene Mueller')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
