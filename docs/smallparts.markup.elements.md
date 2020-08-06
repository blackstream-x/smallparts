# smallparts.markup.elements

> XML, XHTML 1.0 and HTML 5 element definitions.  
> Source: [smallparts/markup/elements.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/markup/elements.py)

## Module contents

### Constants

This module defines the following constants:

smallparts.markup.elements.**LABEL_HTML_5**

> ```'HTML 5'```

smallparts.markup.elements.**LABEL_XHTML_1_0_STRICT**

> ```'XHTML 1.0 Strict'```

smallparts.markup.elements.**LABEL_XHTML_1_0_TRANSITIONAL**

> ```'XHTML 1.0 Transitional'```

smallparts.markup.elements.**LABEL_XML**

> ```'XML'```

smallparts.markup.elements.**XHTML_1_0_STRICT**

> [Set](https://docs.python.org/3/library/stdtypes.html#set)
> of XHTML 1.0 Strict element names

smallparts.markup.elements.**XHTML_1_0_TRANSITIONAL**

> Set of XHTML 1.0 Transitional element names

smallparts.markup.elements.**HTML_5**

> Set of HTML 5 element names

smallparts.markup.elements.**XHTML_1_0_EMPTY_ELEMENTS**

> Set of XHTML 1.0 empty element names

smallparts.markup.elements.**HTML_5_EMPTY_ELEMENTS**

> Set of HTML 5 empty element names

### Classes

#### *class* smallparts.markup.elements.**XmlElement**(*tag_name*)

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
    like ```'<empty/>'```.


#### *class* smallparts.markup.elements.**XmlBasedHtmlElement**(*tag_name*)

Subclass of **XmlElement** with the following differences:
*   tag names and attribute names are _additionally_ transformed to lowercase.
*   empty elements are generated with a blank before the slash (e.g. ```'<br />'```).
*   Elements are only treated as empty if they are defined as empty in
    **XHTML_1_0_EMPTY_ELEMENTS**, so **XmlBasedHtmlElement**('p')()
    generates ```'<p></p>'``` instead of ```'<p />'```.
*   If an element is defined as empty, it will always be displayed as empty,
    regardless of provided content.
*   There are two special attributes: **__class__** and **__classes__**.
    **__class__** may provide one HTML class,
    and **__classes__** may provide a sequence of HTML classes.
    If any of these is provided, **__class__** and **__classes__** are combined
    into one string using blanks as separators, and the combined value
    is rendered as the value of the HTML **class** attribute.

#### *class* smallparts.markup.elements.**HtmlElement**(*tag_name*)

Subclass of **XmlBasedHtmlElement** for *HTML 5* generation.
Differences from the parent class:
*   empty elements are generated without a slash (e.g. ```'<br>'```).
*   Tag names are restricted to the ones listed in **HTML_5**.
    All other tag names produce a ValueError.
*   Elements are only treated as empty if they are defined as empty in
    **HTML_5_EMPTY_ELEMENTS**, so **HtmlElement**('iframe')()
    generates ```'<iframe></iframe>'``` instead of ```'<iframe>'```.
*   If an attribute was provided with value **True**,
    only put its attribute name into the start tag.

#### *class* smallparts.markup.elements.**XhtmlStrictElement**(*tag_name*)

Subclass of **XmlBasedHtmlElement** for *XHTML 1.0 Strict* generation.
Differences from the parent class:
*   Tag names are restricted to the ones listed in **XHTML_1_0_STRICT**.
    All other tag names produce a ValueError.
*   The **lang** attribute is duplicated as **xml:lang** with the same value
    (required by the specification).

#### *class* smallparts.markup.elements.**XhtmlTransitionalElement**(*tag_name*)

Subclass of **XhtmlStrictElement** for *XHTML 1.0 Transitional* generation.
Differences from the parent class:
*   Tag names are restricted to the ones listed in **XHTML_1_0_TRANSITIONAL**.
    All other tag names produce a ValueError.

#### *class* smallparts.markup.elements.**Cache**(*dialect*)

Provides an element factories cache.

Instances of this class store the given *dialect* (which may be one of
this module’s __LABEL_*__ constants) in the **._dialect** attribute.  
They can be used to generate XML or HTML elements
by calling the matching **\*Element()** instance for the dialect.
The **\*Element()** instances are generated *on the fly* using the attribute name,
and cached in the *class attribute **.cached_elements***.
You can call **dir()** on the instance to get a list of cached elements
for the instance dialect only.

See the following examples:

```python
>>> xml_gen = elements.Cache(elements.LABEL_XML)
>>> xml_gen.example_element()
'<example-element/>'
>>> html_gen = elements.Cache(elements.LABEL_HTML_5)
>>> html_gen.p__('paragraph with an ', html_gen.strong('emphasized part'))
'<p>paragraph with an <strong>emphasized part</strong></p>'
>>> 
>>> elements.Cache.cached_elements
{'HTML 5': {'p': <smallparts.markup.elements.HtmlElement object at 0x7f358459bc40>, 'strong': <smallparts.markup.elements.HtmlElement object at 0x7f358431c9d0>}, 'XHTML 1.0 Strict': {}, 'XHTML 1.0 Transitional': {}, 'XML': {'example-element': <smallparts.markup.elements.XmlElement object at 0x7f358437d0a0>}}
>>> dir(xml_gen)
['example-element']
>>> dir(html_gen)
['p', 'strong']
>>>
```

#### *Please note:*
*   Namespaces are not supported
*   Attributes are not checked for validity

## Usage examples

```python
>>> from smallparts.markup import elements
>>> 
>>> # XML example: Note the different treatment of attributes
>>> # depending on their value (None, scalar value or True)
>>> xml_example = elements.XmlElement('tag_name')
>>> xml_example()
'<tag-name/>'
>>> xml_example('content', attribute_1=None, attribute_2='value', attribute_3=True)
'<tag-name attribute-2="value" attribute-3="attribute-3">content</tag-name>'
>>> 
>>> # invalid HTML example: tag name not in the set of allowed element names
>>> html_example = elements.HtmlElement('tag_name')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "………/smallparts/markup/elements.py", line 321, in __init__
    super(XmlBasedHtmlElement, self).__init__(tag_name)
  File "………/smallparts/markup/elements.py", line 234, in __init__
    raise ValueError('Unsupported element name {0!r}'.format(
ValueError: Unsupported element name 'tag-name'
>>> 
>>> # valid HTML example: Note the treatment of the special attributes
>>> # __class__ (for a single class) and __classes__ (for a sequence of classes).
>>> html_div = elements.HtmlElement('div')
>>> html_div('content', __class__='blue')
'<div class="blue">content</div>'
>>> html_div('content', __classes__=('with-border', 'bold'), id_='annotation')
'<div id="annotation" class="bold with-border">content</div>'
>>> 
>>> # empty elements ignore the provided content
>>> html_br = elements.HtmlElement('br')
>>> html_br()
'<br>'
>>> html_br('content')
'<br>'
>>> 
>>> # empty attributes in HTML 5:
>>> html_option = elements.HtmlElement('option')
>>> html_option('display value', value='submit_value', selected=True)
'<option value="submit_value" selected>display value</option>'
>>> 
>>> # lang= duplicated as xml:lang= in XHTML:
>>> xhtml_p = elements.XhtmlStrictElement('p')
>>> xhtml_p('text in paragraph', lang='en')
'<p lang="en" xml:lang="en">text in paragraph</p>'
>>> xhtml_p()
'<p></p>'
>>> 
>>> # Cache examples
>>> XHTML = elements.Cache(elements.LABEL_XHTML_1_0_STRICT)
>>> XHTML.fieldset(XHTML.legend('Task details', lang='en'), '\n', XHTML.label('Please select the due date: ', XHTML.input(type='date', name='due_date')))
'<fieldset><legend lang="en" xml:lang="en">Task details</legend>\n<label>Please select the due date: <input type="date" name="due_date" /></label></fieldset>'
>>> dir(XHTML)
['fieldset', 'input', 'label', 'legend']
>>> 
```

----

[(smallparts docs home)](./)

