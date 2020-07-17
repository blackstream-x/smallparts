# smallparts.text.split

> Text splitting functions.
> Source: [smallparts/text/split.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/text/split.py)

## Module contents

This module defines the following function:

smallparts.text.split.**lines_for_reconstruction**(*unicode_text*)

> Splits *unicode_text* using the standard library’s **str.splitlines()** method,
> and append an empty string at the end (only) if the last line
> of the original text ends with a line break.
>
> That way, the splitted result can be joined back using a line break character
> and keep a trailing line break which would be lost if only using
> **str.splitlines()**.

## Usage examples

```python
>>> from smallparts.text import split
>>> split.lines_for_reconstruction('first,\nsecond and\nthird line\n')
['first,', 'second and', 'third line', '']
>>> split.lines_for_reconstruction('first,\nsecond and\nthird line')
['first,', 'second and', 'third line']
>>> # for comparison:
>>> 'first,\nsecond and\nthird line\n'.splitlines()
['first,', 'second and', 'third line']
>>> 'first,\nsecond and\nthird line'.splitlines()
['first,', 'second and', 'third line']
>>> 
```

