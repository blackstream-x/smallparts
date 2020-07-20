# -*- coding: utf-8 -*-

"""

smallparts.markup.parsers

Markup parsing

"""


import html.parser
import re

from smallparts import constants

from smallparts.markup import elements
from smallparts.markup import entities


#
# Constants
#


PRX_NEWLINE_AND_WHITESPACE = re.compile(r'\s*\n\s*', re.DOTALL)
PRX_MULTI_SPACE = re.compile(r'[ \t\r\f\v]{2,}')


#
# Classes
#


class HTMLTagStripper(html.parser.HTMLParser):

    """Return only the data, concatenated using constants.EMPTY,
    with whitespace squeezed together, but retaining line breaks.
    """

    def __init__(self):
        """Instantiate the base class and define instance variables"""
        html.parser.HTMLParser.__init__(self)
        self.__content_list = []
        self.__image_descriptions = []
        self.__in_body = False

    def __add_body_content(self, content):
        """Add content if self.__in_body"""
        if self.__in_body:
            self.__content_list.append(content)
        #

    @property
    def content(self):
        """Return the result"""
        _content = PRX_MULTI_SPACE.sub(
            constants.BLANK,
            constants.EMPTY.join(self.__content_list))
        return PRX_NEWLINE_AND_WHITESPACE.sub(constants.NEWLINE,
                                              _content).strip()

    @property
    def image_descriptions(self):
        """Return the saved image descriptions"""
        return list(self.__image_descriptions)

    def error(self, message):
        """override _markupbase.ParserBase abstract method"""
        raise ValueError(message)

    def handle_data(self, data):
        """Collect content"""
        self.__add_body_content(data)

    def handle_charref(self, name):
        """Resolve numeric character reference"""
        self.__add_body_content(entities.resolve_charref(name))

    def handle_entityref(self, name):
        """Resolve a named entity reference, use the entity reference
        itself as fallback in case the name could not be resolved.
        """
        try:
            self.__add_body_content(entities.resolve_entityref(name))
        except KeyError:
            self.__add_body_content(entities.entity(name))
        #

    def handle_starttag(self, tag, attrs):
        """Handle a start tag"""
        if tag in elements.HTML_INLINE_ELEMENTS:
            self.__add_body_content(constants.BLANK)
        else:
            self.__add_body_content(constants.NEWLINE)
        if tag == elements.BODY:
            self.__in_body = True
        elif tag == elements.IMG:
            # save images' alt texts
            attrs_map = dict(attrs)
            try:
                self.__image_descriptions.append(attrs_map['alt'])
            except KeyError:
                pass
            #
        #

    def handle_endtag(self, tag):
        """Handle an end tag"""
        if tag == elements.BODY:
            self.__in_body = False
        if tag in elements.HTML_INLINE_ELEMENTS:
            self.__add_body_content(constants.BLANK)
        else:
            self.__add_body_content(constants.NEWLINE)
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
