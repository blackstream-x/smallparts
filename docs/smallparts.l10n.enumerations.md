# smallparts.l10n.enumerations

> Natural-language enumerations.  
> Source: [smallparts/l10n/enumerations.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/l10n/enumerations.py)

## Module contents

### Constants

smallparts.l10n.enumerations.**BLANK**

> ```' '```

smallparts.l10n.enumerations.**COMMA**

> ```','```

smallparts.l10n.enumerations.**EMPTY**

> ```''```

smallparts.l10n.enumerations.**AND**

> ```'and'```

smallparts.l10n.enumerations.**OR**

> ```'or'```

smallparts.l10n.enumerations.**EITHER**

> ```'either'```

smallparts.l10n.enumerations.**NEITHER**

> ```'neither'```

smallparts.l10n.enumerations.**BEFORE**

> ```'before'``` (keyword for spacing rules)

smallparts.l10n.enumerations.**AFTER**

> ```'after'``` (keyword for spacing rules)

smallparts.l10n.enumerations.**SUPPORTED_ENUMS**

> A tuple containing all supported enumeration types
> (AND, OR, EITHER, NEITHER).

smallparts.l10n.enumerations.**ENUM_SEPARATORS**

> A dict containing parameters for enumerations of all supported types
> per supported language.

smallparts.l10n.enumerations.**SPACING_RULES**

> A dict containing spacing rules per supported language.

### Functions

smallparts.l10n.enumerations.**apply\_spacing\_rules**(*separator, lang='en'*)

> Returns *separator* with added blanks before and/or after (or not),
>  as determined by the rules for *lang* from **SPACING_RULES**.

smallparts.l10n.enumerations.**enumeration**(*sequence, enum_type, lang='en'*)

> Returns a string containing the enumeration of *sequence* in *lang*,
> using the parameters defined in **ENUM_SEPARATORS** for *enum_type* and *lang*.  
> Uses the [smallparts.sequences](./smallparts.sequences.md).raw_join() function
> internally.

## Usage examples

```python
>>> from smallparts.l10n import enumerations
>>> enumerations.apply_spacing_rules(',', lang='en')
', '
>>> enumerations.apply_spacing_rules(',', lang='fr')
' , '
>>> enumerations.enumeration((1, 2, 3), enumerations.OR, lang='de')
'1, 2 oder 3'
>>> enumerations.enumeration(('sun', 'moon', 'stars'), enumerations.AND, lang='en')
'sun, moon and stars'
>>> 
```

----
[(smallparts docs home)](./)

