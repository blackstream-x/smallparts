# smallparts.text.reduce

> Classes, functions and rules for reducing unicode text to ASCII.  
> Source: [smallparts/text/reduce.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/text/reduce.py)

## Module contents

### Constants

This module defines the following dicts:

smallparts.text.reduce.**LATIN**

> Latin characters from the Latin-1 supplement (U0080–U00ff) and
> Latin extended-A (U0100–U017f) Unicode blocks and their ASCII replacements.

smallparts.text.reduce.**PUNCTUATION**

> Punctuation and symbols from the Latin-1 supplement (U0080–U00ff) and
> General punctuation (U2000–U206f) Unicode blocks with near-equivalent
> ASCII replacements or short desciptions.  
> All Latin-1 supplement codepoints
> are covered either here or in the LATIN dict above.  
> The most part of the General punctuation block is also covered.

smallparts.text.reduce.**ISO_CURRENCY**

> ISO 4217 codes for all currency symbols from the Currency symbols (U20a0–U20bf)
> Unicode block that are clearly attributable.

smallparts.text.reduce.**NON_ISO_CURRENCY**

> Names for all currency symbols from the Currency symbols (U20a0–U20bf)
> Unicode block that are *not* clearly attributable or do not have a ISO 4217 code.

smallparts.text.reduce.**GERMAN_OVERRIDES**

> German-language overrides including U1e9e (ẞ, capital ß)

### Helper function

smallparts.text.reduce.**checked_ascii**(*unicode_text*)

> Returns *unicode_text* unchanged if it can be converted to ASCII,
> else raises a ValueError.  
> Raises a TypeError if a non-string object was given.
>
> This function is used internally in the ConversionTable class to check all
> replacements as well as the default replacement.

### Class:

*class* smallparts.text.reduce.**ConversionTable**(*rules_mapping, default_replacement=None, remove_c1_controls=False*)

Instances of this class keep an internal mapping from unicode characters
to ASCII characters or strings, which is built from the provided rules_mapping
dict. Call the **.reduce_character()** or **.reduce_text()** methods to apply the
defined reductions to single caracters or strings.

*Parameters:*
*   *rules_mapping* is the mapping from which the internal replacements mapping
    is built initially. A valid rules mapping consists of Unicode keys and
    ASCII-only strings as values.
    The constants in this module can serve as examples for valid rules mappings.
*   *default_replacement* / If provided as a valid ASCII-only string,
    characters not defined in the internal replacements mapping are replaced by
    this string.
*   *remove_c1_controls* / If set to True, characters from the C1 controls range
    (U0080–U009f) will be removed (i.e. replaced with empty strings).
  
ConversionTable instances and dicts (valid rules mappings as described above)
can be added to each other, resulting in a new ConversionTable instance.

Instances of the ConversionTable class have the following methods:

ConversionTable.**add_reduction_items**(*reduction_items*)

> Adds the items provided in the *reduction_items* sequence to the internal
> replacements mapping. Each replacement is fed to the **check_ascii()**
> helper function, causing a ValueError if an invalid replacement was provided.

ConversionTable.**reduce_character**(*character*)

> Reduces the given character to ASCII using the stored rules:  
> If the character is already ASCII, return it unchanged.  
> Otherwise, return the replacement defined for it.  
> If there is no replacement defined for it, return the default replacement.  
> If no default replacement is defined, return a unicode escape in one of the
> \xNN, \uNNNN or \uNNNNNNNN forms, depending on the character’s codepoint.

ConversionTable.**reduce_text**(*unicode_text*)

> Reduces the given text to ASCII by applying the **.reduce_character()**
> method to each of its characters.

The following attributes are also available:

ConversionTable.**reduction_items**

> The internal replacements mapping’s
> [items dictview](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects) 

ConversionTable.**default_replacement**

> Read-only access to the default replacement

### Function

smallparts.text.reduce.**latin_to_ascii**(*unicode_text,* _*_*additional_rules*)

> Reduces the given text to ASCII using basic latin rules (as defined in **LATIN**)
> plus the additional rules given as positional parameters after the text.
>
> Internally, this function first builds a ConversionTable instance from the
> **LATIN** dict, and adds the provided *additional_rules* (which may be
> either ConversionTable instances or dicts) one by one.  
> It returns the result from the accumulated ConversionTable’s
> **.reduce_text()** method applied to *unicode_text*.

## Usage examples

```python
>>> from smallparts.text import reduce
>>> reduce.latin_to_ascii('Fête de Noël')
'Fete de Noel'
>>> reduce.latin_to_ascii('Köln')
'Koln'
>>> reduce.latin_to_ascii('Köln', reduce.GERMAN_OVERRIDES)
'Koeln'
>>> reduce.latin_to_ascii('¼')
'\\xbc'
>>> reduce.latin_to_ascii('¼', reduce.PUNCTUATION)
'1/4'
>>> punctuation_table = reduce.ConversionTable(reduce.PUNCTUATION)
>>> punctuation_table.reduce_character('¼')
'1/4'
>>> punctuation_table.reduce_character('Ü')
'\\xdc'
>>> punctuation_and_latin = punctuation_table + reduce.LATIN
>>> punctuation_and_latin.reduce_character('¼')
'1/4'
>>> punctuation_and_latin.reduce_character('Ü')
'U'
>>> 
```

----
[(smallparts docs home)](./)

