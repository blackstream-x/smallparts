# -*- coding: utf-8 -*-

"""

smallparts.markup.entities

Markup (HTML, XML) generation and parsing - Entities

"""


import html.entities
import unicodedata

from smallparts import constants



BASE_HEX = 16

FS_ENTITY = '&{0};'
FS_HEX_PREFIX = '0{0}'
FS_NUMERIC_ENTITY = FS_ENTITY.format('#{0}')

PREFIX_HEX_CHARREF = 'x'


def entity(reference):
    """Return a numeric (&#reference;) or symbolic: (&reference;) entity,
    depending on the reference's type
    """
    try:
        return FS_NUMERIC_ENTITY.format(int(reference))
    except ValueError:
        return FS_ENTITY.format(reference)
    #


def entity_from_name(unicode_character_name):
    """Return the numeric (&#reference;) entity
    for the given unicode character name
    """
    return entity(ord(unicodedata.lookup(unicode_character_name)))


def replace_by_entity(input_string, character):
    """Replace all occurrences of character in input_string
    by the mathing numeric entity
    """
    return input_string.replace(character, entity(ord(character)))


def resolve_charref(charref_number):
    """Resolve a numeric character reference (decimal or hex)
    and return the matching unicode character
    """
    if charref_number.lower().startswith(PREFIX_HEX_CHARREF):
        codepoint = int(FS_HEX_PREFIX.format(charref_number), BASE_HEX)
    else:
        codepoint = int(charref_number)
    return chr(codepoint)


def resolve_entityref(entity_name):
    """Resolve a named entity reference
    and return the matching unicode character
    """
    return chr(html.entities.name2codepoint[entity_name])


def resolve_matched_entityref(match_object):
    """Return the unicode character from the matched named entity,
    or return the original string if no such entity is defined"""
    entity_name = match_object.group(constants.SECOND_INDEX)
    try:
        return resolve_entityref(entity_name)
    except KeyError:
        return match_object.group(constants.FIRST_INDEX)


def resolve_matched_charref(match_object):
    """Return the unicode character from the matched numeric charref"""
    return resolve_charref(match_object.group(constants.SECOND_INDEX))


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
