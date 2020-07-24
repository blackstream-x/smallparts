# -*- coding: utf-8 -*-

"""

smallparts.markup.generators

Markup (HTML, XML) generation

"""


from smallparts import constants

from smallparts.markup import elements
from smallparts.namespaces import Namespace
from smallparts.text import join


#
# Functions
#


def wrap_cdata(character_data):
    """Wrap character_data in a CDATA section,
    if necessary use multiple CDATA sections as suggested in
    <https://en.wikipedia.org/wiki/CDATA#Nesting>
    """
    return join.directly(
        '<![CDATA[',
        character_data.replace(']]>', ']]]]><![CDATA[>'),
        ']]>')


def css_property(property_name, property_value):
    """Generate a CSS property:
    property_name: property_value;
    """
    return '{0}: {1};'.format(property_name, property_value)


def css_important_property(property_name, property_value):
    """Generate an 'important' CSS property:
    property_name: property_value !important;
    """
    return css_property(property_name,
                        '{0} !important'.format(property_value))


def js_function_call(function_name, arguments):
    """Generate JavaScript code:
    function_name(*arguments)
    """
    return '{0}({1})'.format(
        function_name,
        constants.COMMA_BLANK.join(
            "'{0}'".format(single_arg)
            for single_arg in arguments))


def js_return(function_name, *arguments):
    """Generate JavaScript code:
    return function_name(*arguments);
    """
    return 'return {0};'.format(js_function_call(function_name, arguments))


def xml_declaration(version=constants.XML_1_0,
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
    return '<?xml{0} ?>'.format(
        elements.make_attributes_string(
            version=version,
            encoding=encoding,
            standalone=standalone))


def xml_document(content,
                 version=constants.XML_1_0,
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


#
# Class definitions
#


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


class XhtmlGenerator(XmlGenerator):

    """Generate XHTML code"""

    element_factory = elements.XhtmlElement


class HtmlGenerator(XhtmlGenerator):

    """Generate HTML (5) code"""

    element_factory = elements.HtmlElement


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
