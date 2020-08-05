# -*- coding: utf-8 -*-

"""

smallparts.text.transcode

Universal text decoding and encoding functions,
with additional functions to read and write text files.

"""


import codecs
import os.path
import shutil

from smallparts import constants

from smallparts.text import split


# Encodings with byte order marks

BOM_ASSIGNMENTS = (
    (codecs.BOM_UTF32_BE, 'utf_32_be'),
    (codecs.BOM_UTF32_LE, 'utf_32_le'),
    (codecs.BOM_UTF16_BE, 'utf_16_be'),
    (codecs.BOM_UTF16_LE, 'utf_16_le'),
    (codecs.BOM_UTF8, 'utf_8_sig'))

DEFAULT_TARGET_ENCODING = constants.UTF_8
DEFAULT_FALLBACK_ENCODING = constants.CP1252
DEFAULT_LINE_ENDING = constants.LF

SUPPORTED_OUTPUT_LINE_ENDINGS = (
    constants.LF,
    constants.CRLF)

#
# Functions
#


def to_unicode_and_encoding_name(
        bytestring,
        from_encoding=None,
        fallback_encoding=DEFAULT_FALLBACK_ENCODING):
    """Try to decode bytestring to a unicode string
    and return a tuple containing the conversion result
    and the source encoding name.

    If bytestring is not a byte string, a TypeError is raised.

    Otherwise, the following algorithm is used:
        - If an explicit input codec was given, decode it using that codec.
        - Else, try each of the known encodings which use a Byte Order Mark,
          defined in the global BOM_ASSIGNMENTS list.
          If none of these Byte Order Marks was found, try to decode it
          using UTF-8. If that fails, use the fallback codec which is defined
          in the global DEFAULT_FALLBACK_ENCODING variable but can be
          overridden using the parameter fallback_encoding.
    """
    if isinstance(bytestring, (bytes, bytearray)):
        if from_encoding:
            return (bytestring.decode(from_encoding),
                    from_encoding)
        #
        for (bom, encoding) in BOM_ASSIGNMENTS:
            if bytestring.startswith(bom):
                return (bytestring[len(bom):].decode(encoding),
                        encoding)
            #
        #
        try:
            return (bytestring.decode(constants.UTF_8),
                    constants.UTF_8)
        except UnicodeDecodeError:
            return (bytestring.decode(fallback_encoding),
                    fallback_encoding)
        #
    #
    raise TypeError('This function requires bytes or bytearray as input,'
                    ' not {0}.'.format(bytestring.__class__.__name__))


def to_unicode(bytestring,
               from_encoding=None,
               fallback_encoding=DEFAULT_FALLBACK_ENCODING):
    """Wrap to_unicode_and_encoding_name(),
    but return the conversion result only."""
    return to_unicode_and_encoding_name(
        bytestring,
        from_encoding=from_encoding,
        fallback_encoding=fallback_encoding)[0]


def anything_to_unicode(
        input_object,
        from_encoding=None,
        fallback_encoding=DEFAULT_FALLBACK_ENCODING):
    """Safe wrapper around to_unicode() returning the string conversion
    of the input object if it was not a byte string
    """
    try:
        return to_unicode(
            input_object,
            from_encoding=from_encoding,
            fallback_encoding=fallback_encoding)
    except TypeError:
        return str(input_object)
    #


def to_bytes(
        unicode_text,
        to_encoding=DEFAULT_TARGET_ENCODING):
    """Encode unicode_text to a bytes representation
    using the provided encoding
    """
    if isinstance(unicode_text, str):
        return unicode_text.encode(to_encoding)
    #
    raise TypeError('This function requires a unicode string as input,'
                    ' not {0}.'.format(unicode_text.__class__.__name__))


def anything_to_bytes(
        input_object,
        to_encoding=DEFAULT_TARGET_ENCODING,
        from_encoding=None,
        fallback_encoding=DEFAULT_FALLBACK_ENCODING):
    """Encode any given object to a bytes representation
    using the provided encoding, after decoding it to unicode
    using this modules's anything_to_unicode() function
    """
    try:
        return to_bytes(input_object, to_encoding=to_encoding)
    except TypeError:
        return anything_to_unicode(
            input_object,
            from_encoding=from_encoding,
            fallback_encoding=fallback_encoding).encode(to_encoding)
    #


def to_utf8(unicode_text):
    """Encode unicode_text to UTF-8
    using this modules's to_bytes() function
    """
    return to_bytes(unicode_text, to_encoding=constants.UTF_8)


def anything_to_utf8(
        input_object,
        from_encoding=None,
        fallback_encoding=DEFAULT_FALLBACK_ENCODING):
    """Encode any given object to its UTF-8 representation
    using this modules's to_bytes() function
    """
    return anything_to_bytes(input_object,
                             to_encoding=constants.UTF_8,
                             from_encoding=from_encoding,
                             fallback_encoding=fallback_encoding)


def fix_double_utf8_transformation(unicode_text,
                                   wrong_encoding=constants.CP1252):
    """Fix duplicate UTF-8 transformation,
    which is a frequent result of reading UTF-8 encoded text as Latin encoded
    (CP-1252, ISO-8859-1 or similar), resulting in characters like Ã¤Ã¶Ã¼.
    This function reverts the effect.
    """
    if wrong_encoding == constants.UTF_8:
        raise ValueError('This cannot have any effect!')
    #
    return to_unicode(
        to_bytes(
            unicode_text,
            to_encoding=wrong_encoding),
        from_encoding=constants.UTF_8)


def read_from_file(input_file_or_name,
                   from_encoding=None,
                   fallback_encoding=DEFAULT_FALLBACK_ENCODING):
    """Read input file and return its contents as unicode"""
    try:
        file_contents = input_file_or_name.read()
    except AttributeError:
        with open(input_file_or_name,
                  mode=constants.MODE_READ_BINARY) as real_input_file:
            file_contents = real_input_file.read()
        #
    #
    return to_unicode(
        file_contents,
        from_encoding=from_encoding,
        fallback_encoding=fallback_encoding)


def prepare_file_output(unicode_content,
                        to_encoding=DEFAULT_TARGET_ENCODING,
                        line_ending=DEFAULT_LINE_ENDING):
    """Return a bytes representation of unicode_content,
    with the provided line_ending,
    suitable for writing to a file using mode MODE_WRITE_BINARY.
    """
    if line_ending not in SUPPORTED_OUTPUT_LINE_ENDINGS:
        raise ValueError(
            'line_ending must be one of {0!r}!'.format(
                SUPPORTED_OUTPUT_LINE_ENDINGS))
    #
    lines_list = []
    if isinstance(unicode_content, str):
        lines_list.extend(
            split.lines_for_reconstruction(unicode_content))
    else:
        for text_block in unicode_content:
            text_block_lines = split.lines_for_reconstruction(text_block)
            if not text_block_lines:
                lines_list.append('')
                continue
            #
            lines_list.extend(text_block_lines)
        #
    #
    return to_bytes(
        line_ending.join(lines_list),
        to_encoding=to_encoding)


def transcode_file(file_name,
                   to_encoding=DEFAULT_TARGET_ENCODING,
                   from_encoding=None,
                   fallback_encoding=DEFAULT_FALLBACK_ENCODING,
                   line_ending=None):
    """Read the input file and transcode it to the specified encoding in place.
    Raise a ValueError if the detected encoding is the same as the
    target encoding.
    Preserve original line endings except when specified explicitly.
    Rename the original file to the original name with the detected
    encoding name attached.
    """
    with open(file_name,
              mode=constants.MODE_READ_BINARY) as input_file:
        bytes_content = input_file.read()
    #
    unicode_content, detected_encoding = to_unicode_and_encoding_name(
        bytes_content,
        from_encoding=from_encoding,
        fallback_encoding=fallback_encoding)
    #
    # Check content encoding and raise a ValueError
    # if the original contents were already encoded
    # as to_encoding
    if bytes_content == to_bytes(unicode_content, to_encoding=to_encoding):
        raise ValueError(
            'File {0!r} is already encoded in {1!r}!'.format(
                file_name,
                to_encoding))
    #
    # Change line endings if requested
    if line_ending in SUPPORTED_OUTPUT_LINE_ENDINGS:
        unicode_content = line_ending.join(
            split.lines_for_reconstruction(unicode_content))
    elif line_ending is not None:
        raise ValueError(
            'line_ending – if provided – must be one of {0!r}!'.format(
                SUPPORTED_OUTPUT_LINE_ENDINGS))
    #
    # rename the original file to the backup file name
    file_name_root, file_extension = os.path.splitext(file_name)
    backup_file_name = '{0}.{1}{2}'.format(
        file_name_root, detected_encoding, file_extension)
    shutil.move(file_name, backup_file_name)
    #
    with open(file_name,
              mode=constants.MODE_WRITE_BINARY) as output_file:
        output_file.write(
            to_bytes(
                unicode_content,
                to_encoding=to_encoding))
    #


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
