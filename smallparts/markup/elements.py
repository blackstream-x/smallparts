# -*- coding: utf-8 -*-

"""

smallparts.markup.elements

Markup (HTML, XML) generation and parsing - Element definitions

"""


import xml.sax.saxutils

from smallparts import constants

from smallparts.namespaces import InstantNames

from smallparts.text import join
from smallparts.text import translate


#
# Constants
#


TAG = InstantNames(translate.remove_trailing_underscores,
                   translate.underscores_to_dashes)

BODY = TAG.body
IMG = TAG.img

HTML_INLINE_ELEMENTS = (
    TAG.a__, TAG.abbr, TAG.b__, TAG.bdi, TAG.bdo, TAG.cite,
    TAG.code_, TAG.del_, TAG.dfn, TAG.em_, TAG.i__, TAG.img,
    TAG.ins, TAG.kbd, TAG.mark, TAG.q__, TAG.rp_, TAG.rt_,
    TAG.ruby, TAG.s__, TAG.samp, TAG.small, TAG.strong,
    TAG.span, TAG.sub, TAG.sup, TAG.time_, TAG.u__, TAG.var,
    TAG.wbr)


def xml_attribute(attr_name, attr_value):
    """Make an XML attribute from the given attr_name, attr_value pair"""
    return join.using(
        constants.EQUALS,
        translate.underscores_to_dashes(
            translate.remove_trailing_underscores(attr_name)),
        xml.sax.saxutils.quoteattr(str(attr_value)))


def make_attributes_string(attributes=None, **kwargs):
    """Make a single string from the 'attributes' dict items"""
    if attributes is None:
        attributes = {}
    attributes.update(kwargs)
    tag_attributes_list = [xml_attribute(attr_name, attr_value)
                           for (attr_name, attr_value) in attributes.items()
                           if attr_value is not None]
    if tag_attributes_list:
        return join.directly(
            constants.BLANK,
            constants.BLANK.join(tag_attributes_list))
    #
    return constants.EMPTY


def make_html5_attributes_string(attributes=None, **kwargs):
    """Make a single string from the 'attributes' dict items.
    Attributes with False or None values are ignored,
    attributes with True values or with the name as value
    are rendered as empty attributes. All other attributes
    are rendered normally, including those with an empty string."""
    if attributes is None:
        attributes = {}
    attributes.update(kwargs)
    tag_attributes_list = []
    for (attr_name, attr_value) in attributes.items():
        if attr_value is None or attr_value is False:
            continue
        #
        if attr_value is True or attr_value == attr_name:
            tag_attributes_list.append(attr_name)
        else:
            tag_attributes_list.append(xml_attribute(attr_name, attr_value))
        #
    #
    if tag_attributes_list:
        return join.directly(
            constants.BLANK,
            constants.BLANK.join(tag_attributes_list))
    #
    return constants.EMPTY


#
# Class definitions
#


# pylint: disable=too-few-public-methods; not suitable for the element classes


class XmlElement():

    """Callable XML element"""

    fs_generic_element = ('<{start_tag}{start_tag_additions}'
                          '{tag_attributes}>{tag_content}</{end_tag}>')
    fs_empty_element = ('<{start_tag}{start_tag_additions}'
                        '{tag_attributes} />')
    attributes_string = staticmethod(make_attributes_string)

    def __init__(self, tag_name):
        """Set tag name"""
        self.tag_name = translate.underscores_to_dashes(
            translate.remove_trailing_underscores(tag_name))
        #

    def output(self,
               content_fragments,
               attributes,
               compact_empty=True,
               start_tag_override=None):
        """Return the element as a string containing an XML subtree

        Special attributes:
        in_starttag_      -> additional text in the start tag,
                             e.g. placefolders for later replacements
        """
        start_tag_additions = attributes.pop('in_starttag_',
                                             constants.EMPTY)
        start_tag = start_tag_override or self.tag_name
        content = constants.EMPTY.join(content_fragments)
        if compact_empty and not content:
            fs_element = self.fs_empty_element
        else:
            fs_element = self.fs_generic_element
        #
        return fs_element.format(
            start_tag=start_tag,
            start_tag_additions=start_tag_additions,
            tag_attributes=self.attributes_string(attributes),
            tag_content=content,
            end_tag=self.tag_name)

    def __call__(self, *content_fragments, **attributes):
        """Return an element generated from the given parameters

        Special attributes:
        in_starttag_      -> additional text in the start tag,
                             e.g. placefolders for later replacements
        """
        return self.output(content_fragments, attributes, compact_empty=True)


class HtmlElement(XmlElement):

    """Callable HTML element"""

    def __init__(self,
                 tag_name,
                 placeholder=None,
                 placeholder_enabled_default=False,
                 compact_empty=False):
        """Set tag name"""
        super(HtmlElement, self).__init__(tag_name)
        self.placeholder = placeholder
        self.placeholder_enabled_default = placeholder_enabled_default
        self.compact_empty = compact_empty

    def __call__(self, *content_fragments, **attributes):
        """Return a new tag from the given parameters

        Special attributes:
        start_tag_additions_ -> additional text in the start tag,
                                e.g. placeholders for later replacements
        placeholder_enabled_ -> explicitly allow (when True)
                                or disallow (when False)
                                outputting a placeholder instead of the
                                start tag.
        """
        placeholder_enabled = attributes.pop(
            'placeholder_enabled_', self.placeholder_enabled_default)
        #
        # If a classes list was given using the parameter CLASSES,
        # construct a new class_ attribute
        # with all given class names separated by blanks
        try:
            classes_set = set(attributes.pop('CLASSES'))
        except KeyError:
            pass
        else:
            explicit_class = attributes.pop('class_', None)
            if explicit_class:
                classes_set.add(explicit_class)
            #
            if classes_set:
                attributes['class_'] = constants.BLANK.join(classes_set)
            #
        #
        if placeholder_enabled:
            start_tag_override = self.placeholder
        else:
            start_tag_override = None
        #
        return self.output(content_fragments,
                           attributes,
                           compact_empty=self.compact_empty,
                           start_tag_override=start_tag_override)


class Html5Element(HtmlElement):

    """Callable HTML5 element"""

    fs_empty_element = ('<{start_tag}{start_tag_additions}'
                        '{tag_attributes}>')
    attributes_string = staticmethod(make_html5_attributes_string)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
