# -*- coding: utf-8 -*-

"""

smallparts.text.translate - text translation functions

"""

from smallparts import constants


def remove_trailing_underscores(name):
    """Remove trailing underscores"""
    return name.rstrip(constants.UNDERSCORE)


def underscores_to_blanks(name):
    """translate underscores to blanks"""
    return name.replace(constants.UNDERSCORE, constants.BLANK)


def underscores_to_dashes(name):
    """translate underscores to dashes"""
    return name.replace(constants.UNDERSCORE, constants.DASH)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
