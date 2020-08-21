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
                datetime(2020, 7, 31, 23, 59, 30, 357921),
                '%Y-%m-%d %H:%M:%S'),
            '2020-07-31 23:59:30')
        self.assertEqual(
            time_display._as_specified(
                datetime(2020, 7, 31, 23, 59, 30, 357921),
                '%Y-%m-%d %H:%M:%S',
                with_msec=True),
            '2020-07-31 23:59:30.357')
        self.assertEqual(
            time_display._as_specified(
                datetime(2020, 7, 31, 23, 59, 30, 357921),
                '%Y-%m-%d %H:%M:%S',
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

    def test_timedelta_formatter(self):
        """Formatted timedeltas"""
        ltdf = time_display.LooseTimedeltaFormatter()
        self.assertEqual(
            ltdf(
                timedelta(seconds=1800000),
                lang='en'),
            '2 weeks and 6 days')
        ltdf_no_limits = time_display.LooseTimedeltaFormatter(seconds=None)
        self.assertEqual(
            ltdf_no_limits(
                timedelta(seconds=180157),
                lang='fr'),
            '2 jours , 2 heures , 2 minutes et 37 secondes')
        self.assertEqual(
            ltdf_no_limits(
                timedelta(seconds=79542),
                lang='de'),
            '22 Stunden, 5 Minuten und 42 Sekunden')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
