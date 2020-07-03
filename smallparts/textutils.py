# -*- coding: utf-8 -*-

"""

textutils - text utility functions

"""

import re
import string

from . import constants


FS_0 = '{0}'
KNOWN_CODECS = ('utf_8_sig', 'iso-8859-1')


class MakeTranslationFunction(object):

    """Make a function for multiple replacements
    (adapted from Python Cookbook, Recipe 1.18)
    """

    def __init__(self, *args, **kwds):
        """Build a mapping of strings and their replacements,
        precompile the catch-all regular expression"""
        self.replacements = dict(*args, **kwds)
        self.prx_catch_all = self.precompile_regex()

    def __call__(self, original_text):
        """Execute the second form of regular expression substitution
        using a function instead of a string as replacement,
        see <https://docs.python.org/library/re.html#re.sub>
        """
        return self.prx_catch_all.sub(self.single_translation,
                                      original_text)

    @property
    def catch_all_pattern(self):
        """Provide the catch-all regular expression pattern as a property"""
        return constants.PIPE.join(re.escape(single_pattern)
                                   for single_pattern
                                   in self.replacements)

    def precompile_regex(self):
        """Precompile the catch-all regular expression"""
        return re.compile(self.catch_all_pattern)

    def single_translation(self, match):
        """The core function performing the replacement
        of a single string"""
        return self.replacements[match.group(constants.ZERO)]


class CaseInsensitiveTranslation(MakeTranslationFunction):

    """Make a translation function that is case insensitive
    when searching. If the original match should be preserved
    in the output, specify a placeholder in the replacement
    (see FS_0) so it can be used as a format string.
    Both the keys and the values in the replacement dict
    must be unicode so the replacements can work
    (and case-insensitive non-ascii matches become possible).
    """

    def __init__(self, *args, **kwds):
        """provide an additional lookup directory"""
        super(CaseInsensitiveTranslation, self).__init__(*args, **kwds)
        self.__key_lookup = dict((key.lower(), key)
                                 for key in self.replacements)

    def precompile_regex(self):
        """Precompile the catch-all regular expression,
        case-insensitive
        """
        return re.compile(self.catch_all_pattern, re.I | re.U)

    def single_translation(self, match):
        """The core function performing the replacement
        of a single string
        """
        whole_match = match.group(constants.ZERO)
        try:
            replacement = self.replacements[whole_match]
        except KeyError:
            # case insensitive key lookup
            replacement = \
                self.replacements[self.__key_lookup[whole_match.lower()]]
        if FS_0 in replacement:
            replacement = replacement.format(whole_match)
        return replacement


class Template(string.Template):

    """string.Template subclass adding one property:
    the list of variable names from the template
    """

    prx_placeholder = re.compile(
        '{0}({1})|{0}{2}({1}){3}'.format(re.escape(string.Template.delimiter),
                                         string.Template.idpattern,
                                         re.escape(constants.BRACE_OPEN),
                                         re.escape(constants.BRACE_CLOSE)),
        re.I)

    @property
    def variable_names(self):
        """Return the list of variable names in the template"""
        return [constants.EMPTY.join(placeholder) for placeholder
                in self.prx_placeholder.findall(self.template)]


#
# End of classes, start of functions
#


def flattened_list(input_list):
    """Flatten the input list"""
    flattened = []
    for item in input_list:
        if isinstance(item, (tuple, list)):
            flattened.extend(item)
        else:
            flattened.append(item)
        #
    return flattened


def blank_joined(*parts):
    """return parts joined with a blank"""
    return constants.BLANK.join(parts)


def joined(*parts):
    """return parts joined"""
    return constants.EMPTY.join(parts)


def line_joined(*parts):
    """return parts joined with a newline"""
    return constants.NEWLINE.join(parts)


def joined_with(join_string, *parts):
    """return parts joined with the given string"""
    return join_string.join(parts)


def remove_trailing_underscores(name):
    """Remove trailing underscores"""
    return name.rstrip(constants.UNDERSCORE)


def translate_underscores(name):
    """translate underscores to dashes"""
    return name.replace(constants.UNDERSCORE, constants.DASH)


def underscores_to_blanks(name):
    """translate underscores to blanks"""
    return name.replace(constants.UNDERSCORE, constants.BLANK)


def replace_all_underscores(name):
    """Remove trailing underscores and translate underscores to dashes"""
    return translate_underscores(remove_trailing_underscores(name))


def enumeration(words_list,
                joiner=constants.COMMA_BLANK,
                last_joiner=' und '):
    """Return the words list, enumerated"""
    # work on a copy
    output_list = words_list[:-2]
    output_list.append(last_joiner.join(words_list[-2:]))
    return joiner.join(output_list)


def nested_enumeration(lists_list,
                       inner_joiner=constants.COMMA_BLANK,
                       inner_last_joiner=' und ',
                       joiner=constants.COMMA_BLANK,
                       last_joiner=' sowie '):
    """Return the nested, enumerated"""
    return enumeration(
        [enumeration(single_list,
                     joiner=inner_joiner,
                     last_joiner=inner_last_joiner)
         for single_list in lists_list],
        joiner=joiner,
        last_joiner=last_joiner)


def to_unicode_and_encoding_name(input_string):
    """Convert any given string to unicode and return a tuple:
    (unicode conversion result, detected encoding)
    """
    if isinstance(input_string, bytes):
        last_error = ValueError
        for current_codec in KNOWN_CODECS:
            try:
                return (input_string.decode(current_codec),
                        current_codec)
            except UnicodeDecodeError as unicode_error:
                last_error = unicode_error
            #
        #
        raise last_error
    else:
        return (input_string, 'unicode')
    #


def to_unicode(input_string):
    """Convert any given string to unicode"""
    if isinstance(input_string, bytes):
        last_error = ValueError
        for current_codec in KNOWN_CODECS:
            try:
                return input_string.decode(current_codec)
            except UnicodeDecodeError as unicode_error:
                last_error = unicode_error
            #
        #
        raise last_error
    else:
        return input_string
    #
    # return to_unicode_and_encoding_name(input_string)[constants.FIRST_INDEX]


def to_utf8(input_string):
    """Encode any given string to UTF-8"""
    return to_unicode(input_string).encode(constants.UTF8)


#
# Module testing section
#


if __name__ == '__main__':
    TEMPLATE = Template('$first fixed text ${second_variable} ...\n'
                        '${last_variable_3} END')
    print('Variables:')
    print(repr(TEMPLATE.variable_names))
    print(TEMPLATE.safe_substitute(dict(first='abc',
                                        second_variable='def',
                                        last_variable_3='ghi')))

# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
