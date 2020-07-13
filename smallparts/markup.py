# -*- coding: utf-8 -*-

"""

smallparts.markup - markup (HTML, XML) generation

"""


import html.entities
import html.parser
import re
import unicodedata
import xml.sax.saxutils

from smallparts import constants

from smallparts.namespaces import Namespace, InstantNames
from smallparts.text import join
from smallparts.text import transcode
from smallparts.text import translate


#
# Constants
#

BASE_HEX = 16

CDATA_START = '<![CDATA['
CDATA_END = ']]>'

# A CDATA section end string splitted up
# into two parts in separate CDATA sections
CDATA_END_SPLITTED_UP = ']]{0}{1}>'.format(CDATA_END, CDATA_START)

FS_COMMENT = '<!-- {0} -->'
FS_CSS_PROPERTY = '{0}: {1};'
FS_CSS_IMPORTANT = '{0} !important'
FS_ENTITY = '&{0};'
FS_HEX_PREFIX = '0{0}'
FS_NUMERIC_ENTITY = FS_ENTITY.format('#{0}')
FS_FUNCTION_CALL = '{0}({1})'
FS_SINGLE_QUOTED = "'{0}'"
FS_STARTTAG = '<{tag_name}{tag_attributes}>'

JS_RETURN = 'return'

PREFIX_HEX_CHARREF = 'x'

PRX_HTML_BODY = re.compile(r'(<html(?:\s+.+?)>).+?'
                           r'(<body(?:\s+.+?)>.+)\Z', re.DOTALL)
PRX_NEWLINE_AND_WHITESPACE = re.compile(r'\s*\n\s*', re.DOTALL)
PRX_MULTI_SPACE = re.compile(r'[ \t\r\f\v]{2,}')

XML = 'xml'
XML_VERSION = '1.0'

#
# Names caches
#

KEY = InstantNames()
TAG = InstantNames(translate.remove_trailing_underscores,
                   translate.underscores_to_dashes)

INLINE_ELEMENTS = (TAG.a__, TAG.abbr, TAG.b__, TAG.bdi, TAG.bdo, TAG.cite,
                   TAG.code_, TAG.del_, TAG.dfn, TAG.em_, TAG.i__, TAG.img,
                   TAG.ins, TAG.kbd, TAG.mark, TAG.q__, TAG.rp_, TAG.rt_,
                   TAG.ruby, TAG.s__, TAG.samp, TAG.small, TAG.strong,
                   TAG.span, TAG.sub, TAG.sup, TAG.time_, TAG.u__, TAG.var,
                   TAG.wbr)


def wrap_cdata(character_data):
    """Wrap character_data in a CDATA section,
    if necessary use multiple CDATA sections as suggested in
    <https://en.wikipedia.org/wiki/CDATA#Nesting>
    """
    return join.directly(
        CDATA_START,
        character_data.replace(CDATA_END, CDATA_END_SPLITTED_UP),
        CDATA_END)


def escape(data):
    """Wrap the xml.sax.saxutils.escape function"""
    return xml.sax.saxutils.escape(data)


def unescape(data):
    """Wrap the xml.sax.saxutils.escape function"""
    return xml.sax.saxutils.unescape(data)


def xml_attribute(attr_name, attr_value):
    """Make an XML attribute from the given attr_name, attr_value pair"""
    return join.using(
        constants.EQUALS,
        translate.underscores_to_dashes(
            translate.remove_trailing_underscores(attr_name)),
        xml.sax.saxutils.quoteattr(str(attr_value)))


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


def entity(reference):
    """Return a numeric (&#reference;) or symbolic: (&reference;) entity,
    depending on the reference's type
    """
    try:
        return FS_NUMERIC_ENTITY.format(int(reference))
    except ValueError:
        return FS_ENTITY.format(reference)
    #


def entity_from_name(unicode_character_name):
    """Return the numeric (&#reference;) entity
    for the given unicode character name
    """
    return entity(ord(unicodedata.lookup(unicode_character_name)))


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


def replace_by_entity(input_string, character):
    """Replace all occurrences of character in input_string
    by the mathing numeric entity
    """
    return input_string.replace(character, entity(ord(character)))


def resolve_charref(charref_number):
    """Resolve a numeric character reference (decimal or hex)
    and return the matching unicode character
    """
    if charref_number.lower().startswith(PREFIX_HEX_CHARREF):
        codepoint_ = int(FS_HEX_PREFIX.format(charref_number), BASE_HEX)
    else:
        codepoint_ = int(charref_number)
    return chr(codepoint_)


def resolve_entityref(entity_name):
    """Resolve a named entity reference
    and return the matching unicode character
    """
    return chr(html.entities.name2codepoint[entity_name])


def resolve_matched_entityref(match_object):
    """Return the unicode character from the matched named entity,
    or return the original string if no such entity is defined"""
    entity_name = match_object.group(constants.SECOND_INDEX)
    try:
        return resolve_entityref(entity_name)
    except KeyError:
        return match_object.group(constants.FIRST_INDEX)


def resolve_matched_charref(match_object):
    """Return the unicode character from the matched numeric charref"""
    return resolve_charref(match_object.group(constants.SECOND_INDEX))


#
#
#


INVALID_XML_CODEPOINTS = list(range(0, 9)) + list(range(11, 32)) + [127]
XML_REPLACEMENTS = dict(
    (chr(codepoint), entity(codepoint))
    for codepoint in (34, 39, 60, 62, 91, 93))
XML_REPLACEMENTS.update(dict.fromkeys(
    [chr(codepoint) for codepoint in INVALID_XML_CODEPOINTS],
    constants.EMPTY))


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
        start_tag_additions = attributes.pop(KEY.in_starttag_,
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
            KEY.placeholder_enabled_, self.placeholder_enabled_default)
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


# pylint: enable=too-few-public-methods


class XmlGenerator(Namespace):

    """Generate XML code: cache generated elements"""

    element_factory = XmlElement

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

    element_factory = HtmlElement

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

    element_factory = Html5Element


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

    def feed_html_body_only(self, dangerous_html_data):
        """Feed self the given HTML <body> section only
        (AsciiDoc might produce a document <head> section containing
        non-escaped 'less-than' signs that confuse the Python 2.x HTMLParser)
        """
        html.parser.HTMLParser.feed(
            self,
            PRX_HTML_BODY.sub('\\1\n\\2',
                              dangerous_html_data))

    def error(self, message):
        """override _markupbase.ParserBase abstract method"""
        raise ValueError(message)

    def handle_data(self, data):
        """Collect content"""
        self.__add_body_content(data)

    def handle_charref(self, name):
        """Resolve numeric character reference"""
        self.__add_body_content(resolve_charref(name))

    def handle_entityref(self, name):
        """Resolve a named entity reference, use the entity reference
        itself as fallback in case the name could not be resolved.
        """
        try:
            self.__add_body_content(resolve_entityref(name))
        except KeyError:
            self.__add_body_content(FS_ENTITY.format(name))
        #

    def handle_starttag(self, tag, attrs):
        """Handle a start tag"""
        if tag in INLINE_ELEMENTS:
            self.__add_body_content(constants.BLANK)
        else:
            self.__add_body_content(constants.NEWLINE)
        if tag == TAG.body:
            self.__in_body = True
        elif tag == TAG.img:
            # save images' alt texts
            attrs_map = dict(attrs)
            try:
                self.__image_descriptions.append(attrs_map[KEY.alt])
            except KeyError:
                pass
            #
        #

    def handle_endtag(self, tag):
        """Handle an end tag"""
        if tag == TAG.body:
            self.__in_body = False
        if tag in INLINE_ELEMENTS:
            self.__add_body_content(constants.BLANK)
        else:
            self.__add_body_content(constants.NEWLINE)
        #


class Translation():

    """Translations class, providing some standard classmethods"""

    amp_text = constants.AMPERSAND
    amp_xml = escape(amp_text)
    prx_named_entity = re.compile(FS_ENTITY.format(r'([a-z]\w+?)'))
    prx_numeric_entity = \
        re.compile(FS_NUMERIC_ENTITY.format(r'(\d+|x[\da-f]+)'))
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
        return input_string.encode(KEY.ascii, KEY.xmlcharrefreplace)

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
        return cls.prx_numeric_entity.sub(resolve_matched_charref,
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
        return cls.prx_named_entity.sub(resolve_matched_entityref,
                                        cls.from_xmlentities(input_string))


#
# End of class definitions, start of function definitions
#


def xml_declaration(version=XML_VERSION,
                    encoding=constants.UTF8,
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
        tag_attributes=make_attributes_string(
            version=version,
            encoding=encoding,
            standalone=standalone))


def xml_document(content,
                 version=XML_VERSION,
                 encoding=constants.UTF8,
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
