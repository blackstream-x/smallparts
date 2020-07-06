# -*- coding: utf-8 -*-

"""

smallparts.time_display - time representation functions

"""


from smallparts import text


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

SECONDS = 'seconds'
MINUTES = 'minutes'
HOURS = 'hours'
DAYS = 'days'
WEEKS = 'weeks'

DEFAULT_DISPLAY_LIMITS = {
    SECONDS: 60 * SECONDS_PER_MINUTE,
    MINUTES: 24 * MINUTES_PER_HOUR,
    HOURS: 7 * HOURS_PER_DAY,
    DAYS: 4 * DAYS_PER_WEEK}


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


def units(amount, singular_form, plural_form):
    """Return the matching pretty-printed form for the amount of units"""
    if amount == 1:
        matching_form = singular_form
    else:
        matching_form = plural_form
    #
    return '{0} {1}'.format(amount, matching_form)


def time_component(seconds=None,
                   minutes=None,
                   hours=None,
                   days=None,
                   weeks=None):
    """Return the time component, pretty printed"""
    if seconds is not None:
        value, singular, plural = seconds, 'Sekunde', 'Sekunden'
    elif minutes is not None:
        value, singular, plural = minutes, 'Minute', 'Minuten'
    elif hours is not None:
        value, singular, plural = hours, 'Stunde', 'Stunden'
    elif days is not None:
        value, singular, plural = days, 'Tag', 'Tage'
    elif weeks is not None:
        value, singular, plural = weeks, 'Woche', 'Wochen'
    else:
        raise ValueError('Bitte eine Zeiteinheit angeben!')
    #
    return units(value, singular, plural)


def pretty_printed_timedelta(timedelta, limits=None):
    """Return the timedelta, pretty printed
    and regarding the limits per time component
    """
    result = []
    limits = limits or {}
    totals = {}
    values = {}
    totals[SECONDS] = int(timedelta.total_seconds())
    previous_unit = SECONDS
    for current_unit, conversion_factor in (
            (MINUTES, SECONDS_PER_MINUTE),
            (HOURS, MINUTES_PER_HOUR),
            (DAYS, HOURS_PER_DAY),
            (WEEKS, DAYS_PER_WEEK)):
        totals[current_unit], values[previous_unit] = divmod(
            totals[previous_unit], conversion_factor)
        if values[previous_unit] and \
                totals[previous_unit] < limits.get(
                        previous_unit,
                        DEFAULT_DISPLAY_LIMITS[previous_unit]):
            tc_kwargs = {previous_unit: values[previous_unit]}
            result.append(time_component(**tc_kwargs))
        #
        if not totals[current_unit]:
            break
        previous_unit = current_unit
    #
    if totals.get(WEEKS):
        result.append(time_component(weeks=totals[WEEKS]))
    #
    return text.enumeration(result[::-1])


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
