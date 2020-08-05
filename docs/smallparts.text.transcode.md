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

smallparts.text.transcode.**SUPPORTED_OUTPUT_LINE_ENDINGS**

> A tuple containing ```'\n'``` and ```'\r\n'``` (as defined in
> [smallparts.constants](smallparts.constants.md).**LF** and
> [smallparts.constants](smallparts.constants.md).**CRLF**)

### Functions

This module defines the following functions:

smallparts.text.transcode.**to_unicode_and_encoding_name**(*bytestring, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Tries to decode *bytestring* to a unicode string.
> Returns a tuple containing the conversion result and the source encoding name
> when successful. Raises a UnicodeDecodeError if appropriate.  
> If *bytestring* is neither a **bytes** nor a **bytearray** instance,
> a TypeError is raised.  
> If *from_encoding* is provided, the function explicitly uses that encoding.
> Otherwise, it tries a simple form of encoding auto-detection by first trying
> all known byte order marks, then UTF-8, and *fallback_encoding* as the last resort.  
> All other functions in this module using these two keyword arguments
> wrap this function directly or indirectly,
> so these arguments have the same effect everywhere.

smallparts.text.transcode.**to_unicode**(*bytestring, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Wrapper for the **to_unicode_and_encoding_name()** function returning only
> the conversion result.

smallparts.text.transcode.**anything_to_unicode**(*input_object, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Safe wrapper around the **to_unicode()** function catching the TypeError
> raised if *input_object* is neither a **bytes** nor a **bytearray** instance,
> and simply returning the string conversion of the input object.

smallparts.text.transcode.**to_bytes**(*unicode_text, to_encoding=**DEFAULT_TARGET_ENCODING***)

> Encode *unicode_text* to a bytes representation using *to_encoding*.
> Raises a TypeError if *unicode_text* is not **str**.  

smallparts.text.transcode.**anything_to_bytes**(*input_object, to_encoding=**DEFAULT_TARGET_ENCODING**, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Safe wrapper around the **to_bytes()** function catching the TypeError
> raised if *input_object* is not a **str** instance.  
> In that case, it applies the **anything_to_unicode()** function
> to *input_object* with the *from_encoding* and *fallback_encoding* arguments passed through.
> Then, the result of that conversion is converted using **to_bytes()**.

smallparts.text.transcode.**to_utf8**(*unicode_text*)

> Shortcut for the explicit **to_bytes**(*unicode_text, to_encoding='utf-8'*)
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

smallparts.text.transcode.**read_from_file**(*input_file_or_name, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING***)

> Read *input_file_or_name* contents and return its contents decoded to unicode.
> As the argument name suggests, *input_file_or_name* may be either a file name
> or a file object.

smallparts.text.transcode.**prepare_file_output**(*unicode_content, to_encoding=**DEFAULT_TARGET_ENCODING**, line_ending=**DEFAULT_LINE_ENDING***)

> Return *unicode_content* prepared for binary output to a file
> (i.e. as bytes, encoded as *to_encoding* and with *line_ending* as line ending).  
> Raises a ValueError if *line_ending* is not one of **SUPPORTED_OUTPUT_LINE_ENDINGS**,
> or a TypeError if *unicode_content* is neither a unicode string
> nor a sequence of unicode strings.

smallparts.text.transcode.**transcode_file**(*file_name, to_encoding=**DEFAULT_TARGET_ENCODING**, from_encoding=None, fallback_encoding=**DEFAULT_FALLBACK_ENCODING**, line_ending=None*)

> Transcodes the file with the name *file_name* to *to_encoding*.  
> Raises a ValueError if the file contents are already encoded in *to_encoding*.  
> If *line_ending* is one of **SUPPORTED_OUTPUT_LINE_ENDINGS**,
> changes the line endings in the file contnts to *line_ending*.  
> Renames the original file to a file with the detected encoding appended to
> the original file name, but before the extension.


## Usage examples

```python
>>> from smallparts.text import transcode
>>> transcode.fix_double_utf8_transformation('Ã¤Ã¶Ã¼')
'äöü'
>>> 
```

----
[(smallparts docs home)](./)

