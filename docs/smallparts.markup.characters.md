# smallparts.markup.characters

> HTML and XML Characters handling.  
> Source: [smallparts/markup/characters.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/markup/characters.py)

## Module contents

### Constants

This module defines the following constants as keys for the **Defuser** class:

smallparts.markup.characters.**REMOVE_INVALID**

> ```0```

smallparts.markup.characters.**REMOVE_INVALID**

> ```1```

smallparts.markup.characters.**REMOVE_INVALID**

> ```2```

### Functions

smallparts.markup.characters.**encode_to_charrefs**(*source_text*)

> Returns *source_text* with all non-ascii characters replaced by XML charrefs.

smallparts.markup.characters.**entity**(*reference*)

> Returns an XML charref if *reference* is an integer,
> and a symbolic entity reference in all other cases.

smallparts.markup.characters.**charref_from_name**(*unicode_character_name*)

> Returns the XML charref matching *unicode_character_name*,

smallparts.markup.characters.**translate_to_charrefs**(*characters_sequence, source_text*):

> Returns *source_text* with all characters from *characters_sequence*
> translated to their XML charrefs.
    
### Classes

#### *class* smallparts.markup.characters.**Defuser**(*xml_version='1.0', remove=**REMOVE_INVALID***)

Instances of this dict can be used to defuse text for use as the content
of an XML element.

##### Methods:

**.defuse**(*source_text*)

Defuses *source_text*. This is done by applying the
**.remove_codepoints** method on *source_text* first, and then
the **.escape** static method. 

**.remove_codepoints**(*source_text*)

Invalid, restricted and/or discouraged codepoints are removed from *source_text*,
depending on the values of the *xml_version* and *remove* arguments at
instantiation time.  
Compare <https://www.w3.org/TR/xml/#charsets> for invalid, restricted and
discouraged codepints in XML 1.0, and <https://www.w3.org/TR/xml11/#charsets>
for the same in XML 1.1.

*static method:*  
**.escape**(*source_text*)

This static method escapes ```'&'```, ```'<'```, and ```'>'```
in *source_text* using the standard library’s
[xml.sax.saxutils.escape](https://docs.python.org/3/library/xml.sax.utils.html#xml.sax.saxutils.escape)
function.  
If you do not want to remove any codepoints from *source_text*,
you do not need to instantiate an object,
but can simply call **Defuser.escape**(*source_text*).


## Usage examples

```python
>>> from smallparts.markup import characters
>>> from smallparts.markup import characters
>>> characters.encode_to_charrefs('Ä Ö Ü € ß')
'&#196; &#214; &#220; &#8364; &#223;'
>>> characters.entity(257)
'&#257;'
>>> characters.entity('apos')
'&apos;'
>>> characters.entity('other_name')
'&other_name;'
>>> characters.charref_from_name('ANTICLOCKWISE TOP SEMICIRCLE ARROW')
'&#8630;'
>>> characters.translate_to_charrefs('aeiou', 'Lorem ipsum dolor sit amet …')
'L&#111;r&#101;m &#105;ps&#117;m d&#111;l&#111;r s&#105;t &#97;m&#101;t …'
>>> 
>>> characters.Defuser.escape('[\x00] [\x7f] [\ufdd0] < > &') 
'[\x00] [\x7f] [\ufdd0] &lt; &gt; &amp;'
>>> 
>>> defuser_i = characters.Defuser(remove=characters.REMOVE_INVALID)
>>> defuser_i.defuse('[\x00] [\x7f] [\ufdd0] < > &')
'[] [\x7f] [\ufdd0] &lt; &gt; &amp;'
>>> defuser_r = characters.Defuser(remove=characters.REMOVE_RESTRICTED)
>>> defuser_r.defuse('[\x00] [\x7f] [\ufdd0] < > &')
'[] [] [\ufdd0] &lt; &gt; &amp;'
>>> defuser_d = characters.Defuser(remove=characters.REMOVE_DISCOURAGED)
>>> defuser_d.defuse('[\x00] [\x7f] [\ufdd0] < > &')
'[] [] [] &lt; &gt; &amp;'
>>> 
>>> 
```

----
[(smallparts docs home)](./)

