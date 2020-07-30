# smallparts.text.transcode

> Universal text decoding and encoding functions,
> with additional functions to read and write text files.  
> Source: [smallparts/text/transcode.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/text/transcode.py)

## Module contents

This module defines the following functions:

smallparts.text.transcode.**to_unicode_and_encoding_name**(*input_object, from_encoding=None, fallback_encoding='cp1252'*)

> Tries to decode the input object to a unicode string.
> Returns a tuple containing the conversion result and the source encoding name
> when successful. Raises a UnicodeDecodeError if appropriate.  
> *input_object* must be a **bytes** or **bytearray** instance, otherwise
> a TypeError is raised.  
> If *from_encoding* is provided, the function explicitly uses that encoding.
> Otherwise, it tries a simple form of encoding auto-detection by first trying
> all known byte order marks, then UTF-8, and *fallback_encoding* as last resort.

smallparts.text.transcode.**to_unicode**(*input_object, from_encoding=None, fallback_encoding='cp1252'*)

> Wrapper for the **to_unicode_and_encoding_name()** function returning only
> the conversion result.

smallparts.text.transcode.**anything_to_unicode**(*input_object, from_encoding=None, fallback_encoding='cp1252'*)

> Safe wrapper around the **to_unicode()** function catching the TypeError
> raised if *input_object* is neither a **bytes** nor a **bytearray** instance,
> and simply returning the string conversion of the input object.

smallparts.text.transcode.**to_bytes**(*input_object, to_encoding='utf-8'*)

> Encode a unicode string to a bytes representation using the provided encoding.
> Raises a TypeError if *input_object* is not **str**.

smallparts.text.transcode.**anything_to_bytes**(*input_object, to_encoding='utf-8', from_encoding=None, fallback_encoding='cp1252'*)

> Safe wrapper around the **to_bytes()** function catching the TypeError
> raised if *input_object* is not a **str** instance.  
> In that case, it applies the **anything_to_unicode()** function
> to *input_object* with the *from_encoding* and *fallback_encoding* arguments.
> Then, the result of that conversion is converted using **to_bytes()**.

smallparts.text.transcode.**to_utf8**(*input_object*)

> Shortcut for the explicit **to_bytes**(*input_object, to_encoding='utf-8'*)
> call.

smallparts.text.transcode.**anything_to_utf8**(*input_object, from_encoding=None, fallback_encoding='cp1252'*)

> Shortcut for the explicit
> **anything_to_bytes**(*input_object, from_encoding=None, fallback_encoding='cp1252'*)
> call.

smallparts.text.transcode.**fix_double_utf8_transformation**(*unicode_text*, *wrong_encoding='cp1252'*)

> Fix duplicate UTF-8 transformation, which is a frequent result of reading
> UTF-8 encoded text as Latin encoded (CP-1252, ISO-8859-1 or similar),
> resulting in character sequences like ```Ã¤Ã¶Ã¼```.  
> This function reverts the effect.

*(tbc)*

## Usage examples

```python
>>> from smallparts.text import transcode
>>> transcode.fix_double_utf8_transformation('Ã¤Ã¶Ã¼')
'äöü'
>>> 
```

----
[(smallparts docs home)](./)
----

