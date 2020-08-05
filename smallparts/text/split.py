# -*- coding: utf-8 -*-

"""

smallparts.text.split

Text splitting functions

"""


def lines_for_reconstruction(unicode_text):
    """Split unicode_text using the splitlines() str method,
    but append an empty string at the end if the last line
    of the original text ends with a line break, in order
    to be able to keep this trailing line end when applying
    LINE_BREAK.join(splitted_lines).
    The line break characters below were taken from
    <https://docs.python.org/3/library/stdtypes.html#str.splitlines>
    """
    if isinstance(unicode_text, str):
        splitted_lines = unicode_text.splitlines()
    else:
        raise TypeError('This function requires a unicode argument.')
    #
    if unicode_text and \
            unicode_text[-1] in '\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029':
        splitted_lines.append('')
    #
    return splitted_lines


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
