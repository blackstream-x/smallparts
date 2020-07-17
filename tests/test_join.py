# -*- coding: utf-8 -*-

"""

test smallparts.text.join

"""

import unittest

from smallparts.text import join


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_by_blanks(self):
        """Parts joined by blanks"""
        self.assertEqual(
            join.by_blanks('parts', 'of', 'a', 'sentence'),
            'parts of a sentence')

    def test_directlys(self):
        """Parts joined directly"""
        self.assertEqual(
            join.directly('Words', 'For', 'Camel', 'Case'),
            'WordsForCamelCase')

    def test_by_newlines(self):
        """Parts joined by newlines"""
        self.assertEqual(
            join.by_newlines('first,', 'second and', 'third line'),
            'first,\nsecond and\nthird line')

    def test_by_crlf(self):
        """Parts joined by CRLF"""
        self.assertEqual(
            join.by_crlf('first,', 'second and', 'third DOS file line'),
            'first,\r\nsecond and\r\nthird DOS file line')

    def test_using(self):
        """Parts joined using the provided string"""
        self.assertEqual(
            join.using('<->', 'one', 'two', 'four'),
            'one<->two<->four')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
