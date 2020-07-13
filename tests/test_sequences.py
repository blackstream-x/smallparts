# -*- coding: utf-8 -*-

"""

test smallparts.sequences

"""

import unittest

from smallparts import sequences


class TestSimple(unittest.TestCase):

    """Check the module"""

    def test_flatten(self):
        """Check flattening a list with unlimited recursion"""
        source_list = [1, [2, [3, [4, [5, 6], 7], 8], 9], 10]
        self.assertEqual(
            sequences.flatten(source_list),
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_flatten_with_depth(self):
        """Check flattening a list with given depth"""
        source_list = [1, [2, [3, [4, [5, 6], 7], 8], 9], 10]
        self.assertEqual(
            sequences.flatten(source_list, depth=2),
            [1, 2, 3, [4, [5, 6], 7], 8, 9, 10])


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
