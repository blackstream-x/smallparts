# smallparts.text.reduce

Source: [smallparts/text/reduce.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/text/reduce.py)

Classes, functions and rules for reducing unicode text to ASCII.

## Module contents

...

### Constants

smallparts.text.reduce.**LATIN**

Latin characters from the
Latin-1 supplement (U0080–U00ff) and
Latin extended-A (U0100–U017f) Unicode blocks
and their ASCII replacements.

...

### Class:

*class* smallparts.text.reduce.**ConversionTable**(*rules_mapping, default_replacement='{}'*)

Objects of this class keep an internal mapping
from unicode characters to ASCII characters or strings,
which is built from the provided rules_mapping dict.

(tbc)
