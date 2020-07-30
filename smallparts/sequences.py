# -*- coding: utf-8 -*-

"""

smallparts.sequences

Utility functions for sequences

"""


DEFAULT_JOINER = ','
EMPTY = ''


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


def raw_join(iterable,
             prefix=None,
             joiner=DEFAULT_JOINER,
             final_joiner=None,
             suffix=None):
    """Return a unicode string containing the list items
    joined together according to the provided parameters
    """
    final_joiner = final_joiner or joiner
    words_sequence = [str(item) for item in iterable]
    items_list = words_sequence[:-2]
    items_list.append(final_joiner. join(words_sequence[-2:]))
    return EMPTY.join((prefix or EMPTY,
                       joiner.join(items_list),
                       suffix or EMPTY))


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
