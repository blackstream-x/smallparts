# -*- coding: utf-8 -*-

"""

smallparts.markup.translations

Markup "translations"

"""


import re
import xml.sax.saxutils

from smallparts import constants

from smallparts.markup import entities
from smallparts.text import transcode
from smallparts.text import translate


#
# Constants
#


INVALID_XML_CODEPOINTS = list(range(0, 9)) + list(range(11, 32)) + [127]
XML_REPLACEMENTS = dict(
    (chr(codepoint), entities.entity(codepoint))
    for codepoint in (34, 39, 60, 62, 91, 93))
XML_REPLACEMENTS.update(dict.fromkeys(
    [chr(codepoint) for codepoint in INVALID_XML_CODEPOINTS],
    constants.EMPTY))


def escape(data):
    """Wrap the xml.sax.saxutils.escape function"""
    return xml.sax.saxutils.escape(data)


def unescape(data):
    """Wrap the xml.sax.saxutils.escape function"""
    return xml.sax.saxutils.unescape(data)


#
#
#


class Translation():

    """Translations class, providing some standard classmethods"""

    amp_text = constants.AMPERSAND
    amp_xml = escape(amp_text)
    prx_named_entity = re.compile(
        entities.FS_ENTITY.format(r'([a-z]\w+?)'))
    prx_numeric_entity = re.compile(
        entities.FS_NUMERIC_ENTITY.format(r'(\d+|x[\da-f]+)'))
    # staticmethod attached to the class
    defuse_to_xml = translate.MakeTranslationFunction(XML_REPLACEMENTS)

    @classmethod
    def ampersand_to_xml(cls, input_string):
        """Encode ampersand to named entity"""
        return input_string.replace(constants.AMPERSAND, cls.amp_xml)

    @classmethod
    def ampersand_from_xml(cls, input_string):
        """Decode ampersand from named entity"""
        return input_string.replace(cls.amp_xml, constants.AMPERSAND)

    @classmethod
    def to_xmlentities_encoded(cls, input_string):
        """Return the result of ascii encoding the input string,
        with all non-ascii characters replaced by numeric entities.
        """
        return input_string.encode('ascii', 'xmlcharrefreplace')

    @classmethod
    def to_xmlentities(cls, input_string):
        """Replace non-ascii characters by numeric entities,
        return unicode
        """
        return transcode.to_unicode(
            cls.to_xmlentities_encoded(input_string))

    @classmethod
    def from_xmlentities(cls, input_string):
        """Resolve numeric XML entities only"""
        return cls.prx_numeric_entity.sub(entities.resolve_matched_charref,
                                          input_string)

    @classmethod
    def full_xml_encode(cls, input_string):
        """Replace characters with named or numeric entities
        where appropriate
        """
        return cls.to_xmlentities(
            cls.defuse_to_xml(cls.ampersand_to_xml(input_string)))

    @classmethod
    def full_xml_decode(cls, input_string):
        """Resolve all named and numeric XML entities"""
        return cls.prx_named_entity.sub(entities.resolve_matched_entityref,
                                        cls.from_xmlentities(input_string))


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
