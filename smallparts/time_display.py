# -*- coding: utf-8 -*-

"""

smallparts.time_display - time representation functions

"""


from smallparts.l10n import enumerations as ln_enum
from smallparts.l10n import time_indications as ln_time


FS_DATE = '%Y-%m-%d'
FS_TIME = '%H:%M:%S'
FS_DATETIME = '{0} {1}'.format(FS_DATE, FS_TIME)
FS_USEC = '{0}.%f'
FS_MSEC = '{0}.{1:03d}'
FS_DATETIME_WITH_USEC = FS_USEC.format(FS_DATETIME)
FS_TIME_WITH_USEC = FS_USEC.format(FS_TIME)

SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
DAYS_PER_WEEK = 7

DEFAULT_DISPLAY_LIMITS = {
    ln_time.SECONDS: 60 * SECONDS_PER_MINUTE,
    ln_time.MINUTES: 24 * MINUTES_PER_HOUR,
    ln_time.HOURS: 7 * HOURS_PER_DAY,
    ln_time.DAYS: 4 * DAYS_PER_WEEK}


def _as_specified(datetime_object,
                  format_string=FS_DATETIME,
                  with_msec=False,
                  with_usec=False):
    """Return the datetime object formatted as specified"""
    if with_usec:
        return datetime_object.strftime(FS_USEC.format(format_string))
    #
    if with_msec:
        msec = datetime_object.microsecond // 1000
        return FS_MSEC.format(datetime_object.strftime(format_string), msec)
    # implicit else:
    return datetime_object.strftime(format_string)


def as_date(datetime_object):
    """Return the datetime object formatted as date"""
    return datetime_object.strftime(FS_DATE)


def as_datetime(datetime_object, with_msec=False, with_usec=False):
    """Return the datetime object formatted as datetime,
    convenience wrapper around _as_specified
    """
    return _as_specified(datetime_object,
                         format_string=FS_DATETIME,
                         with_msec=with_msec,
                         with_usec=with_usec)


def as_time(datetime_object, with_msec=False, with_usec=False):
    """Return the datetime object formatted as time,
    convenience wrapper around _as_specified
    """
    return _as_specified(datetime_object,
                         format_string=FS_TIME,
                         with_msec=with_msec,
                         with_usec=with_usec)


def pretty_printed_timedelta(timedelta, limits=None, lang=None):
    """Return the timedelta, pretty printed
    and regarding the limits per time component
    """
    result = []
    limits = limits or {}
    totals = {}
    values = {}
    totals[ln_time.SECONDS] = int(timedelta.total_seconds())
    previous_unit = ln_time.SECONDS
    for current_unit, conversion_factor in (
            (ln_time.MINUTES, SECONDS_PER_MINUTE),
            (ln_time.HOURS, MINUTES_PER_HOUR),
            (ln_time.DAYS, HOURS_PER_DAY),
            (ln_time.WEEKS, DAYS_PER_WEEK)):
        totals[current_unit], values[previous_unit] = divmod(
            totals[previous_unit], conversion_factor)
        if values[previous_unit] and \
                totals[previous_unit] < limits.get(
                        previous_unit,
                        DEFAULT_DISPLAY_LIMITS[previous_unit]):
            tc_kwargs = {previous_unit: values[previous_unit],
                         'lang': lang}
            result.append(
                ln_time.pretty_print_component(**tc_kwargs))
        #
        if not totals[current_unit]:
            break
        previous_unit = current_unit
    #
    if totals.get(ln_time.WEEKS):
        result.append(
            ln_time.pretty_print_component(weeks=totals[ln_time.WEEKS],
                                           lang=lang))
    #
    return ln_enum.enumeration(result[::-1], ln_enum.AND, lang=lang)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
