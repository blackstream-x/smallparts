# smallparts.text.join

> Text joining functions where the parts are given as positional arguments.
> Source: [smallparts/text/join.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/text/join.py)

## Module contents

This module defines the following functions:

smallparts.text.join.**by_blanks**(_*parts_)

> Joins the provided text parts using blanks

smallparts.text.join.**directly**(_*parts_)

> Joins the provided text parts directly adjacent

smallparts.text.join.**by_blanks**(_*parts_)

> Joins the provided text parts using newline characters (```\n```)

smallparts.text.join.**by_blanks**(_*parts_)

> Joins the provided text parts using CRLF (```\r\n```)

smallparts.text.join.**using**(*join_string,* _*parts_)

> Joins the provided text parts using *join_string*

## Usage examples

```python
>>> from smallparts.text import join
>>> join.by_blanks('parts', 'of', 'a', 'sentence')
'parts of a sentence'
>>> join.directly('Words', 'For', 'Camel', 'Case')
'WordsForCamelCase'
>>> join.by_newlines('first,', 'second and', 'third line')
'first,\nsecond and\nthird line'
>>> join.by_crlf('first,', 'second and', 'third DOS file line')
'first,\r\nsecond and\r\nthird DOS file line'
>>> join.using('<->', 'one', 'two', 'four')
'one<->two<->four'
>>> 
```

