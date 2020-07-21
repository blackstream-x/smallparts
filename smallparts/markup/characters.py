# -*- coding: utf-8 -*-

"""

smallparts.markup.characters

Markup (HTML, XML) generation and parsing - Character and entity handling

"""


import html.entities
import re
import unicodedata
import xml.sax.saxutils

from smallparts import constants


BASE_HEX = 16

FS_ENTITY = '&{0};'
FS_HEX_PREFIX = '0{0}'
FS_NUMERIC_ENTITY = FS_ENTITY.format('#{0:d}')

PREFIX_HEX_CHARREF = 'x'

PRX_NAMED_ENTITY = re.compile(
    FS_ENTITY.format(r'([a-z]\w+?)'))
PRX_NUMERIC_ENTITY = re.compile(
    FS_ENTITY.format(r'#(\d+|x[\da-f]+)'))

V10 = '1.0'
V11 = '1.1'

# Invalid and restricted code points, see
# <https://www.w3.org/TR/2006/REC-xml-20060816/Overview.html#charsets>
# for XML 1.0 and
# <https://www.w3.org/TR/xml11/Overview.html#charsets>
# for XML 1.1

RESTRICTED_C0 = list(range(0x1, 0x9)) + [0xb, 0xc] + list(range(0xe, 0x20))

INVALID_CODEPOINTS = {
    V11: [0x0] + list(range(0xd800, 0xe000)) + [0xfffe, 0xffff]}
RESTRICTED_CODEPOINTS = {
    V10: list(range(0x7f, 0x85)) + list(range(0x86, 0xa0))}
INVALID_CODEPOINTS[V10] = sorted(INVALID_CODEPOINTS[V11] + RESTRICTED_C0)
RESTRICTED_CODEPOINTS[V11] = RESTRICTED_C0 + RESTRICTED_CODEPOINTS[V10]

#
#
#


def entity(reference):
    """Return a numeric (&#reference;) or symbolic: (&reference;) entity,
    depending on the reference's type
    """
    try:
        return FS_NUMERIC_ENTITY.format(reference)
    except ValueError:
        return FS_ENTITY.format(reference)
    #


def entity_from_name(unicode_character_name):
    """Return the numeric (&#reference;) entity
    for the given unicode character name
    """
    return entity(ord(unicodedata.lookup(unicode_character_name)))


def replace_by_charref(character, source_text):
    """Replace all occurrences of character in source_text
    by the mathing numeric entity
    """
    return source_text.replace(character, entity(ord(character)))


def resolve_single_charref(charref_number):
    """Resolve a numeric character reference (decimal or hex)
    and return the matching unicode character
    """
    if charref_number.lower().startswith(PREFIX_HEX_CHARREF):
        codepoint = int(FS_HEX_PREFIX.format(charref_number), BASE_HEX)
    else:
        codepoint = int(charref_number)
    return chr(codepoint)


def resolve_single_entityref(entity_name):
    """Resolve a named entity reference
    and return the matching unicode character
    """
    return chr(html.entities.name2codepoint[entity_name])


def resolve_matched_charref(match_object):
    """Return the unicode character from the matched numeric charref
    when using PRX_NUMERIC_ENTITY
    """
    return resolve_single_charref(match_object.group(constants.SECOND_INDEX))


def resolve_matched_entityref(match_object):
    """Return the unicode character from the matched named entity
    (using PRX_NAMED_ENTITY),
    or return the original string if no such entity is defined"""
    entity_name = match_object.group(constants.SECOND_INDEX)
    try:
        return resolve_single_entityref(entity_name)
    except KeyError:
        return match_object.group(constants.FIRST_INDEX)


def resolve_all_charrefs(source_text):
    """Resolve all numeric character references"""
    return PRX_NUMERIC_ENTITY.sub(resolve_matched_charref,
                                  source_text)


def resolve_all_entityrefs(source_text):
    """Resolve all character references"""
    return PRX_NAMED_ENTITY.sub(resolve_matched_entityref,
                                resolve_all_charrefs(source_text))


def encode_to_charrefs(source_text):
    """Replace non-ascii characters by numeric entities,
    return unicode
    """
    ascii_bytes = source_text.encode('ascii',
                                     errors='xmlcharrefreplace')
    return ascii_bytes.decode()


def defuse(source_text, target_xml_version=V10, remove_restricted=False):
    """Defuse source_text for use as content of an XML element:
    Remove invalid codepoints and, if requested also restricted ones.
    Escape special characters (<, > and &).
    """
    try:
        remove_codepoints = dict.fromkeys(
            INVALID_CODEPOINTS[target_xml_version])
    except KeyError:
        raise ValueError(
            'target_xml_version must be {0!r} or {1!r}'.format(V10, V11))
    #
    if remove_restricted:
        remove_codepoints.update(
            dict.fromkeys(RESTRICTED_CODEPOINTS[target_xml_version]))
    #
    return xml.sax.saxutils.escape(source_text.translate(remove_codepoints))


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
