# smallparts.text.reduce

Source: [smallparts/text/reduce.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/text/reduce.py)

Classes, functions and rules for reducing unicode text to ASCII.

## Module contents

### Constants

This module defines the following dicts:

smallparts.text.reduce.**LATIN**

Latin characters from the Latin-1 supplement (U0080–U00ff) and
Latin extended-A (U0100–U017f) Unicode blocks and their ASCII replacements.

smallparts.text.reduce.**PUNCTUATION**

Punctuation and symbols from the Latin-1 supplement (U0080–U00ff) and
General punctuation (U2000–U206f) Unicode blocks with near-equivalent
ASCII replacements or short desciptions.  
All Latin-1 supplement codepoints
are covered either here or in the LATIN dict above.  
The most part of the General punctuation block is also covered.

smallparts.text.reduce.**ISO_CURRENCY**

ISO 4217 codes for all currency symbols from the Currency symbols (U20a0–U20bf)
Unicode block that are clearly attributable.

smallparts.text.reduce.**NON_ISO_CURRENCY**

Names for all currency symbols from the Currency symbols (U20a0–U20bf)
Unicode block that are *not* clearly attributable or do not have a ISO 4217 code.

smallparts.text.reduce.**GERMAN_OVERRIDES**

German-language overrides including U1e9e (ẞ, capital ß)

### Helper function

smallparts.text.reduce.**checked_ascii**(*unicode_text*)

Returns *unicode_text* unchanged if it can be converted to ASCII,
else raises a ValueError.  
Raises a TypeError if a non-string object was given.

This function is used internally in the ConversionTable class.

### Class:

*class* smallparts.text.reduce.**ConversionTable**(*rules_mapping, default_replacement=None, remove_c1_controls=False*)

Instances of this class keep an internal mapping from unicode characters
to ASCII characters or strings, which is built from the provided rules_mapping
dict.

#### Parameters:

* *rules_mapping* is the mapping from which the internal replacements mapping
is built initially. The constants in this module, especially **LATIN**,
are good starting values.
* *default_replacement* if provided as a valid ASCII-only string,
characters not defined in the internal replacements mapping are replaced by
this string.  
If no default replacement is provided, unmatched characters will be replaced by
either a \xNN, \uNNNN or \uNNNNNNNN unicode escape, depending on their codepoint.
* *remove_c1_controls* if set to True, characters from the C1 controls range
(U0080–U009f) will be removed (i.e. replaced with empty strings).

#### Methods:

(tba)

### Function

smallparts.text.reduce.**latin_to_ascii**(*unicode_text,* _*_*additional_rules*)

Reduces the given text to ASCII using basic latin rules (as defined in **LATIN**)
plus the additional rules given as positional parameters after the text.

Internally, this function first builds a ConversionTable instance from the
**LATIN** dict, and adds the provided *additional_rules* (which may be
either ConversionTable instances or dicts) one by one.  
It returns the result from the accumulated ConversionTable’s reduce_text() method
applied to *unicode_text*.

## Usage example(s)

(tba)
