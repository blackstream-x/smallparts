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

# Invalid, restricted and discouraged codepoints, see
# <https://www.w3.org/TR/2006/REC-xml-20060816/Overview.html#charsets>
# for XML 1.0 and
# <https://www.w3.org/TR/xml11/Overview.html#charsets>
# for XML 1.1

INVALID = 'invalid'
RESTRICTED = 'restricted'
DISCOURAGED = 'discouraged'

SUPPORTED_CHARACTER_REMOVALS = (INVALID, RESTRICTED, DISCOURAGED)

SUPPORTED_XML_VERSIONS = (constants.XML_1_0, constants.XML_1_1)

RESTRICTED_C0_CONTROLS = \
    tuple(range(0x1, 0x9)) + (0xb, 0xc) + tuple(range(0xe, 0x20))
RESTRICTED__IN_XML_1_0 = \
    tuple(range(0x7f, 0x85)) + tuple(range(0x86, 0xa0))
INVALID_IN_XML_1_1 = \
    (0x0,) + tuple(range(0xd800, 0xe000)) + (0xfffe, 0xffff)
INVALID_CODEPOINTS = {
    constants.XML_1_0: INVALID_IN_XML_1_1 + RESTRICTED_C0_CONTROLS,
    constants.XML_1_1: INVALID_IN_XML_1_1}
RESTRICTED_CODEPOINTS = {
    constants.XML_1_0: RESTRICTED__IN_XML_1_0,
    constants.XML_1_1: RESTRICTED__IN_XML_1_0 + RESTRICTED_C0_CONTROLS}
DISCOURAGED_CODEPOINTS = tuple(range(0xfdd0, 0xfde0)) + (
    0x1fffe, 0x1ffff, 0x2fffe, 0x2ffff, 0x3fffe, 0x3ffff,
    0x4fffe, 0x4ffff, 0x5fffe, 0x5ffff, 0x6fffe, 0x6ffff,
    0x7fffe, 0x7ffff, 0x8fffe, 0x8ffff, 0x9fffe, 0x9ffff,
    0xafffe, 0xaffff, 0xbfffe, 0xbffff, 0xcfffe, 0xcffff,
    0xdfffe, 0xdffff, 0xefffe, 0xeffff, 0xffffe, 0xfffff,
    0x10fffe, 0x10ffff)

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


def translate_to_charrefs(characters_sequence, source_text):
    """Return source_text with all characters from the
    characters sequence translated to their respective charrefs.
    """
    charrefs = {}
    for character in characters_sequence:
        codepoint = ord(character)
        charrefs[codepoint] = entity(codepoint)
    #
    return source_text.translate(charrefs)


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
    """Replace non-ascii characters by numeric entities"""
    ascii_bytes = source_text.encode('ascii',
                                     errors='xmlcharrefreplace')
    return ascii_bytes.decode()


def defuse(source_text,
           target_xml_version=constants.XML_1_0,
           remove=INVALID):
    """Defuse source_text in two steps for use as content of an XML element:
    1.) clean up the text by removing the specified codepoints:
        - None (requested explicitly by specifying remove=None)
        - Invalid codepoints as defined in the
          INVALID_CODEPOINTS[target_xml_version] tuple
          (this is the default, but could also be
           requested explicitly by specifying remove=INVALID)
        - Invalid codepoints as above AND
          restricted codepoints as defined in the
          RESTRICTED_CODEPOINTS[target_xml_version] tuple
          (requested explicitly by specifying remove=RESTRICTED)
        - Invalid AND restricted codepoints as above AND
          discouraged codepoints as defined in the
          (not XML version dependent) DISCOURAGED_CODEPOINTS tuple
          (requested explicitly by specifying remove=DISCOURAGED)
    2.) Escape special characters (<, > and &).
    """
    if target_xml_version not in SUPPORTED_XML_VERSIONS:
        raise ValueError(
            'target_xml_version must be one of {0!r}!'.format(
                SUPPORTED_XML_VERSIONS))
    #
    if remove is None:
        cleaned_up_source = source_text
    elif remove in SUPPORTED_CHARACTER_REMOVALS:
        remove_codepoints = dict.fromkeys(
            INVALID_CODEPOINTS[target_xml_version])
        if remove in (RESTRICTED, DISCOURAGED):
            remove_codepoints.update(
                dict.fromkeys(
                    RESTRICTED_CODEPOINTS[target_xml_version]))
            if remove == DISCOURAGED:
                remove_codepoints.update(
                    dict.fromkeys(DISCOURAGED_CODEPOINTS))
           #
        #
        cleaned_up_source = source_text.translate(remove_codepoints)
    else:
        raise ValueError(
            'remove must be None or one of {0!r}!'.format(
                SUPPORTED_CHARACTER_REMOVALS))

    #
    return xml.sax.saxutils.escape(cleaned_up_source)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
