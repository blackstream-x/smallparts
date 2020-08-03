# smallparts.text.transcode

> Universal text decoding and encoding functions,
> with additional functions to read and write text files.  
> Source: [smallparts/text/transcode.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/text/transcode.py)

## Module contents

### Constants

This module defines the following constants:

smallparts.text.transcode.**BOM_ASSIGNMENTS**

> A dict mapping byte order marks (and the unnecessary, but often encountered
> UTF-8 signature) to the matching codecs.

smallparts.text.transcode.**DEFAULT_TARGET_ENCODING**

> ```'utf-8'``` as defined in [smallparts.constants](smallparts.constants.md).**UTF_8**

smallparts.text.transcode.**DEFAULT_FALLBACK_ENCODING**

> ```'cp1252'``` as defined in [smallparts.constants](smallparts.constants.md).**CP1252**

smallparts.text.transcode.**DEFAULT_LINE_ENDING**

> ```'\n'``` as defined in [smallparts.constants](smallparts.constants.md).**LF**

### Functions

This module defines the following functions:

smallparts.text.transcode.**to_unicode_and_encoding_name**(*input_object, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Tries to decode the input object to a unicode string.
> Returns a tuple containing the conversion result and the source encoding name
> when successful. Raises a UnicodeDecodeError if appropriate.  
> *input_object* must be a **bytes** or **bytearray** instance, otherwise
> a TypeError is raised.  
> If *from_encoding* is provided, the function explicitly uses that encoding.
> Otherwise, it tries a simple form of encoding auto-detection by first trying
> all known byte order marks, then UTF-8, and *fallback_encoding* as last resort.  
> All other functions in this module using these two keyword arguments
> wrap this function directly or indirectly,
> so these arguments have the same effect everywhere.

smallparts.text.transcode.**to_unicode**(*input_object, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Wrapper for the **to_unicode_and_encoding_name()** function returning only
> the conversion result.

smallparts.text.transcode.**anything_to_unicode**(*input_object, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Safe wrapper around the **to_unicode()** function catching the TypeError
> raised if *input_object* is neither a **bytes** nor a **bytearray** instance,
> and simply returning the string conversion of the input object.

smallparts.text.transcode.**to_bytes**(*input_object, to_encoding=**DEFAULT_TARGET_ENCODING***)

> Encode a unicode string to a bytes representation using *to_encoding*.
> Raises a TypeError if *input_object* is not **str**.  

smallparts.text.transcode.**anything_to_bytes**(*input_object, to_encoding=**DEFAULT_TARGET_ENCODING**, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Safe wrapper around the **to_bytes()** function catching the TypeError
> raised if *input_object* is not a **str** instance.  
> In that case, it applies the **anything_to_unicode()** function
> to *input_object* with the *from_encoding* and *fallback_encoding* arguments passed through.
> Then, the result of that conversion is converted using **to_bytes()**.

smallparts.text.transcode.**to_utf8**(*input_object*)

> Shortcut for the explicit **to_bytes**(*input_object, to_encoding='utf-8'*)
> call.

smallparts.text.transcode.**anything_to_utf8**(*input_object, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Wrapper around the explicit
> **anything_to_bytes**(*input_object, to_encoding='utf-8', from_encoding=from_encoding, fallback_encoding=fallback_encoding*)
> call (the *from_encoding* and *fallback_encoding* arguments are passed through).

smallparts.text.transcode.**fix_double_utf8_transformation**(*unicode_text, wrong_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Fix duplicate UTF-8 transformation, which is a frequent result of reading
> UTF-8 encoded text as Latin encoded (CP-1252, ISO-8859-1 or similar),
> resulting in character sequences like ```Ã¤Ã¶Ã¼```.  
> This function reverts the effect by re-encoding *unicode_text* using
> *wrong_encoding* and decoding it as UTF-8 again.

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

