# -*- coding: utf-8 -*-

"""

smallparts.markup.elements

Markup (HTML, XML) generation – Element definitions

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

# TODO: HTML 4 elements
# <https://www.w3.org/QA/2002/04/valid-dtd-list.html>
# <https://www.w3.org/TR/html401/loose.dtd>
# for an exhaustive list of HTML 4 elements

# Generated from the XHTML Strict DTD
# <https://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd>
# using these commands:
# =============================================================================
# >>> with open('xhtml1-strict.dtd', mode='rt', encoding='utf-8') as dtd_file:
# ...     dtd_lines = sorted(line for line in dtd_file)
# ...
# >>> for line in dtd_lines:
# ...     if '!ELEMENT' in line:
# ...         print('    TAG.{0[1]:_<3},'.format(line.split()))
# ...
# =============================================================================
XHTML_1_0_ELEMENTS = {
    TAG.a__,
    TAG.abbr,
    TAG.acronym,
    TAG.address,
    TAG.area,
    TAG.b__,
    TAG.base,
    TAG.bdo,
    TAG.big,
    TAG.blockquote,
    TAG.body,
    TAG.br_,
    TAG.button,
    TAG.caption,
    TAG.cite,
    TAG.code,
    TAG.col,
    TAG.colgroup,
    TAG.dd_,
    TAG.del_,
    TAG.dfn,
    TAG.div,
    TAG.dl_,
    TAG.dt_,
    TAG.em_,
    TAG.fieldset,
    TAG.form,
    TAG.h1_,
    TAG.h2_,
    TAG.h3_,
    TAG.h4_,
    TAG.h5_,
    TAG.h6_,
    TAG.head,
    TAG.hr_,
    TAG.html,
    TAG.i__,
    TAG.img,
    TAG.input,
    TAG.ins,
    TAG.kbd,
    TAG.label,
    TAG.legend,
    TAG.li_,
    TAG.link,
    TAG.map,
    TAG.meta,
    TAG.noscript,
    TAG.object,
    TAG.ol_,
    TAG.optgroup,
    TAG.option,
    TAG.p__,
    TAG.param,
    TAG.pre,
    TAG.q__,
    TAG.samp,
    TAG.script,
    TAG.select,
    TAG.small,
    TAG.span,
    TAG.strong,
    TAG.style,
    TAG.sub,
    TAG.sup,
    TAG.table,
    TAG.tbody,
    TAG.td_,
    TAG.textarea,
    TAG.tfoot,
    TAG.th_,
    TAG.thead,
    TAG.title,
    TAG.tr_,
    TAG.tt_,
    TAG.ul_,
    TAG.var,
}

# Sorted out of the above list manually using the
# W3C XHTML 1.0 Strict Cheat Sheet
# <https://www.w3.org/2010/04/xhtml10-strict.html>
XHTML_1_0_INLINE_ELEMENTS = {
    TAG.a__,
    TAG.abbr,
    TAG.acronym,
    TAG.b__,
    TAG.big,
    TAG.br_,
    TAG.button,
    TAG.cite,
    TAG.code,
    TAG.dfn,
    TAG.em_,
    TAG.i__,
    TAG.img,
    TAG.input,
    TAG.kbd,
    TAG.label,
    TAG.object,
    TAG.q__,
    TAG.samp,
    TAG.select,
    TAG.small,
    TAG.span,
    TAG.strong,
    TAG.sub,
    TAG.sup,
    TAG.textarea,
    TAG.tt_,
    TAG.var,
}

# Generated from the XHTML Strict DTD
# <https://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd>
# using these commands:
# =============================================================================
# >>> with open('xhtml1-strict.dtd', mode='rt', encoding='utf-8') as dtd_file:
# ...     dtd_lines = sorted(line for line in dtd_file)
# ...
# >>> for line in dtd_lines:
# ...     if '!ELEMENT' in line and 'EMPTY' in line:
# ...         print('    TAG.{0[1]:_<3},'.format(line.split()))
# ...
# =============================================================================
XHTML_1_0_EMPTY_ELEMENTS = {
    TAG.area,
    TAG.base,
    TAG.br_,
    TAG.col,
    TAG.hr_,
    TAG.img,
    TAG.input,
    TAG.link,
    TAG.meta,
    TAG.param,
}

# HTML 5 Elements difference from XHTML, see
# <https://www.w3.org/TR/html5-diff/#obsolete-elements> and
# <>
HTML_5_ELEMENTS = XHTML_1_0_ELEMENTS - {
    TAG.acronym,
    TAG.applet,
    TAG.basefont,
    TAG.big,
    TAG.center,
    TAG.dir,
    TAG.font,
    TAG.isindex,
    TAG.strike,
    TAG.tt_,
} | {
    TAG.section,
    TAG.article,
    TAG.main,
    TAG.aside,
    TAG.header,
    TAG.footer,
    TAG.nav,
    TAG.figure,
    TAG.figcaption,
    TAG.template,
    TAG.video,
    TAG.audio,
    TAG.source,
    TAG.track,
    TAG.embed,
    TAG.mark,
    TAG.progress,
    TAG.meter,
    TAG.time,
    TAG.ruby,
    TAG.rt_,
    TAG.rp_,
    TAG.bdi,
    TAG.wbr,
    TAG.canvas,
    TAG.datalist,
    TAG.keygen,
    TAG.output,
}


HTML_INLINE_ELEMENTS = (
    TAG.a__, TAG.abbr, TAG.b__, TAG.bdi, TAG.bdo, TAG.cite,
    TAG.code_, TAG.del_, TAG.dfn, TAG.em_, TAG.i__, TAG.img,
    TAG.ins, TAG.kbd, TAG.mark, TAG.q__, TAG.rp_, TAG.rt_,
    TAG.ruby, TAG.s__, TAG.samp, TAG.small, TAG.strong,
    TAG.span, TAG.sub, TAG.sup, TAG.time_, TAG.u__, TAG.var,
    TAG.wbr)


#
# Functions
#


def xml_attribute(attr_name, attr_value):
    """Make an XML attribute from the given attr_name, attr_value pair"""
    return join.using(
        constants.EQUALS,
        translate.underscores_to_dashes(
            translate.remove_trailing_underscores(attr_name)),
        xml.sax.saxutils.quoteattr(str(attr_value)))


def make_attributes_string(attributes=None, **kwargs):
    """Make a single string from the 'attributes' dict items.
    Attributes with None values are ignored.
    """
    if attributes is None:
        attributes = {}
    attributes.update(kwargs)
    tag_attributes_list = [
        xml_attribute(attr_name, attr_value)
        for (attr_name, attr_value) in attributes.items()
        if attr_value is not None]
    if tag_attributes_list:
        return join.directly(
            constants.BLANK,
            constants.BLANK.join(tag_attributes_list))
    #
    return constants.EMPTY


def make_html_attributes_string(attributes=None, **kwargs):
    """Make a single string from the 'attributes' dict items.
    Attributes with False or None values are ignored,
    attributes with True values are rendered as empty attributes.
    All other attributes are rendered normally,
    including those with an empty string value.
    """
    if attributes is None:
        attributes = {}
    #
    attributes.update(kwargs)
    tag_attributes_list = []
    for (attr_name, attr_value) in attributes.items():
        if attr_value is None or attr_value is False:
            continue
        #
        if attr_value is True:
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


class XhtmlElement(XmlElement):

    """Callable XHTML element"""

    restrict_elements_to = XHTML_1_0_ELEMENTS
    empty_elements = XHTML_1_0_EMPTY_ELEMENTS

    def __init__(self,
                 tag_name,
                 placeholder=None,
                 placeholder_enabled_default=False):
        """Set tag name"""
        if self.restrict_elements_to and tag_name not in self.restrict_elements_to:
            raise ValueError('Unsupported element name {0!r}'.format(
                tag_name))
        #
        super(XhtmlElement, self).__init__(tag_name)
        self.placeholder = placeholder
        self.placeholder_enabled_default = placeholder_enabled_default
        self.compact_empty = tag_name in self.empty_elements

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
        # If a classes sequence was given using the parameter __classes__,
        # construct a new class_ attribute
        # with all given class names separated by blanks
        try:
            classes_set = set(attributes.pop('__classes__'))
        except KeyError:
            pass
        else:
            explicit_class = attributes.pop('class_', None)
            if explicit_class:
                classes_set.add(explicit_class)
            #
            if classes_set:
                attributes['class_'] = constants.BLANK.join(
                    sorted(classes_set))            #
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


class HtmlElement(XhtmlElement):

    """Callable HTML (5) element"""

    restrict_elements_to = HTML_5_ELEMENTS

    fs_empty_element = ('<{start_tag}{start_tag_additions}'
                        '{tag_attributes}>')
    attributes_string = staticmethod(make_html_attributes_string)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
