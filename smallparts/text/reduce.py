# -*- coding: utf-8 -*-

"""

smallparts.text.reduce - Functions for reducing unicode text to ASCII

"""

# import re

# from smallparts import constants


MAX_ASCII = '\x7f'
MAX_C1_CONTROL = '\x9f'


# German-style ASCII replacements for characters in the
# Latin-1 Supplement, Latin Extended-A,
# and Currency Symbols Unicode ranges
# (U0080–U017F and U20A0–U20BF).
# and some additional characters:
# - Dutch Guilder (ƒ, U0192)
# - Thai Baht (฿, U0e3f)
# - Bangladesh Taka (৳, U09f3)
# - Capital ß (ẞ, U1e9e)
#
# Control charachters U0080–U009f are not replaced.

GERMAN_REDUCTIONS = {
    '\u0020': '\u00a0',
    '{!}': '¡',
    'ct': '¢',
    'GBP': '£',
    '{Waehrung}': '¤',
    'JPY': '¥',
    '|': '¦',
    '{Paragraf}': '§',
    '{"}': '¨',
    '(C)': '©',
    '{^a}': 'ª',
    '<<': '«',
    '{nicht}': '¬',
    '{(-)}': '\u00ad',
    '(R)': '®',
    '{Macron}': '¯',
    '{Grad}': '°',
    '{+-}': '±',
    '{^2}': '²',
    '{^3}': '³',
    "{'}": '´',
    '{Mikro}': 'µ',
    '{Absatzmarke}\n': '¶',
    '{*}': '·×',
    '{Cedille}': '¸',
    '{^1}': '¹',
    '{^o}': 'º',
    '>>': '»',
    '{1/4}': '¼',
    '{1/2}': '½',
    '{3/4}': '¾',
    '{?}': '¿',
    'A': 'ÀÁÂÃÅĀĂĄ',
    'Ae': 'ÄÆ',
    'C': 'ÇĆĈĊČ',
    'D': 'Ď',
    'Dh': 'ÐĐ',
    'E': 'ÈÉÊËĒĔĖĘĚ',
    'G': 'ĜĞĠĢ',
    'H': 'ĤĦ',
    'I': 'ÌÍÎÏĨĪĬĮİ',
    'IJ': 'Ĳ',
    'J': 'Ĵ',
    'K': 'Ķ',
    'L': 'ĹĻĽĿŁ',
    'N': 'ÑŃŅŇ',
    'Ng': 'Ŋ',
    'O': 'ÒÓÔÕŌŎŐ',
    'Oe': 'ÖØŒ',
    'R': 'ŔŖŘ',
    'S': 'ŚŜŞŠ',
    'T': 'ŢŤŦ',
    'Th': 'Þ',
    'U': 'ÙÚÛŨŪŬŮŰŲ',
    'Ue': 'Ü',
    'W': 'Ŵ',
    'Y': 'ÝŶŸ',
    'Z': 'ŹŻŽ',
    'a': 'àáâãåāăą',
    'ae': 'äæ',
    'c': 'çćĉċč',
    'd': 'ď',
    'dh': 'ðđ',
    'e': 'èéêëēĕėęě',
    'g': 'ĝğġģ',
    'h': 'ĥħ',
    'i': 'ìíîïĩīĭįı',
    'ij': 'ĳ',
    'j': 'ĵ',
    'k': 'ķĸ',
    'l': 'ĺļľŀł',
    'n': 'ñńņň',
    'ng': 'ŋ',
    'o': 'òóôõōŏő',
    'oe': 'öøœ',
    'r': 'ŕŗř',
    's': 'śŝşšſ',
    'ss': 'ß',
    't': 'ţťŧ',
    'th': 'þ',
    'u': 'ùúûũūŭůűų',
    'ue': 'ü',
    'w': 'ŵ',
    'y': 'ýŷÿ',
    'z': 'źżž',
    '/': '÷',
    'ECU': '₠',
    '{Colon}': '₡',
    '{Cruzeiro}': '₢',
    'FRF': '₣',
    '{Lira}': '₤',
    '{Mill}': '₥',
    'NGN': '₦',
    'ESP': '₧',
    '{Rupie}': '₨',
    '{Won}': '₩',
    'ILS': '₪',
    'VND': '₫',
    'EUR': '€',
    'LAK': '₭',
    'MNT': '₮',
    'GRD': '₯',
    'Pf.': '₰',
    'PHP': '₱',
    'PYG': '₲',
    '{Austral}': '₳',
    'UAH': '₴',
    'GHS': '₵',
    '{Livre Tournois}': '₶',
    '{Spesmilo}': '₷',
    'KZT': '₸',
    'INR': '₹',
    'TRY': '₺',
    '{Nordische Mark}': '₻',
    'AZN': '₼',
    'RUB': '₽',
    'GEL': '₾',
    'BTC': '₿',
    'NLG': 'ƒ',
    'THB': '฿',
    'BDT': '৳',
    'SZ': 'ẞ'
}

FS_0 = '{0}'


class MakeAsciiReductionFunction():

    """Make a function for reducing any given unicode string to ASCII
    using the replacements given in a dict of (replacement, source characters)
    pairs
    """

    default_replacement = '[_]'

    def __init__(self, replacements_map):
        """Build a mapping of strings and their replacements,
        precompile the catch-all regular expression"""
        self.replacements = []
        for (replacement, source_characters) in replacements_map.items():
            try:
                replacement.encode('ascii')
            except UnicodeEncodeError:
                raise ValueError('Replacements must be ASCII only!')
            #
            self.replacements.append((source_characters, replacement))
        #
        self.replacements.sort()

    def __call__(self, original_text):
        """
        """
        reduced = []
        for character in original_text:
            if character <= MAX_ASCII:
                reduced.append(character)
            elif character > MAX_C1_CONTROL:
                for (source_characters, replacement) in self.replacements:
                    if character in source_characters:
                        reduced.append(replacement)
                        break
                    #
                else:
                    reduced.append(self.default_replacement)
                #
            #
        #
        return ''.join(reduced)


#
# End of classes, start of functions
#


GERMAN_ASCII_REDUCER = MakeAsciiReductionFunction(GERMAN_REDUCTIONS)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
