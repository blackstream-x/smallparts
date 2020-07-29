[(smallparts docs home)](./) > [(smallparts.markup)](./smallparts.markup.md) >
----
# smallparts.markup.elements

> XML, XHTML 1.0 and HTML 5 element definitions.  
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
    Trailing underscores are removed,
    and all other underscores are replaced by dashes.
 
Instances are called like this:  
generated_markup = _**Instance**_(_*_*content_fragments*, _**_*attributes*)  
and return the element with the provided attributes, enclosing
the content fragments.
*   Attribute names are treated the same way as the tag names:
    trailing underscores are removed, and all other underscore are replaced by
    dashes.
*   If an attribute was provided with value **None** or **False**,
    the attribute is omitted.
*   If an attribute was provided with value **True**,
    set its value to the attribute name.
*   If no or empty content was provided, generate an empty element
    like ```<empty/>```.


*class* smallparts.markup.elements.**XmlBasedHtmlElement**(*tag_name*)

Subclass of **XmlElement** with the following differences:
*   tag names and attribute names are transformed to lowercase
*   empty elements are generated with a blank before the slash (e.g. ```<br />```).
*   Elements are only treated as empty if they are defined as empty in
    **XHTML_1_0_EMPTY_ELEMENTS**, so **XmlBasedHtmlElement**('p')()
    generates ```<p></p>``` instead of ```<p />```.
*   If an element is defined as empty, it will always be displayed as empty,
    regardless of provided content.
*   There are two special attributes: **__class__** and **__classes__**.
    **__class__** may provide one HTML class,
    and **__classes__** may provide a sequence of HTML classes.
    If any of these is provided, **__class__** and **__classes__** are combined
    into one string using blanks as separators, and the combined value
    is rendered as the value of the HTML **class** attribute.

*class* smallparts.markup.elements.**HtmlElement**(*tag_name*)

Subclass of **XmlBasedHtmlElement** for *HTML 5* generation.
Differences from the parent class:
*   empty elements are generated without a slash (e.g. ```<br>```).
*   Tag names are restricted to the ones listed in **HTML_5**.
    All other tag names produce a ValueError.
*   Elements are only treated as empty if they are defined as empty in
    **HTML_5_EMPTY_ELEMENTS**, so **HtmlElement**('iframe')()
    generates ```<iframe></iframe>``` instead of ```<iframe>```.
*   If an attribute was provided with value **True**,
    only put its attribute name into the start tag.

*class* smallparts.markup.elements.**XhtmlStrictElement**(*tag_name*)

Subclass of **XmlBasedHtmlElement** for *XHTML 1.0 Strict* generation.
Differences from the parent class:
*   Tag names are restricted to the ones listed in **XHTML_1_0_STRICT**.
    All other tag names produce a ValueError.
*   The **lang** attribute is duplicated as **xml:lang** with the same value
    (required by the specification).

*class* smallparts.markup.elements.**XhtmlTransitionalElement**(*tag_name*)

Subclass of **XhtmlStrictElement** for *XHTML 1.0 Transitional* generation.
Differences from the parent class:
*   Tag names are restricted to the ones listed in **XHTML_1_0_TRANSITIONAL**.
    All other tag names produce a ValueError.

***Please note:***
*   Namespaces are not supported
*   Attributes are not checked for validity

## Usage examples

```python
>>> from smallparts.markup import elements
>>> xml_example = elements.XmlElement('tag_name')
>>> xml_example()
'<tag-name/>'
>>> xml_example('content', attribute_1=None, attribute_2='value', attribute_3=True)
'<tag-name attribute-2="value" attribute-3="attribute-3">content</tag-name>'
>>> 
>>> html_example = elements.HtmlElement('tag_name')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/………/smallparts/markup/elements.py", line 316, in __init__
    super(XmlBasedHtmlElement, self).__init__(tag_name)
  File "/………/smallparts/markup/elements.py", line 229, in __init__
    raise ValueError('Unsupported element name {0!r}'.format(
ValueError: Unsupported element name 'tag-name'
>>> html_example = elements.HtmlElement('div')
>>> html_example('content', __class__='blue')
'<div class="blue">content</div>'
>>> html_example('content', __classes__=('with-border', 'bold'), id_='annotation')
'<div id="annotation" class="bold with-border">content</div>'
>>> 
>>> html_br = elements.HtmlElement('br')
>>> html_br()
'<br>'
>>> html_br('content')
'<br>'
>>> 
>>> html_option = elements.HtmlElement('option')
>>> html_option('display value', value='submit_value', selected=True)
'<option value="submit_value" selected>display value</option>'
>>> 
>>> xhtml_example = elements.XhtmlStrictElement('p')
>>> xhtml_example('text in paragraph', lang='en')
'<p lang="en" xml:lang="en">text in paragraph</p>'
>>> xhtml_example()
'<p></p>'
>>> 
```

