# smallparts.lists

Source: [smallparts/lists.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/lists.py)

Functions for lists.

## Module contents

This module currently contains only one function.

smallparts.lists.**flatten**(*nested_list*)

Returns a copy of *nested_list* with direct members which are lists or tuples
expanded into the list. Note that this function does not do any recursion.

Example:

```python
>>> import smallparts.lists
>>> smallparts.lists.flatten(['a', 'bcd', ['e', 'fgh', 'ijk'], 'lm', 'nop'])
['a', 'bcd', 'e', 'fgh', 'ijk', 'lm', 'nop']
>>> 
```
