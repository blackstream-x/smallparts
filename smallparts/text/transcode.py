# -*- coding: utf-8 -*-

"""

smallparts.text.transcode

Universal text decoding and encoding functions,
with additional functions to read and write text files.

"""


import codecs
import re


# Encodings

CP1252 = 'cp1252'
UTF_8 = 'utf8'

BOM_ASSIGNMENTS = (
    (codecs.BOM_UTF32_BE, 'utf_32_be'),
    (codecs.BOM_UTF32_LE, 'utf_32_le'),
    (codecs.BOM_UTF16_BE, 'utf_16_be'),
    (codecs.BOM_UTF16_LE, 'utf_16_le'),
    (codecs.BOM_UTF8, 'utf_8_sig'))

# Line endings

LF = '\n'
CRLF = '\r\n'

# File access modes

MODE_APPEND_BINARY = 'ab'
MODE_READ_BINARY = 'rb'
MODE_WRITE_BINARY = 'wb'

# Defaults

DEFAULT_ENCODING = UTF_8
DEFAULT_INPUT_FALLBACK_CODEC = CP1252
DEFAULT_LINE_ENDING = LF
DEFAULT_WRITE_MODE = MODE_WRITE_BINARY

#
# Functions
#


def to_unicode_and_encoding_name(
        input_object,
        explicit_input_codec=None,
        input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC):
    """Try to decode the input object to a unicode string
    and return a tuple containing the conversion result
    and the source encoding name.

    Any conversion errors will raise the original exception
    (probably a UnicodeDecodeError).

    If the input object is already a string, the returned tuple will contain
    the original input object and the str class name (i.e. 'str').

    If the input object is not a byte string, a TypeError is raised.

    Otherwise, the following algorithm is used:
        - If an explicit input codec was given, decode it using that codec.
        - Else, try each of the known encodings which use a Byte Order Mark,
          defined in the global BOM_ASSIGNMENTS list.
          If none of these Byte Order Marks was found, try to decode it
          using UTF-8. If that fails, use the fallback codec which is defined
          in the global DEFAULT_INPUT_FALLBACK_CODEC variable but can be
          overridden using the parameter input_fallback_codec.
    """
    if isinstance(input_object, (bytes, bytearray)):
        if explicit_input_codec:
            return (input_object.decode(explicit_input_codec),
                    explicit_input_codec)
        #
        for (bom, encoding) in BOM_ASSIGNMENTS:
            if input_object.startswith(bom):
                return (input_object[len(bom):].decode(encoding),
                        encoding)
            #
        #
        try:
            return (input_object.decode(UTF_8),
                    UTF_8)
        except UnicodeDecodeError:
            return (input_object.decode(input_fallback_codec),
                    input_fallback_codec)
        #
    #
    raise TypeError('This function requires bytes or bytearray as input,'
                    ' not {0}.'.format(input_object.__class__.__name__))


def to_unicode(input_object,
               explicit_input_codec=None,
               input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC):
    """Wrap to_unicode_and_encoding_name(),
    but return the conversion result only."""
    return to_unicode_and_encoding_name(
        input_object,
        explicit_input_codec=explicit_input_codec,
        input_fallback_codec=input_fallback_codec)[0]


def anything_to_unicode(
        input_object,
        explicit_input_codec=None,
        input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC):
    """Safe wrapper around to_unicode() returning the string conversion
    of the input object if it was not a byte string
    """
    try:
        return to_unicode(
            input_object,
            explicit_input_codec=explicit_input_codec,
            input_fallback_codec=input_fallback_codec)
    except TypeError:
        return str(input_object)
    #


def to_bytes(
        input_object,
        encoding=DEFAULT_ENCODING):
    """Encode a unicode string to a bytes representation
    using the provided encoding
    """
    if isinstance(input_object, str):
        return input_object.encode(encoding)
    #
    raise TypeError('This function requires a unicode string as input,'
                    ' not {0}.'.format(input_object.__class__.__name__))


def anything_to_bytes(
        input_object,
        encoding=DEFAULT_ENCODING,
        explicit_input_codec=None,
        input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC):
    """Encode any given object to a bytes representation
    using the provided encoding, after decoding it to unicode
    using this modules's to_unicode() function
    """
    try:
        return to_bytes(input_object, encoding=encoding)
    except TypeError:
        return anything_to_unicode(
            input_object,
            explicit_input_codec=explicit_input_codec,
            input_fallback_codec=input_fallback_codec).encode(encoding)
    #


def to_utf8(input_object):
    """Encode the input object string to UTF-8
    using this modules's to_bytes() function
    """
    return to_bytes(input_object, encoding=UTF_8)


def anything_to_utf8(
        input_object,
        explicit_input_codec=None,
        input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC):
    """Encode any given object to its UTF-8 representation
    using this modules's to_bytes() function
    """
    return anything_to_bytes(input_object,
                             encoding=UTF_8,
                             explicit_input_codec=explicit_input_codec,
                             input_fallback_codec=input_fallback_codec)


def lines(input_object,
          explicit_input_codec=None,
          input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC,
          keepends=False):
    """Iterate over the decoded input object's lines"""
    for single_line in to_unicode(
            input_object,
            explicit_input_codec=explicit_input_codec,
            input_fallback_codec=input_fallback_codec).\
                splitlines(keepends=keepends):
        yield single_line
    #


def read_from_file(input_file,
                   explicit_input_codec=None,
                   input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC):
    """Read input file and return its content as unicode"""
    try:
        return to_unicode(input_file.read(),
                          explicit_input_codec=explicit_input_codec,
                          input_fallback_codec=input_fallback_codec)
    except AttributeError:
        with open(input_file,
                  mode=MODE_READ_BINARY) as real_input_file:
            return read_from_file(real_input_file,
                                  explicit_input_codec=explicit_input_codec,
                                  input_fallback_codec=input_fallback_codec)
        #
    #


def lines_from_file(input_file_or_name,
                    explicit_input_codec=None,
                    input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC,
                    keepends=False):
    """Iterate over the decoded input file's lines"""
    for single_line in read_from_file(
            input_file_or_name,
            explicit_input_codec=explicit_input_codec,
            input_fallback_codec=input_fallback_codec).\
                splitlines(keepends=keepends):
        yield single_line
    #


def prepare_file_output(input_object,
                        encoding=DEFAULT_ENCODING,
                        explicit_input_codec=None,
                        input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC,
                        line_ending=DEFAULT_LINE_ENDING):
    """Return a bytes representation of the input object
    suitable for writing to a file using mode MODE_WRITE_BINARY.
    """
    if isinstance(input_object, (tuple, list)):
        lines_list = []
        for line in input_object:
            assert isinstance(line, str)
            lines_list.append(line)
        #
    else:
        lines_list = list(lines(input_object,
                                input_fallback_codec=input_fallback_codec))
    #
    return anything_to_bytes(line_ending.join(lines_list),
                             encoding=encoding,
                             explicit_input_codec=explicit_input_codec)


# pylint: disable=too-many-arguments; required for versatility


def write_to_file(file_name,
                  input_object,
                  encoding=DEFAULT_ENCODING,
                  explicit_input_codec=None,
                  input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC,
                  line_ending=DEFAULT_LINE_ENDING,
                  write_mode=DEFAULT_WRITE_MODE):
    """Write the input object or list to the file specified by file_name"""
    with open(file_name,
              mode=write_mode) as output_file:
        output_file.write(
            prepare_file_output(input_object,
                                encoding=encoding,
                                explicit_input_codec=explicit_input_codec,
                                input_fallback_codec=input_fallback_codec,
                                line_ending=line_ending))
    #


# pylint: enable=too-many-arguments


def _splitlines(unicode_text):
    """Split unicode_text into lines using some kind of poor man's
    universal newline support.
    We cannot use str.splitlines() here
    because it does not preserve trailing empty lines.
    """
    return re.split(r'(?:\r\n|\r|\n)', unicode_text)


def transcode_file(file_name,
                   encoding=DEFAULT_ENCODING,
                   explicit_input_codec=None,
                   input_fallback_codec=DEFAULT_INPUT_FALLBACK_CODEC,
                   line_ending=None):
    """Read the input file and transcode it to the specified encoding IN PLACE.
    Preserve original line endings except when specified explicitly.
    """
    unicode_content = read_from_file(
        file_name,
        explicit_input_codec=explicit_input_codec,
        input_fallback_codec=input_fallback_codec)
    if line_ending in (LF, CRLF):
        unicode_content = line_ending.join(_splitlines(unicode_content))
    #
    with open(file_name,
              write_mode=MODE_WRITE_BINARY) as output_file:
        output_file.write(to_bytes(unicode_content, encoding=encoding))
    #


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
