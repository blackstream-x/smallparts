# -*- coding: utf-8 -*-

"""

smallparts.l10n.enumerations

Natural language enumerations

"""


from smallparts.l10n import languages

from smallparts.sequences import raw_join


BLANK = ' '
COMMA = ','
EMPTY = ''

AND = 'and'
OR = 'or'
EITHER = 'either'
NEITHER = 'neither'

DEFAULT = 'default'
EXCEPTIONS = 'exceptions'

BEFORE = 'before'
AFTER = 'after'

SUPPORTED_ENUMS = (AND, OR, EITHER, NEITHER)

# (prefix, joiner, last joiner)
ENUM_JOINERS = {
    languages.EN: {
        AND: (None, COMMA, AND),
        OR: (None, COMMA, OR),
        EITHER: (EITHER, COMMA, OR),
        NEITHER: (NEITHER, COMMA, 'nor')
    },
    languages.DE: {
        AND: (None, COMMA, 'und'),
        OR: (None, COMMA, 'oder'),
        EITHER: ('entweder', COMMA, 'oder'),
        NEITHER: ('weder', COMMA, 'noch')
    },
    languages.ES: {
        AND: (None, COMMA, 'y'),
        OR: (None, COMMA, 'o'),
        EITHER: ('ya sea', COMMA, 'o'),
        NEITHER: ('ni', COMMA, 'ni')
    },
    languages.FR: {
        AND: (None, COMMA, 'et'),
        OR: (None, COMMA, 'ou'),
        EITHER: ('soit', COMMA, 'ou'),
        NEITHER: ('ni', COMMA, 'ni')
    },
    '__test__': {AND: (None, None, None)}
}

# Spacing rules: (before, after)
SPACING_RULES = {
    languages.EN: {
        DEFAULT: (True, True),
        EXCEPTIONS: {BEFORE: {',;.:!?/': False},
                     AFTER: {'/': False}}
    },
    languages.DE: {
        DEFAULT: (True, True),
        EXCEPTIONS: {BEFORE: {',;.:!?': False}}
    },
    languages.ES: {
        DEFAULT: (True, True),
        EXCEPTIONS: {BEFORE: {',;.:!?': False}}
    },
    languages.FR: {
        DEFAULT: (True, True),
        EXCEPTIONS: {}
    },
    '__test__': {
        DEFAULT: (False, False),
        EXCEPTIONS: {}
    }
}

#
# Functions
#


def apply_spacing_rules(joiner, lang=None):
    """Apply language-specific spacing rules"""
    stripped_joiner = joiner.strip()
    if not stripped_joiner:
        return joiner
    #
    lang = lang or languages.DEFAULT
    try:
        spacing_rules = SPACING_RULES[lang]
    except KeyError:
        raise ValueError(
            languages.missing_translation(
                lang,
                message='No spacing rules available yet'
                'for {0!r}!'.format(lang)))
    #
    for (characters, rule_before) in spacing_rules[EXCEPTIONS].get(
            BEFORE, {}).items():
        if stripped_joiner[0] in characters:
            space_before = rule_before
            break
        #
    else:
        space_before = spacing_rules[DEFAULT][0]
    #
    for (characters, rule_after) in spacing_rules[EXCEPTIONS].get(
            AFTER, {}).items():
        if stripped_joiner[-1] in characters:
            space_after = rule_after
            break
        #
    else:
        space_after = spacing_rules[DEFAULT][-1]
    #
    prefix = suffix = EMPTY
    if space_before:
        prefix = BLANK
    #
    if space_after:
        suffix = BLANK
    #
    return EMPTY.join((prefix, stripped_joiner, suffix))


def enumeration(sequence, enum_type, lang=None):
    """Return the sequence enumerated according to the
    given enum_type and language
    """
    lang = lang or languages.DEFAULT
    try:
        enum_joiners = ENUM_JOINERS[lang]
    except KeyError:
        raise ValueError(languages.missing_translation(lang))
    else:
        try:
            prefix, joiner, final_joiner = enum_joiners[enum_type]
        except KeyError:
            raise ValueError(
                'No {0!r} translation available for {1!r}!'.format(
                    lang, enum_type))
        #
    #
    if joiner is None:
        joiner = COMMA
    #
    if final_joiner is None:
        final_joiner = joiner
    #
    if prefix:
        prefix = prefix.strip() + BLANK
    #
    return raw_join(
        sequence,
        prefix=prefix,
        joiner=apply_spacing_rules(joiner, lang=lang),
        final_joiner=apply_spacing_rules(final_joiner, lang=lang))


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
