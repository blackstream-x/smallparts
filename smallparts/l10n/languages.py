# -*- coding: utf-8 -*-

"""

smallparts.l10n.languages

(Natural) language definitions

"""


DE = 'de'
EN = 'en'
ES = 'es'
FR = 'fr'

DEFAULT = EN
SUPPORTED = {DE, EN, ES, FR}


def missing_translation(lang, message=None):
    """Return an explanation if a language is not supported at all
    or if the translation is missing, to be used as a message for
    a ValuError which is raised in that case.
    """
    if lang not in SUPPORTED:
        return 'Language {0!r} not supported!'.format(lang)
    #
    return message or 'No {0!r} translation available yet!'.format(lang)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
