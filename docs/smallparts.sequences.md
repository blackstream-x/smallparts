# smallparts.sequences

> Functions for sequences.  
> Source: [smallparts/sequences.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/sequences.py)

## Module contents

This module defines the constant

smallparts.sequences.**DEFAULT_SEPARATOR**

> simply ```','``` (an ASCII comma)

and the following functions:

smallparts.sequences.**flatten**(*iterable, depth=None*)

> Returns a list containing all items in iterable which are either strings
> bytes or non-iterable objects.
> This function uses recursion, thus expanding all iterables except strings or
> bytes. You can limit recursion to *depth* levels by providing *depth* as a
> positive number.

smallparts.sequences.**raw_join**(_iterable, prefix=None, separator=_**DEFAULT_SEPARATOR**_,_ *final_separator=None, suffix=None*):

> Returns a unicode string containing the list items joined together according
> to the provided parameters.  
> *separator* is the string separating all items except the next-to-last and
> last ones in the returned string,
> *final_separator* is the string separating the next-to-last and last items,
> and defaults to the value of *separator*.  
> *prefix*  and *suffix* default to empty strings.

## Usage examples

```python
>>> from smallparts import sequences
>>> nested_list = [1, [2, [3, [4, [5, 6], 7], 8], 9], 10]
>>> sequences.flatten(nested_list)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> sequences.flatten(nested_list, depth=1)
[1, 2, [3, [4, [5, 6], 7], 8], 9, 10]
>>> sequences.flatten(nested_list, depth=2)
[1, 2, 3, [4, [5, 6], 7], 8, 9, 10]
>>> 
>>> sequences.raw_join(['a', 'b', 'c', 'd'])
'a,b,c,d'
>>> sequences.raw_join(['a', 'b', 'c', 'd'], separator=', ', final_separator=' and ')
'a, b, c and d'
>>> sequences.raw_join(['a', 'b', 'c', 'd'], separator='|', prefix='(', suffix=')')
'(a|b|c|d)'
>>> 

```

----
[(smallparts docs home)](./)

