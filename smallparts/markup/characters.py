# -*- coding: utf-8 -*-

"""

smallparts.markup.characters

Markup (HTML, XML) generation – Characters handling

"""


import unicodedata
import xml.sax.saxutils

from smallparts import constants


#
# Constants
#

# Keyword constants for the Defuser class

REMOVE_INVALID = 0
REMOVE_RESTRICTED = 1
REMOVE_DISCOURAGED = 2


#
# Classes
#


class Defuser():

    """Used to defuse a provided text:
    remove invalid and/or restricted and/or discouraged codepoints
    from the text and (XML-)escape the characters < > &
    (the latter is delegated to xml.sax.saxutils.escape()).
    """

    supported_xml_versions = (constants.XML_1_0,
                              constants.XML_1_1)
    supported_removals = (REMOVE_INVALID,
                          REMOVE_RESTRICTED,
                          REMOVE_DISCOURAGED)
    invalid_in_xml_1_1 = \
        (0x0,) + tuple(range(0xd800, 0xe000)) + (0xfffe, 0xffff)
    restricted_c0_controls = \
        tuple(range(0x1, 0x9)) + (0xb, 0xc) + tuple(range(0xe, 0x20))
    restricted_in_xml_1_0 = \
        tuple(range(0x7f, 0x85)) + tuple(range(0x86, 0xa0))

    codepoints = (
        {constants.XML_1_0: invalid_in_xml_1_1 + restricted_c0_controls,
         constants.XML_1_1: invalid_in_xml_1_1},
        {constants.XML_1_0: restricted_in_xml_1_0,
         constants.XML_1_1: restricted_in_xml_1_0 + restricted_c0_controls},
        tuple(range(0xfdd0, 0xfde0)) + (
            0x1fffe, 0x1ffff, 0x2fffe, 0x2ffff, 0x3fffe, 0x3ffff,
            0x4fffe, 0x4ffff, 0x5fffe, 0x5ffff, 0x6fffe, 0x6ffff,
            0x7fffe, 0x7ffff, 0x8fffe, 0x8ffff, 0x9fffe, 0x9ffff,
            0xafffe, 0xaffff, 0xbfffe, 0xbffff, 0xcfffe, 0xcffff,
            0xdfffe, 0xdffff, 0xefffe, 0xeffff, 0xffffe, 0xfffff,
            0x10fffe, 0x10ffff))

    def __init__(self,
                 xml_version=constants.XML_1_0,
                 remove=REMOVE_INVALID):
        """Build the translation dict"""
        if xml_version not in self.supported_xml_versions:
            raise ValueError(
                'xml_version must be one of {0!r}!'.format(
                    self.supported_xml_versions))
        #
        if remove not in self.supported_removals:
            if remove is None:
                raise ValueError(
                    'Please use the {0!r} class static method'
                    ' .escape() if you do not want to remove'
                    ' codepoints at all'.format(self.__class__.__name__))
            #
            raise ValueError(
                'remove must be one of {0!r}!'.format(
                    self.supported_removals))
        #
        self.__removable_codepoints = dict.fromkeys(
            self.codepoints[REMOVE_INVALID][xml_version])
        if remove >= REMOVE_RESTRICTED:
            self.__removable_codepoints.update(
                dict.fromkeys(
                    self.codepoints[REMOVE_RESTRICTED][xml_version]))
        #
        if remove >= REMOVE_DISCOURAGED:
            self.__removable_codepoints.update(
                dict.fromkeys(
                    self.codepoints[REMOVE_DISCOURAGED]))
        #

    @staticmethod
    def escape(source_text):
        """Wrap xml.sax.saxutils.escape()"""
        return xml.sax.saxutils.escape(source_text)

    def remove_codepoints(self, source_text):
        """Remove codepoints as specified at instantiation time"""
        return source_text.translate(self.__removable_codepoints)

    def defuse(self, source_text):
        """Remove codepoints as specified at instantiation time,
        and escape the remaining characters
        """
        return self.escape(self.remove_codepoints(source_text))


#
# Functions
#


def encode_to_charrefs(source_text):
    """Replace non-ascii characters by numeric entities"""
    ascii_bytes = source_text.encode('ascii',
                                     errors='xmlcharrefreplace')
    return ascii_bytes.decode()


def entity(reference):
    """Return a numeric (&#reference;) or symbolic: (&reference;) entity,
    depending on the reference's type
    """
    try:
        return '&#{0:d};'.format(reference)
    except ValueError:
        return '&{0};'.format(reference)
    #


def charref_from_name(unicode_character_name):
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


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
