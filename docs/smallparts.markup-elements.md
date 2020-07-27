# smallparts.markup.elements

> XML, XHTML 1.0 and HTML 5 element generation
> Source: [smallparts/markup/elements.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/markup/elements.py)

## Module contents

### Constants

This module defines the following sets:

smallparts.markup.elements.**XHTML_1_0_STRICT**

> XHTML 1.0 Strict element names

smallparts.markup.elements.**XHTML_1_0_TRANSITIONAL**

> XHTML 1.0 Transitional element names

smallparts.markup.elements.**HTML_5**

> HTML 5 element names

smallparts.markup.elements.**XHTML_1_0_EMPTY_ELEMENTS**

> Names of XHTML 1.0 empty elements

smallparts.markup.elements.**HTML_5_EMPTY_ELEMENTS**

> Names of HTML 5 empty elements

### Classes

*class* smallparts.markup.elements.**XmlElement**(*tag_name*)

Instances of this class act as a function generating an XML element
with content and attributes provided when calling the instance.

*Parameter:*
*   *tag_name* is the tag name of the XML element.
 
Instances are called like this:  
_**Instance**_(_*_*content_fragments*, _**_*attributes*)  
and return the element with the provided attributes, enclosing
the content fragments _(tbc)_

## Usage examples

```python
>>> from smallparts.markup import elements
>>> 
```

