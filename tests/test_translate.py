# -*- coding: utf-8 -*-

"""

test smallparts.text.translate

"""

import unittest

from smallparts.text import translate


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_remove_trailing_underscores(self):
        """Text including a trailing newline"""
        self.assertEqual(
            translate.remove_trailing_underscores('__main__'),
            '__main')

    def test_underscores_to_dashes(self):
        """Text including a trailing newline"""
        self.assertEqual(
            translate.underscores_to_dashes('Snake_case_text_example'),
            'Snake-case-text-example')

    def test_underscores_to_blanks(self):
        """Text including a trailing newline"""
        self.assertEqual(
            translate.underscores_to_blanks('Snake_case_text_example'),
            'Snake case text example')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
