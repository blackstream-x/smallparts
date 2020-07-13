# -*- coding: utf-8 -*-

"""

smallparts.text.reduce

Classes, functions and rules for reducing unicode text to ASCII

"""

#
# Reduction rules as dicts: {source_characters: ascii_replacement, …}
#

LATIN = {
    # Latin characters from the
    # Latin-1 supplement (U0080–U00ff) and
    # Latin extended-A (U0100–U017f) Unicode blocks
    #
    'ÀÁÂÃÄÅĀĂĄ': 'A',
    'Æ': 'Ae',
    'ÇĆĈĊČ': 'C',
    'Ď': 'D',
    'ÐĐ': 'Dh',
    'ÈÉÊËĒĔĖĘĚ': 'E',
    'ĜĞĠĢ': 'G',
    'ĤĦ': 'H',
    'ÌÍÎÏĨĪĬĮİ': 'I',
    'Ĳ': 'IJ',
    'Ĵ': 'J',
    'Ķ': 'K',
    'ĹĻĽĿŁ': 'L',
    'ÑŃŅŇ': 'N',
    'Ŋ': 'Ng',
    'ÒÓÔÕÖŌŎŐØ': 'O',
    'Œ': 'Oe',
    'ŔŖŘ': 'R',
    'ŚŜŞŠ': 'S',
    'ŢŤŦ': 'T',
    'Þ': 'Th',
    'ÙÚÛÜŨŪŬŮŰŲ': 'U',
    'Ŵ': 'W',
    'ÝŶŸ': 'Y',
    'ŹŻŽ': 'Z',
    'àáâãäåāăą': 'a',
    'æ': 'ae',
    'çćĉċč': 'c',
    'ď': 'd',
    'ðđ': 'dh',
    'èéêëēĕėęě': 'e',
    'ĝğġģ': 'g',
    'ĥħ': 'h',
    'ìíîïĩīĭįı': 'i',
    'ĳ': 'ij',
    'ĵ': 'j',
    'ķĸ': 'k',
    'ĺļľŀł': 'l',
    'ñńņň': 'n',
    'ŋ': 'ng',
    'òóôõöōŏőø': 'o',
    'œ': 'oe',
    'ŕŗř': 'r',
    'śŝşšſ': 's',
    'ß': 'ss',
    'ţťŧ': 't',
    'þ': 'th',
    'ùúûüũūŭůűų': 'u',
    'ŵ': 'w',
    'ýŷÿ': 'y',
    'źżž': 'z'
}

PUNCTUATION = {
    # Punctuation and symbols from the
    # Latin-1 supplement (U0080–U00ff) and
    # General punctuation (U2000–U206f) Unicode blocks
    #
    # Spacing characters → space
    '\u0080\u2000\u2001\u2002\u2003\u2004'
    '\u2005\u2006\u2007\u2008\u2009\u200a': '\x20',
    # Soft hyphen → hyphen in parentheses
    '\u00ad': '(-)',
    # Hyphen bullet → hyphen
    '\u2043': '-',
    # Dashes → single or double hyphen
    '\u2010\u2011\u2012\u2013': '-',
    '\u2014\u2015': '--',
    # Quotation marks → apostrophe, quotation mark, << or >>
    '\u2018\u2019\u201a\u201b': '\x27',
    '\u201c\u201d\u201e\u201f': '"',
    '«': '<<',
    '»': '>>',
    # Leader dots, ellipsis → dots
    '\u2024': '.',
    '\u2025': '..',
    '\u2026': '...',
    # Bullets, middle dots, times sign → asterisk
    '\u00b7\u00d7\u2022\u2027\u204c\u204d\u204e': '*',
    # Line and paragraph separators → ASCII LF
    '\u2028': '\n',
    '\u2029': '\n\n',
    # Per mille and per myriad (= per then thousand) signs → {description}
    '\u2030': '{permille}',
    '\u2031': '{permyriad}',
    # Primes → apostrophes, reverse primes → grave accents
    '\u2032': '\x27',
    '\u2033': '\x27\x27',
    '\u2034': '\x27\x27\x27',
    '\u2057': '\x27\x27\x27\x27',
    '\u2035': '\x60',
    '\u2036': '\x60\x60',
    '\u2037': '\x60\x60\x60',
    # Caret, angle quotation marks → circumflex, less-than, greater than
    '\u2038': '^',
    '\u2039': '<',
    '\u203a': '>',
    # Exclamation and question marks, semicolon
    '¡': '!',
    '¿': '?',
    '\u203c': '!!',
    '\u203d': '?!',
    '\u2047': '??',
    '\u2048': '?!',
    '\u2049': '!?',
    '\u204f': ';',
    # Division sign and fraction slash → slash
    '÷\u2044': '/',
    # Tironian sign et → ampersand
    '\u204a': '&',
    # Various punctuation and symbols from the U2000 block
    '\u204b': '{reversed pilcrow}\n',
    '\u2051': '**',
    '\u2052': './.',
    '\u2053': '~',
    '\u2055': '*',
    # Various punctuation and symbols from the U0080 block
    '¢': 'ct',
    '£': 'GBP',
    '¤': '{currency}',
    '¥': 'JPY',
    '¦': '|',
    '§': '{section sign}',
    '¨': '"',
    '©': '(C)',
    'ª': '^a',
    '¬': '{not}',
    '®': '(R)',
    '¯': '{macron}',
    '°': '{degree}',
    '±': '+-',
    '¹': '^1',
    '²': '^2',
    '³': '^3',
    '´': '\x27',
    'µ': '{micro}',
    '¶': '{pilcrow}\n',
    '¸': '{cedilla}',
    'º': '^o',
    '¼': '1/4',
    '½': '1/2',
    '¾': '3/4'
}

ISO_CURRENCY = {
    # ISO 4217 codes for all currency symbols from the
    # Currency symbols (U20a0–U20bf) Unicode block
    # that are clearly attributable
    #
    '₠': 'ECU',
    '₣': 'FRF',
    '₦': 'NGN',
    '₧': 'ESP',
    '₪': 'ILS',
    '₫': 'VND',
    '€': 'EUR',
    '₭': 'LAK',
    '₮': 'MNT',
    '₯': 'GRD',
    '₱': 'PHP',
    '₲': 'PYG',
    '₳': 'ARA',
    '₴': 'UAH',
    '₵': 'GHS',
    '₸': 'KZT',
    '₹': 'INR',
    '₺': 'TRY',
    '₼': 'AZN',
    '₽': 'RUB',
    '₾': 'GEL',
    '₿': 'BTC',
    'ƒ': 'NLG',
    '฿': 'THB',
    '৳': 'BDT'
}

NON_ISO_CURRENCY = {
    # Names for all currency symbols from the
    # Currency symbols (U20a0–U20bf) Unicode block that are
    # NOT clearly attributable or do not have a ISO 4217 code
    #
    '₡': '{Colon}',             # CRC and SVC
    '₢': '{Cruzeiro}',          # BRB, BRC, BRN, BRE, BRR
    '₤': '{Lira}',              # ITL, MTL, SML, VAL, possybly also SYP
    '₥': '{Mill}',              # former US currency unit (1/1000 $)
    '₨': '{Rupee}',             # various currencies; Indian Rupee: see INR
    '₩': '{Won}',               # KPW and KRW
    '₰': '{Pfennig}',           # former German curreny unit (1/100 Mark)
    '₶': '{Livre tournois}',    # former French currency, 13th to 18th century
    '₷': '{Spesmilo}',          # historical proposed int'l currency
    '₻': '{Nordic Mark}'        # Danish rigsdaler
}

GERMAN_OVERRIDES = {
    # German-language overrides including U1e9e (ẞ, capital ß)
    #
    'Ä': 'Ae',
    'ÖŐØ': 'Oe',
    'ẞ': 'SZ',
    'ÜŰ': 'Ue',
    'ä': 'ae',
    'öőø': 'oe',
    'üű': 'ue',
    '\u2030': '{Promille}',
    '¤': '{Waehrung}',
    '§': 'Par.',
    '¬': '{nicht}',
    '°': '{Grad}',
    '¶': '{Absatzmarke}\n',
    '¸': '{Cedille}',
    '₰': 'Pf.'
}


#
# Internal helper functions
#


def _check_ascii_replacement(characters, replacement):
    """Raise a ValueError if the replacement is not ASCII only"""
    try:
        replacement.encode('ascii')
    except UnicodeEncodeError:
        raise ValueError(
            'Replacements must be ASCII only,'
            ' the provided replacement {0!r}'
            ' for {1!r} is invalid!'.format(
                replacement, characters))
    #


#
# Classes
#


class ConversionTable:

    """Conversion table for reductions to ASCII"""

    max_ascii = '\x7f'
    max_c1_control = '\x9f'

    def __init__(self, rules_mapping, default_replacement='{}'):
        """Set up the internal conversion mapping
        from the given rules mapping
        (key: string of characters to convert; value: ASCII replacement)
        """
        self.__reductions = {}
        self.add_reductions(rules_mapping)
        self.default_replacement = default_replacement

    @property
    def reductions(self):
        """Read only access to self.__reductions (snapshot copy)"""
        return dict(self.__reductions)

    def add_reductions(self, rules_mapping):
        """Add values from the given mapping to the internal mapping"""
        for source_characters, replacement in rules_mapping.items():
            _check_ascii_replacement(source_characters, replacement)
            for character in source_characters:
                self.__reductions[character] = replacement
            #
        #

    def __add__(self, other):
        """Return a new object as a copy, with the internal mapping
        updated form the added object's mapping
        """
        if isinstance(other, ConversionTable):
            mapping_to_add = other.reductions
        elif isinstance(other, dict):
            mapping_to_add = other
        else:
            raise TypeError('Cannot add any other type than'
                            ' ConversionTable or dict!')
        #
        result = ConversionTable(
            self.__reductions,
            default_replacement=self.default_replacement)
        result.add_reductions(mapping_to_add)
        return result

    def reduce_character(self, character):
        """Reduce a single unicode character according to the rules"""
        if character < self.max_ascii:
            return character
        #
        if character < self.max_c1_control:
            return ''
        #
        return self.__reductions.get(character, self.default_replacement)

    def reduce_text(self, unicode_text):
        """Reduce the provided unicode text character by character"""
        return ''.join(self.reduce_character(character)
                       for character in unicode_text)


#
# End of classes, start of functions
#


def latin_to_ascii(unicode_text, *additional_rules):
    """Reduce the given text to ascii using basic latin rules
    plus the additional rules given as positional parameters
    after the text
    """
    conversion_table = ConversionTable(LATIN)
    for rule in additional_rules:
        conversion_table = conversion_table + rule
    #
    return conversion_table.reduce_text(unicode_text)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
