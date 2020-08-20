# -*- coding: utf-8 -*-

"""

smallparts.time_display - time representation functions

"""


from smallparts.l10n import enumerations
from smallparts.l10n import time_indications


def _as_specified(datetime_object,
                  format_string,
                  with_msec=False,
                  with_usec=False):
    """Return the datetime object formatted as specified"""
    if with_usec:
        return datetime_object.strftime(
            '{0}.%f'.format(format_string))
    #
    if with_msec:
        msec = datetime_object.microsecond // 1000
        return '{0}.{1:03d}'.format(
            datetime_object.strftime(format_string),
            msec)
    # implicit else:
    return datetime_object.strftime(format_string)


def as_date(datetime_object):
    """Return the datetime object formatted as date"""
    return datetime_object.strftime('%Y-%m-%d')


def as_datetime(datetime_object, with_msec=False, with_usec=False):
    """Return the datetime object formatted as datetime,
    convenience wrapper around _as_specified
    """
    return _as_specified(datetime_object,
                         '%Y-%m-%d %H:%M:%S',
                         with_msec=with_msec,
                         with_usec=with_usec)


def as_time(datetime_object, with_msec=False, with_usec=False):
    """Return the datetime object formatted as time,
    convenience wrapper around _as_specified
    """
    return _as_specified(datetime_object,
                         '%H:%M:%S',
                         with_msec=with_msec,
                         with_usec=with_usec)


class TimedeltaPrettyPrinter():

    """Create a function to pretty print timedeltas"""

    units = (
        time_indications.WEEKS,
        time_indications.DAYS,
        time_indications.HOURS,
        time_indications.MINUTES,
        time_indications.SECONDS)

    conversion_factors = (
        (time_indications.MINUTES, 60),
        (time_indications.HOURS, 60),
        (time_indications.DAYS, 24),
        (time_indications.WEEKS, 7))

    def __init__(self, seconds=3600, minutes=1440, hours=168, days=70):
        """Set the limits mapping from the arguments."""
        self.limits = dict(seconds=seconds,
                           minutes=minutes,
                           hours=hours,
                           days=days,
                           weeks=None)
        remove_limits = False
        for current_unit in reversed(self.units):
            if remove_limits:
                self.limits[current_unit] = None
            elif not self.limits[current_unit]:
                remove_limits = True
            #
        #

    @classmethod
    def get_components(cls, timedelta_object):
        """Return a tuple of two dicts containing
        totals and values for the timedelta's components
        (seconds, minutes, hours, days and weeks)
        """
        values = {}
        totals = dict(seconds=int(timedelta_object.total_seconds()))
        previous_unit = time_indications.SECONDS
        for current_unit, conversion_factor in cls.conversion_factors:
            totals[current_unit], values[previous_unit] = divmod(
                totals[previous_unit], conversion_factor)
            previous_unit = current_unit
        #
        values[current_unit] = totals[current_unit]
        return (totals, values)

    def __call__(self, timedelta_object, lang='en'):
        """Pretty print the given timedelta object in the
        given language, regarding the limits.
        """
        totals, values = self.get_components(timedelta_object)
        printed_components = []
        for current_unit in self.units:
            if values[current_unit]:
                if self.limits[current_unit]:
                    if totals[current_unit] > self.limits[current_unit]:
                        continue
                    #
                #
                printed_components.append(
                    time_indications.pretty_print_component(
                        **{current_unit: values[current_unit],
                           'lang': lang}))
            #
        #
        return enumerations.enumeration(
            printed_components,
            enumerations.AND,
            lang=lang)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
