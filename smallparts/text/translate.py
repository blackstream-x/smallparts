# -*- coding: utf-8 -*-

"""

smallparts.text.translate - text translation functions

"""

import re

from smallparts import constants


FS_0 = '{0}'


class MakeTranslationFunction():

    """Make a function for multiple replacements
    (adapted from Python Cookbook, Recipe 1.18)
    """

    def __init__(self, *args, **kwargs):
        """Build a mapping of strings and their replacements,
        precompile the catch-all regular expression"""
        self.replacements = dict(*args, **kwargs)
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

    def __init__(self, *args, **kwargs):
        """provide an additional lookup directory"""
        super(CaseInsensitiveTranslation, self).__init__(*args, **kwargs)
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


#
# End of classes, start of functions
#


def remove_trailing_underscores(name):
    """Remove trailing underscores"""
    return name.rstrip(constants.UNDERSCORE)


def underscores_to_dashes(name):
    """translate underscores to dashes"""
    return name.replace(constants.UNDERSCORE, constants.DASH)


def underscores_to_blanks(name):
    """translate underscores to blanks"""
    return name.replace(constants.UNDERSCORE, constants.BLANK)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
