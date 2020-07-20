# -*- coding: utf-8 -*-

"""

smallparts.markup

Markup (HTML, XML) generation and parsing

"""


#import html.entities
#import re
#import unicodedata
#import xml.sax.saxutils

from smallparts import constants

from smallparts.markup import elements
from smallparts.namespaces import Namespace, InstantNames
from smallparts.text import join
from smallparts.text import translate


#
# Constants
#

CDATA_START = '<![CDATA['
CDATA_END = ']]>'

# A CDATA section end string splitted up
# into two parts in separate CDATA sections
CDATA_END_SPLITTED_UP = ']]{0}{1}>'.format(CDATA_END, CDATA_START)

FS_COMMENT = '<!-- {0} -->'
FS_CSS_PROPERTY = '{0}: {1};'
FS_CSS_IMPORTANT = '{0} !important'

FS_FUNCTION_CALL = '{0}({1})'
FS_SINGLE_QUOTED = "'{0}'"
FS_STARTTAG = '<{tag_name}{tag_attributes}>'

JS_RETURN = 'return'

XML = 'xml'
XML_VERSION = '1.0'

#
# Names caches
#

TAG = InstantNames(translate.remove_trailing_underscores,
                   translate.underscores_to_dashes)


def wrap_cdata(character_data):
    """Wrap character_data in a CDATA section,
    if necessary use multiple CDATA sections as suggested in
    <https://en.wikipedia.org/wiki/CDATA#Nesting>
    """
    return join.directly(
        CDATA_START,
        character_data.replace(CDATA_END, CDATA_END_SPLITTED_UP),
        CDATA_END)



def css_property(property_name, property_value):
    """Generate a CSS property:
    property_name: property_value;
    """
    return FS_CSS_PROPERTY.format(property_name, property_value)


def css_important_property(property_name, property_value):
    """Generate an 'important' CSS property:
    property_name: property_value !important;
    """
    return css_property(property_name,
                        FS_CSS_IMPORTANT.format(property_value))


def js_function_call(function_name, arguments):
    """Generate JavaScript code:
    function_name(*arguments)
    """
    return FS_FUNCTION_CALL.format(
        function_name,
        constants.COMMA_BLANK.join(
            FS_SINGLE_QUOTED.format(single_arg)
            for single_arg in arguments))


def js_return(function_name, *arguments):
    """Generate JavaScript code:
    return function_name(*arguments);
    """
    return join.directly(
        JS_RETURN,
        constants.BLANK,
        js_function_call(function_name, arguments),
        constants.SEMICOLON)


#
# Class definitions
#


# pylint: disable=too-few-public-methods; not suitable for the element classes


# pylint: enable=too-few-public-methods


class XmlGenerator(Namespace):

    """Generate XML code: cache generated elements"""

    element_factory = elements.XmlElement

    def __init__(self):
        """Initialize the Namespace"""
        # pylint: disable=useless-super-delegation ; do not accept arguments
        super(XmlGenerator, self).__init__()

    def __getattribute__(self, name):
        """Access a visible attribute,
        return an existing dict member
        or create a new member
        """
        if name in type(self).visible_attributes:
            return object.__getattribute__(self, name)
        #
        try:
            return self[name]
        except KeyError:
            new_function = type(self).element_factory(name)
            setattr(self, name, new_function)
            return new_function
        #


class HtmlGenerator(XmlGenerator):

    """Generate HTML code """

    element_factory = elements.HtmlElement

    def __init__(self):
        """Define non-standard elements"""
        super(HtmlGenerator, self).__init__()
        cls = type(self)
        self.br_ = cls.element_factory(TAG.br, compact_empty=True)
        self.hr_ = cls.element_factory(TAG.hr, compact_empty=True)
        self.img = cls.element_factory(TAG.img, compact_empty=True)
        self.link = cls.element_factory(TAG.link, compact_empty=True)
        self.meta = cls.element_factory(TAG.meta, compact_empty=True)
        self.input_ = self.input = \
            cls.element_factory(TAG.input, compact_empty=True)
        #


class Html5Generator(HtmlGenerator):

    """Generate HTML5 code """

    element_factory = elements.Html5Element


#
# End of class definitions, start of function definitions
#


def xml_declaration(version=XML_VERSION,
                    encoding=constants.UTF_8,
                    standalone=None):
    """Return an XML declaration.
    Omit the 'standalone' attribute if not specified.
    """
    if standalone is not None:
        if standalone:
            standalone = constants.YES
        else:
            standalone = constants.NO
        #
    #
    return FS_STARTTAG.format(
        tag_name=XML,
        tag_attributes=elements.make_attributes_string(
            version=version,
            encoding=encoding,
            standalone=standalone))


def xml_document(content,
                 version=XML_VERSION,
                 encoding=constants.UTF_8,
                 standalone=None):
    """Return a full XML document.
    Strip trailing whitespace from the content
    and end the document with a newline.
    """
    return join.by_newlines(
        xml_declaration(version=version,
                        encoding=encoding,
                        standalone=standalone),
        content.rstrip(),
        constants.EMPTY)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
