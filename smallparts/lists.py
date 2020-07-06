# -*- coding: utf-8 -*-

"""

smallparts.lists

Utility functions for lists

"""

def flatten(nested_list):
    """Flatten the given nested list"""
    flattened_list = []
    for item in nested_list:
        if isinstance(item, (tuple, list)):
            flattened_list.extend(item)
        else:
            flattened_list.append(item)
        #
    return flattened_list


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
