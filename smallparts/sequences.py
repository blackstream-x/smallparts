# -*- coding: utf-8 -*-

"""

smallparts.sequences

Utility functions for sequences

"""


def flatten(iterable):
    """Flatten the given iterable recursively and return a list."""
    if isinstance(iterable, (str, bytes)):
        return [iterable]
    #
    flattened_list = []
    try:
        for item in iterable:
            flattened_list.extend(flatten(item))
        #
    except TypeError:
        return [iterable]
    else:
        return flattened_list
    #


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
