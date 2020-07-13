# smallparts.sequences

Source: [smallparts/sequences.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/sequences.py)

Functions for sequences.

## Module contents

This module currently contains only one function.

smallparts.sequences.**flatten**(*iterable, depth=None*)

Returns a list containing all items in iterable which are either strings, bytes
or non-iterable objects.
This function uses recursion, thus expanding all iterables except strings or
bytes. You can limit recursion to *depth* levels by providing *depth* as a
positive number.


Example:

```python
>>> import smallparts.sequences
>>> smallparts.sequences.flatten(['a', 'bcd', ['e', 'fgh', 'ijk'], 'lm', 'nop'])
['a', 'bcd', 'e', 'fgh', 'ijk', 'lm', 'nop']
>>> 
```
