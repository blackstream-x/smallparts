# -*- coding: utf-8 -*-

"""

smallparts.markup.parsers

Markup parsing

"""


import html.parser
import re

from smallparts import constants


#
# Constants
#

# Keyword constants for the HtmlTagStripper class

IMAGES_WITH_ALT_TEXT_ONLY = 'images with alt text only'


#
# Classes
#


class EntityResolver():

    """Resolve entities"""

    # Map xml emtity names to codepoints
    xml_name2codepoint = {
        'lt': 60,
        'gt': 62,
        'amp': 38,
        'apos': 39,
        'quot': 34
    }
    # Numeric character references:
    # <https://www.w3.org/TR/xml/#NT-CharRef>
    re_charref = r'#(?:[0-9]+|x[0-9a-fA-F]+)'
    # Entity names: see <https://www.w3.org/TR/xml/#NT-NameStartChar>
    # and https://www.w3.org/TR/xml/#NT-NameChar
    re_name_start_char = (
        r':A-Z_a-z\xc0-\xd6\xd8-\xf6\xf8-\u02ff\u0370-\u037d\u037f-\u1fff'
        r'\u200c-\u200d\u2070-\u218f\u2c00-\u2fef\u3001-\ud7ff'
        r'\uf900-\ufdcf\ufdf0-\ufffd\U00010000-\U000effff')
    re_name_char = '-' + re_name_start_char + \
        r'\.0-9\xb7\u0300-\u036f\u203f-\u2040'

    def __init__(self, named_entities=None):
        """Precompile the regular expression matching all entity references.
        Allocate the internal named entities mapping from the provided
        named_entities mapping, default to XML_NAME2CODEPOINT.
        """
        self.__prx_entity = re.compile(
            '&([{0}][{1}]+|{2});'.format(
                self.re_name_start_char,
                self.re_name_char,
                self.re_charref))
        self.__named_entities = {}
        try:
            self.set_named_entities(named_entities)
        except TypeError:
            self.set_named_entities(self.xml_name2codepoint)
        #

    def set_named_entities(self, named_entities):
        """Override the internal named entities mapping with
        the provided dict after checking its contents for validity.
        Raises a TypeError if anything other than a mapping was
        provided.
        Raises a ValueError if any invalid replacement is
        defined in the provided mapping.
        """
        try:
            names_and_replacements = named_entities.items()
        except AttributeError:
            raise TypeError('Please provide a mapping.')
        #
        checked_replacements = {}
        for (name, replacement) in names_and_replacements:
            if isinstance(replacement, str):
                checked_replacements[name] = replacement
            elif isinstance(replacement, int):
                # Might raise a ValueError on invalid values
                # outside the range 0–1114111 (0x0–0x10ffff)
                checked_replacements[name] = chr(replacement)
            else:
                raise ValueError(
                    'Only integers up to 0x10ffff or strings'
                    ' are allowed as replacements.')
            #
        #
        self.__named_entities = checked_replacements

    @staticmethod
    def resolve_charref(charref):
        """Resolve a numeric (hexadecimal or decimal) character reference"""
        if charref.startswith('x'):
            codepoint = int('0' + charref, 16)
        else:
            codepoint = int(charref)
        return chr(codepoint)

    def resolve_named_entity(self, name):
        """Resolve a named entity from the internal mapping"""
        try:
            return self.__named_entities[name]
        except KeyError:
            raise ValueError('Name {0!r} not defined.'.format(name))
        #

    def resolve_any_entity(self, entityref):
        """Dispatch to the appropriate resolver method"""
        if entityref.startswith('#'):
            return self.resolve_charref(entityref[1:])
        #
        return self.resolve_named_entity(entityref)

    def __resolve_match(self, match_object):
        """Return the resolved matched entity's replacement,
        or the entity itself if it could not be resolved
        """
        try:
            return self.resolve_any_entity(match_object[1])
        except ValueError:
            return match_object[0]
        #

    def resolve_all_entities(self, source_text):
        """Resolve all entities in source_text using
        this object's __resolve_match() method as replacement
        """
        return self.__prx_entity.sub(self.__resolve_match,
                                     source_text)


# pylint: disable=abstract-method ; The error method is not used


class HtmlTagStripper(html.parser.HTMLParser):

    """Return only the data, concatenated using constants.EMPTY,
    with whitespace squeezed together, but preserving line breaks.
    """

    image_placeholder_with_alt_text = '[image: {0[alt]}]'
    image_placeholder_empty = '[image]'

    re_multiple_space = r'[ \t\r\f\v]{2,}'
    re_newline_and_whitespace = r'\s*\n\s*'

    treated_as_block = {
        'address',
        'article',
        'aside',
        'bdi',
        'blockquote',
        'body',
        'br',
        'canvas',
        'caption',
        'datalist',
        'details',
        'dialog',
        'dir',
        'div',
        'dl',
        'dt',
        'fieldset',
        'figure',
        'figcaption',
        'footer',
        'form',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'head',
        'header',
        'hr',
        'html',
        'iframe',
        'legend',
        'li',
        'main',
        'menu',
        'nav',
        'noscript',
        'ol',
        'option',
        'output',
        'p',
        'picture',
        'pre',
        'ruby',
        'rt',
        'rb',
        'script',
        'section',
        'select',
        'slot',
        'style',
        'summary',
        'table',
        'tbody',
        'template',
        'tfoot',
        'thead',
        'title',
        'tr',
        'ul',
    }

    def __init__(self, image_placeholders=IMAGES_WITH_ALT_TEXT_ONLY):
        """Instantiate the base class and define instance variables"""
        html.parser.HTMLParser.__init__(self, convert_charrefs=True)
        if image_placeholders:
            if image_placeholders == IMAGES_WITH_ALT_TEXT_ONLY:
                self.image_placeholder_empty = ''
            #
        else:
            self.image_placeholder_with_alt_text = ''
        #
        self.__content_list = []
        self.__images = []
        self.__in_body = False
        self.__prx_multiple_space = re.compile(self.re_multiple_space)
        self.__prx_newline_and_whitespace = re.compile(
            self.re_newline_and_whitespace, re.DOTALL)

    def __add_body_content(self, content):
        """Add content if self.__in_body"""
        if self.__in_body:
            self.__content_list.append(content)
        #

    def __add_whitespace(self, lowercased_tag):
        """Add whitespace
        (newline if the tag is treated as a block element,
         else a blank)
        """
        if lowercased_tag in self.treated_as_block:
            self.__add_body_content(constants.NEWLINE)
        else:
            self.__add_body_content(constants.BLANK)
        #

    @property
    def content(self):
        """Return the result"""
        collected_content = self.__prx_multiple_space.sub(
            constants.BLANK,
            constants.EMPTY.join(self.__content_list))
        return self.__prx_newline_and_whitespace.sub(
            constants.NEWLINE,
            collected_content).strip()

    @property
    def images(self):
        """Return the saved image data"""
        return list(self.__images)

    def handle_data(self, data):
        """Collect content"""
        self.__add_body_content(data)

    def handle_starttag(self, tag, attrs):
        """Handle a start tag"""
        tag = tag.lower()
        self.__add_whitespace(tag)
        if tag == 'body':
            self.__in_body = True
        elif tag == 'img':
            # save images' attributes
            current_image = dict(attrs)
            self.__images.append(current_image)
            try:
                self.__add_body_content(
                    self.image_placeholder_with_alt_text.format(
                        current_image))
            except KeyError:
                self.__add_body_content(self.image_placeholder_empty)
            #
        #

    def handle_endtag(self, tag):
        """Handle an end tag"""
        tag = tag.lower()
        self.__add_whitespace(tag)
        if tag == 'body':
            self.__in_body = False
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
