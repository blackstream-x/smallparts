# smallparts.l10n.languages

> Definitions of supported languages.  
> Source: [smallparts/l10n/languages.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/l10n/languages.py)

## Module contents

### Constants

smallparts.l10n.languages.**DE**

> ```'de'``` for german.

smallparts.l10n.languages.**EN**

> ```'en'``` for english.

smallparts.l10n.languages.**ES**

> ```'es'``` for spanish.

smallparts.l10n.languages.**FR**

> ```'fr'``` for french.

smallparts.l10n.languages.**DEFAULT**

> ```'en'``` like **EN**

smallparts.l10n.languages.**SUPPORTED**

> A set containing all supported (= all of the above) language abbreviations

### Helper function

smallparts.l10n.languages.**missing_translation**(*lang, message=None*)

> Returns the matching error message for the given *lang* argument,
> for use in an exception (**ValueError**) raised by l10n functions.
> It is used to distinguish between single missing translations
> and completely unsupported languages.  
> The *message* keyword argument can be provided to override the default
> error message for missing translations.

----
[(smallparts docs home)](./)

