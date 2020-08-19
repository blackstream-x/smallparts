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

BEFORE = 'before'
AFTER = 'after'

WITHOUT_EXCEPTION = frozenset()

SUPPORTED_ENUMS = (AND, OR, EITHER, NEITHER)

# Separators for enumerations: (prefix, separator, last separator)
ENUM_SEPARATORS = {
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

# Spacing rules: BEFORE|AFTER: (generic rule, exceptions)
SPACING_RULES = {
    languages.EN: {
        BEFORE: (True, ',;.:!?/'),
        AFTER: (True, '/')
    },
    languages.DE: {
        BEFORE: (True, ',;.:!?'),
        AFTER: (True, WITHOUT_EXCEPTION)
    },
    languages.ES: {
        BEFORE: (True, ',;.:!?'),
        AFTER: (True, WITHOUT_EXCEPTION)
    },
    languages.FR: {
        BEFORE: (True, WITHOUT_EXCEPTION),
        AFTER: (True, WITHOUT_EXCEPTION)
    },
    '__test__': {
        BEFORE: (False, WITHOUT_EXCEPTION),
        AFTER: (False, WITHOUT_EXCEPTION)
    }
}


#
# Functions
#


def apply_spacing_rules(separator, lang=languages.DEFAULT):
    """Apply language-specific spacing rules"""
    stripped_separator = separator.strip()
    if not stripped_separator:
        return separator
    #
    try:
        spacing_rules = SPACING_RULES[lang]
    except KeyError:
        raise ValueError(
            languages.missing_translation(
                lang,
                message='No spacing rules available yet'
                'for {0!r}!'.format(lang)))
    #
    space = {}
    for character_index, position in ((0, BEFORE), (-1, AFTER)):
        generic_rule, exceptions = spacing_rules[position]
        if stripped_separator[character_index] in exceptions:
            space[position] = EMPTY if generic_rule else BLANK
        else:
            space[position] = BLANK if generic_rule else EMPTY
        #
    #
    return EMPTY.join((space[BEFORE], stripped_separator, space[AFTER]))


def enumeration(sequence, enum_type, lang=languages.DEFAULT):
    """Return the sequence enumerated according to the
    given enum_type and language
    """
    try:
        enum_separators = ENUM_SEPARATORS[lang]
    except KeyError:
        raise ValueError(languages.missing_translation(lang))
    else:
        try:
            prefix, separator, final_separator = enum_separators[enum_type]
        except KeyError:
            raise ValueError(
                'No {0!r} translation available for {1!r}!'.format(
                    lang, enum_type))
        #
    #
    if separator is None:
        separator = COMMA
    #
    if final_separator is None:
        final_separator = separator
    #
    if prefix:
        prefix = prefix.strip() + BLANK
    #
    return raw_join(
        sequence,
        prefix=prefix,
        separator=apply_spacing_rules(separator, lang=lang),
        final_separator=apply_spacing_rules(final_separator, lang=lang))


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
