# -*- coding: utf-8 -*-

"""

smallparts.sequences

Utility functions for sequences

"""


def flatten(iterable, depth=None):
    """Flatten the given iterable recursively and return a list."""
    if isinstance(iterable, (str, bytes)):
        return [iterable]
    #
    if depth is None:
        children_depth = None
    else:
        children_depth = depth - 1
        if depth < 0:
            return [iterable]
        #
    #
    flattened_list = []
    try:
        for item in iterable:
            flattened_list.extend(flatten(item, depth=children_depth))
        #
    except TypeError:
        return [iterable]
    else:
        return flattened_list
    #


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
