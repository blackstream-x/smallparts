# -*- coding: utf-8 -*-

"""

test smallparts.text.split

"""

import unittest

from smallparts.text import split


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_with_trailing_newline(self):
        """Text including a trailing newline"""
        self.assertEqual(
            split.lines_for_reconstruction(
                'first,\nsecond and\nthird line\n'),
            ['first,', 'second and', 'third line', ''])

    def test_without_trailing_newline(self):
        """Text not ending in a newline"""
        self.assertEqual(
            split.lines_for_reconstruction(
                'first,\nsecond and\nthird line'),
            ['first,', 'second and', 'third line'])

    def test_unsupported_type(self):
        """Unsuppoerted type (here: bytes)"""
        self.assertRaises(
            TypeError,
            split.lines_for_reconstruction,
            b'first,\nsecond and\nthird line')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
