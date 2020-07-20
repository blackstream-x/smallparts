# -*- coding: utf-8 -*-

"""

smallparts.text.translate - text translation functions

"""

import re

from smallparts import constants


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
