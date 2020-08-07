# smallparts.markup.parsers

> HTML and XML parsers and entity resolvers.  
> Source: [smallparts/markup/parsers.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/markup/parsers.py)

## Module contents

### Classes

#### *class* smallparts.markup.parsers.**EntityResolver**(*named_entities=None*)

Instances of this class can be used to resolve named entities as well as
numeric character references.

***Please Note:*** This class is intended for use with XML to enable resolving
user-defined entity references. Although it is possible to use it for resolving
HTML entity references by instantiating it like  
**EntityResolver**(*named_entities=html.entities.name2codepoint*)  
it might be a better idea to use the standard library function
[html.unescape()](https://docs.python.org/3/library/html.html#html.unescape)
directly.

##### Parameter:

*   *named_entities* can be provided as a dict mapping entity names to their
    replacements. The replacements must be either valid Unicode codepoints
    as integers (i.e. 0–1114111), or strings.  
    If this parameter is not provided (or set to None), the instance
    uses the named entities known to XML (amp, apos, gt, lt and quot).

##### Methods:

*static method*  
**.resolve_charref**(*charref*)

Resolves the provided decimal or hexadecimal character reference
(i.e. the part of a numeric entity notation between ```&#``` and ```;```)
to the matching unicode character.
Raises a ValueError for invalid references.

**.resolve_named_entity**(*name*)

Resolves the provided symbolic reference
(i.e. the part of an entity notation between ```&``` and ```;```)
to the matching replacement.
Raises a ValueError for unknown names.

**.resolve_any_entity**(*entityref*)

Resolves the provided reference
(i.e. the part of an entity notation between ```&``` and ```;```)
by dispatching to **.resolve_charref** if it is numeric (i.e. starts with ```#```)
or to **.resolve_named_entity** otherwise.

**.resolve_all_entities**(*source_text*)

Returns *source_text* wth all valid character references and all known
symbolic entity references resolved. Invalid or unknown entities are left
as they were.

#### *class* smallparts.markup.parsers.**HtmlTagStripper**(*image_placeholders='with alt text only', body_reqired=True*)

Instances of this class can be used to strip all markup from an HTML document
while trying to keep line breaks (but squeezing multiple ones together,
as well as other whitespace).
When parsing a document, the text contents are stored, and a list of images
with all attributes is kept separately.

##### Parameters:

* *image_placeholders* is used for distinguishing between three ways of
  treating inline images:
  1. When left at the default value ```'with alt text only'```,
     a placeholder '\[image: \<text from the alt attribute\>\]'
     is placed into the resulting text only for images having an *alt* attribute.
  2. When set to ```True```, images havin an *alt* attribute are treated as above,
     and a placeholder \[image\] is placed into the resulting text for each
     image lacking the *alt* attribute.
  3. When set to ```False``` or ```None```, no placeholders for images are put
     into the resulting text at all.

_(tbc)_


## Usage examples

```python
>>> from smallparts.markup import parsers
>>> 
```

----

[(smallparts docs home)](./)

