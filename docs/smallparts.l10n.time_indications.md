# smallparts.l10n.time_indications

> Translations of time indications.  
> Source: [smallparts/l10n/time_indications.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/l10n/time_indications.py)

## Module contents

### Constants

smallparts.l10n.time_indications.**SECONDS**

> ```'seconds'```

smallparts.l10n.time_indications.**MINUTES**

> ```'minutes'```

smallparts.l10n.time_indications.**HOURS**

> ```'hours'```

smallparts.l10n.time_indications.**DAYS**

> ```'days'```

smallparts.l10n.time_indications.**WEEKS**

> ```'weeks'```

smallparts.l10n.time_indications.**MONTHS**

> ```'months'```

smallparts.l10n.time_indications.**YEARS**

> ```'years'```

smallparts.l10n.time\_indications.**SUPPORTED_UNITS**

> A tuple containing all supported (= all of the above) time units.

smallparts.l10n.time\_indications.**NUMBER_CATEGORIES**

> A dict containing singular and plural forms of all supported time units
> per supported language.

### Function

smallparts.l10n.time\_indications.**pretty\_print\_component**(*lang='en', \*\*kwargs*)

> Returns the time component given as a keyword argument, pretty printed
> in the language *lang* as defined in **NUMBER_CATEGORIES**.
> If multiple time components are given, only the smallest unit is processed.  
> Raises a ValueError if no time component was given.

## Usage examples

```python
>>> from smallparts.l10n import time_indications
>>> time_indications.pretty_print_component(seconds=1)
'1 second'
>>> time_indications.pretty_print_component(seconds=5)
'5 seconds'
>>> time_indications.pretty_print_component(seconds=7, minutes=1, lang='fr')
'7 secondes'
>>> time_indications.pretty_print_component(minutes=1, lang='fr')
'1 minute'
>>> 
```

----
[(smallparts docs home)](./)

