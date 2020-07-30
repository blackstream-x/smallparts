# smallparts.text.translate

> Simple text transliterations.  
> Source: [smallparts/text/translate.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/text/translate.py)

## Module contents

This module defines the following functions:

smallparts.text.translate.**remove_trailing_underscores**(_name_)

> Remove all trailing underscores from the given name (i.e. string)

smallparts.text.translate.**underscores_to_blanks**(_name_)

> Replace all underscores by blanks

smallparts.text.translate.**underscores_to_dashes**(_name_)

> Replace all underscores by dashes

## Usage examples

```python
>>> from smallparts.text import translate
>>> translate.remove_trailing_underscores('example_name__')
'example_name'
>>> translate.underscores_to_blanks('example_name__')
'example name  '
>>> translate.underscores_to_dashes('example_name__')
'example-name--'
>>> 
```

----
[(smallparts docs home)](./)
----

