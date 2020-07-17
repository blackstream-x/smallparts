# -*- coding: utf-8 -*-

"""

smallparts.text.join

Text joining functions where the parts are given as positional arguments

"""


def by_blanks(*parts):
    """return parts joined by blanks"""
    return ' '.join(parts)


def directly(*parts):
    """return parts joined directly"""
    return ''.join(parts)


def by_newlines(*parts):
    """return parts joined by newline characters - Unix style"""
    return '\n'.join(parts)


def by_crlf(*parts):
    """return parts joined by crlf - DOS style"""
    return '\r\n'.join(parts)


def using(join_string, *parts):
    """return parts joined using the given string"""
    return join_string.join(parts)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
