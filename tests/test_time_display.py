# -*- coding: utf-8 -*-

"""

test smallparts.time_display

"""

import unittest

from datetime import datetime, timedelta

from smallparts import time_display


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_as_specified(self):
        """Datetime display as specified"""
        self.assertEqual(
            time_display._as_specified(
                datetime(2020, 7, 31, 23, 59, 30, 357921)),
            '2020-07-31 23:59:30')
        self.assertEqual(
            time_display._as_specified(
                datetime(2020, 7, 31, 23, 59, 30, 357921),
                with_msec=True),
            '2020-07-31 23:59:30.357')
        self.assertEqual(
            time_display._as_specified(
                datetime(2020, 7, 31, 23, 59, 30, 357921),
                with_usec=True),
            '2020-07-31 23:59:30.357921')

    def test_as_date(self):
        """Datetime display as date"""
        self.assertEqual(
            time_display.as_date(
                datetime(2020, 7, 31, 23, 59, 30, 357921)),
            '2020-07-31')

    def test_as_datetime(self):
        """Datetime display as datetime"""
        self.assertEqual(
            time_display.as_datetime(
                datetime(2020, 7, 31, 23, 59, 30, 357921),
                with_usec=True),
            '2020-07-31 23:59:30.357921')

    def test_as_time(self):
        """Datetime display as time"""
        self.assertEqual(
            time_display.as_time(
                datetime(2020, 7, 31, 23, 59, 30, 357921),
                with_msec=True),
            '23:59:30.357')

    def test_pretty_printed_timedelta(self):
        """Pretty printed timedelta"""
        self.assertEqual(
            time_display.pretty_printed_timedelta(
                timedelta(seconds=1800000),
                lang='en'),
            '2 weeks and 6 days')
        self.assertEqual(
            time_display.pretty_printed_timedelta(
                timedelta(seconds=180157),
                lang='fr'),
            '2 jours et 2 heures')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
