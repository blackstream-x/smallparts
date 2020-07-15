# -*- coding: utf-8 -*-

"""

test smallparts.constants

"""

import unittest

from smallparts import constants


class TestSimple(unittest.TestCase):

    """Test the constants module"""

    def test_constants(self):
        """Check one constant value"""
        self.assertEqual(constants.CRLF, '\r\n')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
