# -*- coding: utf-8 -*-

"""

smallparts.markup.elements

Markup (HTML, XML) generation:
Simple XML, XHTML 1.0 and HTML 5 element definitions

"""


import xml.sax.saxutils

from smallparts import constants

from smallparts.text import translate


#
# Constants
#

LABEL_HTML_5 = 'HTML 5'
LABEL_XHTML_1_0_STRICT = 'XHTML 1.0 Strict'
LABEL_XHTML_1_0_TRANSITIONAL = 'XHTML 1.0 Transitional'
LABEL_XML = 'XML'

# From the XHTML Strict DTD
# <https://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd>
XHTML_1_0_STRICT = {
    'a',
    'abbr',
    'acronym',
    'address',
    'area',
    'b',
    'base',
    'bdo',
    'big',
    'blockquote',
    'body',
    'br',
    'button',
    'caption',
    'cite',
    'code',
    'col',
    'colgroup',
    'dd',
    'del',
    'dfn',
    'div',
    'dl',
    'dt',
    'em',
    'fieldset',
    'form',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'head',
    'hr',
    'html',
    'i',
    'img',
    'input',
    'ins',
    'kbd',
    'label',
    'legend',
    'li',
    'link',
    'map',
    'meta',
    'noscript',
    'object',
    'ol',
    'optgroup',
    'option',
    'p',
    'param',
    'pre',
    'q',
    'samp',
    'script',
    'select',
    'small',
    'span',
    'strong',
    'style',
    'sub',
    'sup',
    'table',
    'tbody',
    'td',
    'textarea',
    'tfoot',
    'th',
    'thead',
    'title',
    'tr',
    'tt',
    'ul',
    'var',
}

# From the XHTML 1.0 Transitional DTD
# <http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd>
# (difference to transitional only)
XHTML_1_0_TRANSITIONAL = XHTML_1_0_STRICT | {
    'applet',
    'basefont',
    'center',
    'dir',
    'font',
    'iframe',
    'isindex',
    'menu',
    'noframes',
    's',
    'strike',
    'u',
}

# HTML 5 Elements (difference from XHTML 1.0 Transitional), see
# <https://www.w3.org/TR/html5-diff/#language> and
# <https://html.spec.whatwg.org/>
HTML_5 = XHTML_1_0_TRANSITIONAL - {
    'acronym',
    'applet',
    'basefont',
    'big',
    'center',
    'dir',
    'font',
    'isindex',
    'strike',
    'tt',
} | {
    'article',
    'aside',
    'audio',
    'bdi',
    'canvas',
    'datalist',
    'details',
    'dialog',
    'embed',
    'figcaption',
    'figure',
    'footer',
    'header',
    'keygen',
    'main',
    'mark',
    'meter',
    'nav',
    'output',
    'picture',
    'progress',
    'rp',
    'rt',
    'ruby',
    'section',
    'slot',
    'source',
    'summary',
    'template',
    'time',
    'track',
    'video',
    'wbr',
}

XHTML_1_0_EMPTY_ELEMENTS = {
    'area',
    'base',
    'basefont',
    'br',
    'col',
    'hr',
    'iframe',
    'img',
    'input',
    'isindex',
    'link',
    'meta',
    'param',
}

HTML_5_EMPTY_ELEMENTS = XHTML_1_0_EMPTY_ELEMENTS - {
    'basefont',
    'iframe',
    'isindex',
} | {
    'embed',
    'keygen',
    'source',
    'track',
    'wbr',
}


#
# Class definitions
#


class XmlElement():

    """Callable XML element"""

    fs_empty_element = \
        '<{start_tag}{attributes}/>'
    fs_generic_element = \
        '<{start_tag}{attributes}>{content}</{end_tag}>'
    # Empty set: do not restrict element names
    restrict_elements_to = set()
    name_translations = (
        translate.remove_trailing_underscores,
        translate.underscores_to_dashes,
    )

    def __init__(self, tag_name):
        """Set tag name"""
        tag_name = self.translate_name(tag_name)
        #
        if self.restrict_elements_to and \
                tag_name not in self.restrict_elements_to:
            raise ValueError('Unsupported element name {0!r}'.format(
                tag_name))
        #
        self.tag_name = tag_name

    @classmethod
    def translate_name(cls, name):
        """Apply all functions in the name_translations sequence to name
        and return the result
        """
        for translation_function in cls.name_translations:
            name = translation_function(name)
        #
        return name

    @classmethod
    def single_attribute(cls, attribute_name, attribute_value):
        """Make an XML attribute from the given attr_name, attr_value pair"""
        if attribute_value is None or attribute_value is False:
            return constants.EMPTY
        #
        attribute_name = cls.translate_name(attribute_name)
        #
        if attribute_value is True:
            attribute_value = attribute_name
        #
        return ' {0}={1}'.format(
            attribute_name,
            xml.sax.saxutils.quoteattr(str(attribute_value)))

    @classmethod
    def attributes_string(cls, attributes):
        """Make a single string from the 'attributes' (name, value) list.
        Attributes with None values are ignored.
        """
        tag_attributes = [
            cls.single_attribute(attribute_name, attribute_value)
            for (attribute_name, attribute_value) in attributes
            if attribute_value is not None]
        return constants.EMPTY.join(tag_attributes)

    def _output(self,
                content_fragments,
                attributes,
                compact_empty=True,
                start_tag_override=None):
        """Return the element as a string containing an XML subtree"""
        start_tag = start_tag_override or self.tag_name
        content = constants.EMPTY.join(content_fragments)
        if compact_empty and not content:
            fs_element = self.fs_empty_element
        else:
            fs_element = self.fs_generic_element
        #
        return fs_element.format(
            start_tag=start_tag,
            attributes=self.attributes_string(attributes.items()),
            content=content,
            end_tag=self.tag_name)

    def __call__(self, *content_fragments, **attributes):
        """Return an element generated from the given parameters"""
        return self._output(content_fragments,
                            attributes,
                            compact_empty=True)


class XmlBasedHtmlElement(XmlElement):

    """Callable HTML element (base class)"""

    fs_empty_element = \
        '<{start_tag}{attributes} />'
    # Always lowercase tag names
    name_translations = (
        translate.remove_trailing_underscores,
        translate.underscores_to_dashes,
        str.lower,
    )

    # Definitions for HTML elements only
    empty_elements = XHTML_1_0_EMPTY_ELEMENTS
    attribute_duplications = {}

    def __init__(self,
                 tag_name):
        """Set tag name"""
        super(XmlBasedHtmlElement, self).__init__(tag_name)
        self.is_empty = self.tag_name in self.empty_elements

    def __call__(self, *content_fragments, **attributes):
        """Return a new tag from the given parameters

        Special attributes:
        __class__   -> HTML attribute 'class' because 'class'
                       is a keyword in Python
        __classes__ -> Sequence of classes for the element
        """
        #
        # If a classes sequence was given using the parameter __classes__,
        # construct a new class attribute
        # with all given class names separated by blanks
        classes_set = set()
        try:
            classes_set.add(attributes.pop('__class__'))
        except KeyError:
            ...
        #
        try:
            classes_set.update(set(attributes.pop('__classes__')))
        except KeyError:
            ...
        #
        if classes_set:
            attributes['class'] = constants.BLANK.join(sorted(classes_set))
        #
        # Duplicate certain elements as others
        # (xml:lang= with the same value as lang= in XHTML)
        for (source, target) in self.attribute_duplications.items():
            try:
                attributes[target] = attributes[source]
            except KeyError:
                ...
            #
        #
        if self.is_empty:
            return self._output(tuple(),
                                attributes,
                                compact_empty=True)
        #
        return self._output(content_fragments,
                            attributes,
                            compact_empty=False)


class HtmlElement(XmlBasedHtmlElement):

    """Callable HTML (5) element"""

    fs_empty_element = ('<{start_tag}{attributes}>')
    restrict_elements_to = HTML_5
    empty_elements = HTML_5_EMPTY_ELEMENTS

    @classmethod
    def single_attribute(cls, attribute_name, attribute_value):
        """Make an XML attribute from the given attr_name, attr_value pair"""
        if attribute_value is True:
            return ' {0}'.format(cls.translate_name(attribute_name))
        #
        return XmlElement.single_attribute(
            attribute_name,
            attribute_value)


class XhtmlStrictElement(XmlBasedHtmlElement):

    """Callable XHTML 1.0 Strict element"""

    restrict_elements_to = XHTML_1_0_STRICT
    attribute_duplications = {'lang': 'xml:lang'}


class XhtmlTransitionalElement(XhtmlStrictElement):

    """Callable XHTML 1.0 Transitional element"""

    restrict_elements_to = XHTML_1_0_TRANSITIONAL


class Cache():

    """Cache for element factories"""

    accessible_attributes = ('_dialect',)
    cached_elements = {
        LABEL_HTML_5: {},
        LABEL_XHTML_1_0_STRICT: {},
        LABEL_XHTML_1_0_TRANSITIONAL: {},
        LABEL_XML: {}}
    factories = {
        LABEL_HTML_5: HtmlElement,
        LABEL_XHTML_1_0_STRICT: XhtmlStrictElement,
        LABEL_XHTML_1_0_TRANSITIONAL: XhtmlTransitionalElement,
        LABEL_XML: XmlElement}

    def __init__(self, dialect):
        """Initialize the cache"""
        if dialect not in type(self).cached_elements:
            raise ValueError('Unsupported dialect.')
        #
        self._dialect = dialect

    def __dir__(self):
        """Sorted list of generated elements"""
        return sorted(type(self).cached_elements[self._dialect])

    def __repr__(self):
        """Textual representation"""
        return '{0}(dialect={1!r})'.format(
            type(self).__name__, self._dialect)

    def __getattribute__(self, name):
        """Return an existing cache member
        or create a new member
        """
        if name in type(self).accessible_attributes:
            return object.__getattribute__(self, name)
        #
        dialect_cache = type(self).cached_elements[self._dialect]
        factory = type(self).factories[self._dialect]
        name = factory.translate_name(name)
        try:
            return dialect_cache[name]
        except KeyError:
            return dialect_cache.setdefault(name, factory(name))


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
