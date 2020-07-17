# -*- coding: utf-8 -*-

"""

smallparts.text.transcode

Universal text decoding and encoding functions,
with additional functions to read and write text files.

"""


import codecs
import logging
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
DEFAULT_WRITE_MODE = constants.MODE_WRITE_BINARY

#
# Functions
#


def to_unicode_and_encoding_name(
        input_object,
        from_encoding=None,
        fallback_encoding=DEFAULT_FALLBACK_ENCODING):
    """Try to decode the input object to a unicode string
    and return a tuple containing the conversion result
    and the source encoding name.

    If the input object is not a byte string, a TypeError is raised.

    Otherwise, the following algorithm is used:
        - If an explicit input codec was given, decode it using that codec.
        - Else, try each of the known encodings which use a Byte Order Mark,
          defined in the global BOM_ASSIGNMENTS list.
          If none of these Byte Order Marks was found, try to decode it
          using UTF-8. If that fails, use the fallback codec which is defined
          in the global DEFAULT_FALLBACK_ENCODING variable but can be
          overridden using the parameter fallback_encoding.
    """
    if isinstance(input_object, (bytes, bytearray)):
        if from_encoding:
            return (input_object.decode(from_encoding),
                    from_encoding)
        #
        for (bom, encoding) in BOM_ASSIGNMENTS:
            if input_object.startswith(bom):
                return (input_object[len(bom):].decode(encoding),
                        encoding)
            #
        #
        try:
            return (input_object.decode(constants.UTF_8),
                    constants.UTF_8)
        except UnicodeDecodeError:
            return (input_object.decode(fallback_encoding),
                    fallback_encoding)
        #
    #
    raise TypeError('This function requires bytes or bytearray as input,'
                    ' not {0}.'.format(input_object.__class__.__name__))


def to_unicode(input_object,
               from_encoding=None,
               fallback_encoding=DEFAULT_FALLBACK_ENCODING):
    """Wrap to_unicode_and_encoding_name(),
    but return the conversion result only."""
    return to_unicode_and_encoding_name(
        input_object,
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
        input_object,
        to_encoding=DEFAULT_TARGET_ENCODING):
    """Encode a unicode string to a bytes representation
    using the provided encoding
    """
    if isinstance(input_object, str):
        return input_object.encode(to_encoding)
    #
    raise TypeError('This function requires a unicode string as input,'
                    ' not {0}.'.format(input_object.__class__.__name__))


def anything_to_bytes(
        input_object,
        to_encoding=DEFAULT_TARGET_ENCODING,
        from_encoding=None,
        fallback_encoding=DEFAULT_FALLBACK_ENCODING):
    """Encode any given object to a bytes representation
    using the provided encoding, after decoding it to unicode
    using this modules's to_unicode() function
    """
    try:
        return to_bytes(input_object, to_encoding=to_encoding)
    except TypeError:
        return anything_to_unicode(
            input_object,
            from_encoding=from_encoding,
            fallback_encoding=fallback_encoding).encode(to_encoding)
    #


def to_utf8(input_object):
    """Encode the input object string to UTF-8
    using this modules's to_bytes() function
    """
    return to_bytes(input_object, to_encoding=constants.UTF_8)


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
        raise ValueError('This would not have any effect!')
    #
    return to_unicode(to_bytes(unicode_text, to_encoding=wrong_encoding))


def lines(input_object,
          from_encoding=None,
          fallback_encoding=DEFAULT_FALLBACK_ENCODING,
          keepends=False):
    """Iterate over the decoded input object's lines"""
    for single_line in to_unicode(
            input_object,
            from_encoding=from_encoding,
            fallback_encoding=fallback_encoding).splitlines(keepends=keepends):
        yield single_line
    #


def read_from_file(input_file,
                   from_encoding=None,
                   fallback_encoding=DEFAULT_FALLBACK_ENCODING):
    """Read input file and return its content as unicode"""
    try:
        return to_unicode(input_file.read(),
                          from_encoding=from_encoding,
                          fallback_encoding=fallback_encoding)
    except AttributeError:
        with open(input_file,
                  mode=constants.MODE_READ_BINARY) as real_input_file:
            return read_from_file(real_input_file,
                                  from_encoding=from_encoding,
                                  fallback_encoding=fallback_encoding)
        #
    #


def lines_from_file(input_file_or_name,
                    from_encoding=None,
                    fallback_encoding=DEFAULT_FALLBACK_ENCODING,
                    keepends=False):
    """Iterate over the decoded input file's lines"""
    decoded_file_content = read_from_file(
        input_file_or_name,
        from_encoding=from_encoding,
        fallback_encoding=fallback_encoding)
    for single_line in decoded_file_content.splitlines(keepends=keepends):
        yield single_line
    #


def prepare_file_output(input_object,
                        to_encoding=DEFAULT_TARGET_ENCODING,
                        from_encoding=None,
                        fallback_encoding=DEFAULT_FALLBACK_ENCODING,
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
                                fallback_encoding=fallback_encoding))
    #
    return anything_to_bytes(line_ending.join(lines_list),
                             to_encoding=to_encoding,
                             from_encoding=from_encoding)


# pylint: disable=too-many-arguments; required for versatility


def write_to_file(file_name,
                  input_object,
                  to_encoding=DEFAULT_TARGET_ENCODING,
                  from_encoding=None,
                  fallback_encoding=DEFAULT_FALLBACK_ENCODING,
                  line_ending=DEFAULT_LINE_ENDING,
                  write_mode=DEFAULT_WRITE_MODE):
    """Write the input object or list to the file specified by file_name"""
    with open(file_name,
              mode=write_mode) as output_file:
        output_file.write(
            prepare_file_output(input_object,
                                to_encoding=to_encoding,
                                from_encoding=from_encoding,
                                fallback_encoding=fallback_encoding,
                                line_ending=line_ending))
    #


def transcode_file(file_name,
                   to_encoding=DEFAULT_TARGET_ENCODING,
                   from_encoding=None,
                   fallback_encoding=DEFAULT_FALLBACK_ENCODING,
                   line_ending=None,
                   write_backup_file=True):
    """Read the input file and transcode it to the specified encoding IN PLACE.
    Preserve original line endings except when specified explicitly.
    Write a backup file unless explicitly told not to do that.
    """
    with open(file_name,
              mode=constants.MODE_READ_BINARY) as input_file:
        bytes_content = input_file.read()
    #
    unicode_content, detected_encoding = to_unicode_and_encoding_name(
        bytes_content,
        from_encoding=from_encoding,
        fallback_encoding=fallback_encoding)
    if detected_encoding == to_encoding:
        logging.warning('File %r is already encoded in %r!',
                        file_name,
                        to_encoding)
        return False
    #
    if write_backup_file:
        file_name_root, file_extension = os.path.splitext(file_name)
        backup_file_name = '{0}.{1}{2}'.format(
            file_name_root, detected_encoding, file_extension)
        shutil.move(file_name, backup_file_name)
    #
    if line_ending in (constants.LF, constants.CRLF):
        unicode_content = line_ending.join(
            split.lines_for_reconstruction(unicode_content))
    #
    with open(file_name,
              mode=constants.MODE_WRITE_BINARY) as output_file:
        output_file.write(to_bytes(unicode_content, to_encoding=to_encoding))
    #
    return True


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
