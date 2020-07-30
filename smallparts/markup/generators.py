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
# Constants
#

HTML_5 = 'HTML 5'
XHTML_1_0_STRICT = 'XHTML 1.0 Strict'
XHTML_1_0_TRANSITIONAL = 'XHTML 1.0 Transitional'


#
# Class definitions
#


# pylint: disable= too-few-public-methods ; Not required for the caches


class XmlGenerator():

    """Generate XML code: cache element factories"""

    # visible_attributes = ('_cached_elements_',)
    _cached_elements_ = {}
    element_type = elements.XmlElement

    def __init__(self):
        """Initialize the cache"""
        ...

    def __getattribute__(self, name):
        """Return an existing cache member
        or create a new member
        """
        if name == '__class__':
            return object.__getattribute__(self, name)
        #
        name = type(self).element_type.translate_name(name)
        try:
            return type(self)._cached_elements_[name]
        except KeyError:
            return type(self)._cached_elements_.setdefault(
                name,
                type(self).element_type(name))


class XhtmlStrictGenerator(XmlGenerator):

    """Generate XHTML 1.0 Strict code"""

    _cached_elements_ = {}
    element_type = elements.XhtmlStrictElement


class XhtmlTransitionalGenerator(XmlGenerator):

    """Generate XHTML 1.0 Transitional code"""

    _cached_elements_ = {}
    element_type = elements.XhtmlTransitionalElement


class HtmlGenerator(XmlGenerator):

    """Generate HTML (5) code"""

    _cached_elements_ = {}
    element_type = elements.HtmlElement


#
# Supported HTML dialect definitions
#


SUPPORTED_HTML_DIALECTS = {
    HTML_5: Namespace(
        doctype='<!DOCTYPE html>',
        factory=HtmlGenerator,
        xmlns=None),
    XHTML_1_0_STRICT: Namespace(
        doctype='<!DOCTYPE html PUBLIC'
        ' "-//W3C//DTD XHTML 1.0 Strict//EN"'
        ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
        factory=XhtmlStrictGenerator,
        xmlns='http://www.w3.org/1999/xhtml'),
    XHTML_1_0_TRANSITIONAL: Namespace(
        doctype='<!DOCTYPE html PUBLIC'
        ' "-//W3C//DTD XHTML 1.0 Transitional//EN"'
        ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
        factory=XhtmlTransitionalGenerator,
        xmlns='http://www.w3.org/1999/xhtml'),
}


#
# Functions
#


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


def html_document(dialect=HTML_5,
                  lang='en',
                  title='Untitled page',
                  head='',
                  body=''):
    """Generate an HTML document"""
    try:
        html_dialect = SUPPORTED_HTML_DIALECTS[dialect]
    except KeyError:
        raise ValueError(
            'Unsupported HTML dialect.'
            ' Please specify one of {0}!'.format(
                constants.COMMA_BLANK.join(
                    repr(single_dialect) for single_dialect in
                    SUPPORTED_HTML_DIALECTS)))
    #
    element = html_dialect.factory()
    head_fragments = ['']
    if dialect == HTML_5 and '<meta charset' not in head.lower():
        head_fragments.append(element.meta(charset=constants.UTF_8))
    #
    if '<title' not in head.lower():
        head_fragments.append(element.title(title))
    #
    head = head.strip()
    if head:
        head_fragments.append(head)
    #
    head_fragments.append('')
    body = body.strip()
    if body:
        body = '\n{0}\n'.format(body)
    return join.by_newlines(
        html_dialect.doctype,
        element.html(
            join.by_newlines(
                '',
                element.head(constants.NEWLINE.join(head_fragments)),
                element.body(body),
                ''),
            xmlns=html_dialect.xmlns,
            lang=lang))


def js_function_call(function_name, arguments):
    """Generate JavaScript code:
    function_name(*arguments)
    """
    return '{0}({1})'.format(
        function_name,
        constants.COMMA_BLANK.join(
            "{0!r}".format(single_arg)
            for single_arg in arguments))


def js_return(function_name, *arguments):
    """Generate JavaScript code:
    return function_name(*arguments);
    """
    return 'return {0};'.format(
        js_function_call(function_name, arguments))


def wrap_cdata(character_data):
    """Wrap character_data in a CDATA section.
    If necessary use multiple CDATA sections as suggested in
    <https://en.wikipedia.org/wiki/CDATA#Nesting>
    """
    return join.directly(
        '<![CDATA[',
        character_data.replace(']]>', ']]]]><![CDATA[>'),
        ']]>')


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
        elements.XmlElement.attributes_string(
            dict(version=version,
                 encoding=encoding,
                 standalone=standalone).items()))


def xml_document(content,
                 version=constants.XML_1_0,
                 encoding=constants.UTF_8,
                 standalone=None):
    """Return a full XML document.
    Strip trailing whitespace from the content.
    """
    return join.by_newlines(
        xml_declaration(version=version,
                        encoding=encoding,
                        standalone=standalone),
        content.rstrip())


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
