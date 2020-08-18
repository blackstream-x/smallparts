# -*- coding: utf-8 -*-

"""

smallparts.l10n.time_indications

Time indication translations

"""


from smallparts.l10n import languages


SECONDS = 'seconds'
MINUTES = 'minutes'
HOURS = 'hours'
DAYS = 'days'
WEEKS = 'weeks'
MONTHS = 'months'
YEARS = 'years'

SUPPORTED_UNITS = (SECONDS, MINUTES, HOURS, DAYS,
                   WEEKS, MONTHS, YEARS)


# Singular and plural forms for time units
NUMBER_CATEGORIES = {
    languages.EN: {
        SECONDS: ('second', SECONDS),
        MINUTES: ('minute', MINUTES),
        HOURS: ('hour', HOURS),
        DAYS: ('day', DAYS),
        WEEKS: ('week', WEEKS),
        MONTHS: ('month', MONTHS),
        YEARS: ('year', YEARS)
    },
    languages.DE: {
        SECONDS: ('Sekunde', 'Sekunden'),
        MINUTES: ('Minute', 'Minuten'),
        HOURS: ('Stunde', 'Stunden'),
        DAYS: ('Tag', 'Tage'),
        WEEKS: ('Woche', 'Wochen'),
        MONTHS: ('Monat', 'Monate'),
        YEARS: ('Jahr', 'Jahre')
    },
    languages.ES: {
        SECONDS: ('segundo', 'segundos'),
        MINUTES: ('minuto', 'minutos'),
        HOURS: ('hora', 'horas'),
        DAYS: ('día', 'dias'),
        WEEKS: ('semana', 'semanas'),
        MONTHS: ('mes', 'meses'),
        YEARS: ('año', 'años')
    },
    languages.FR: {
        SECONDS: ('seconde', 'secondes'),
        MINUTES: ('minute', 'minutes'),
        HOURS: ('heure', 'heures'),
        DAYS: ('jour', 'jours'),
        WEEKS: ('semaine', 'semaines'),
        MONTHS: ('mois', 'mois'),
        YEARS: ('an', 'ans')
    }
}


#
# Functions
#


def pretty_print_component(lang=languages.DEFAULT, **kwargs):
    """Return the time component,
    pretty printed in singular or plural form
    in the language selected by lang=...
    """
    try:
        number_category = NUMBER_CATEGORIES[lang]
    except KeyError:
        raise ValueError(languages.missing_translation(lang))
    #
    for unit in SUPPORTED_UNITS:
        amount = kwargs.get(unit)
        if amount is not None:
            singular, plural = number_category[unit]
            if amount == 1:
                matching_form = singular
            else:
                matching_form = plural
            #
            break
        #
    else:
        raise ValueError('Please specify an amount of time as keyword'
                         ' argument {0!r}!'.format(SUPPORTED_UNITS))
    #
    return '{0} {1}'.format(amount, matching_form)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
