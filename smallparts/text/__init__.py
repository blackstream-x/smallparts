# -*- coding: utf-8 -*-

"""

smallparts.text

text subpackage

"""


COMMA_BLANK = ', '
FINAL_JOIN_EXPRESSION = ' und '
OUTER_FINAL_JOIN_EXPRESSION = ' sowie '


def enumeration(
        words_sequence,
        join_expression=COMMA_BLANK,
        final_join_expression=FINAL_JOIN_EXPRESSION):
    """Return the words list, enumerated"""
    # work on a copy
    output_list = words_sequence[:-2]
    output_list.append(final_join_expression.join(words_sequence[-2:]))
    return join_expression.join(output_list)


def nested_enumeration(
        nested_words_sequence,
        inner_final_join_expression=FINAL_JOIN_EXPRESSION,
        join_expression=COMMA_BLANK,
        final_join_expression=OUTER_FINAL_JOIN_EXPRESSION):
    """Return the nested, enumerated"""
    return enumeration(
        [enumeration(
            inner_sequence,
            join_expression=join_expression,
            final_join_expression=inner_final_join_expression)
         for inner_sequence in nested_words_sequence],
        join_expression=join_expression,
        final_join_expression=final_join_expression)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
