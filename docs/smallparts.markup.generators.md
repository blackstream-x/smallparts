# smallparts.markup.generators

> XML, XHTML 1.0 and HTML 5 element generator functions and classes.  
> Source: [smallparts/markup/generators.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/markup/generators.py)

## Module contents

### Constants

This module defines the following constants:

smallparts.markup.generators.**HTML_5**

> ```'HTML 5'```

smallparts.markup.generators.**XHTML_1_0_STRICT**

> ```'XHTML 1.0 Strict'```

smallparts.markup.generators.**XHTML_1_0_TRANSITIONAL**

> ```'XHTML 1.0 Transitional'```

smallparts.markup.generators.**XML**

> ```'XML'```

smallparts.markup.generators.**SUPPORTED_DIALECTS**

> A dict mapping each supported dialect (one of the above constants)
> to a **[namespaces.Namespace()](./smallparts.namespaces.md#class-smallpartsnamespacesnamespace)**
> with the following attributes suitable for the dialect:  
> **.doctype** (the DOCTYPE declaration, HTML dialects only)  
> **.factory** (the matching  …Element class from [smallparts.markup.elements](./smallparts.markup.elements.md#classes))  
> **.xmlns** (HTML dialects only, set to None for HTML 5)

### Functions

smallparts.markup.generators.**css_property**(*property_name, property_value*)

> Return a single CSS property (property_name: property_value;)

smallparts.markup.generators.**css_important_property**(*property_name, property_value*)

> Return a single CSS important property (property\_name: property\_value !important;)

smallparts.markup.generators.**html_document**(*dialect=**HTML_5**, lang='en', title='Untitled page', head='', body=''*)

> Return an HTML document in one of the supported HTML dialects from
> **SUPPORTED_DIALECTS**.
> Fill in head and body content if provided.

smallparts.markup.generators.**js_function**(*function_name, arguments*)

> Return a JavaScript function call like
> ```function_name(arg1, arg2, …, argN)```
> where *arg1, args2, …, argN* are the items in the arguments sequence.

smallparts.markup.generators.**js_return**(*function_name,* _*arguments_)

> Return the content for an HTML onclick (or similar) attribute
> calling a JavaScript function. The result looks like
> ```return function_name(arg1, arg2, …, argN);```
> where *arg1, args2, …, argN* are the items given as positional arguments.

smallparts.markup.generators.**wrap_cdata**(*character_data*)

> Wrap *character_data* in a CDATA section.
> If necessary use multiple CDATA sections as suggested in
> <https://en.wikipedia.org/wiki/CDATA#Nesting>

smallparts.markup.generators.**xml_declaration**(*version='1.0', encoding='utf-8', standalone=None*)

> Returns an XML declaration with version and encoding as provided.
> With defaults, this function returns ```<?xml version="1.0" encoding="utf-8" ?>```  
> Adds ```standalone="yes"``` if *standalone* is defined als **True**, and
> ```standalone="no"``` if *standalone* is defined as **False** explicitly.

smallparts.markup.generators.**xml_document**(*content, version='1.0', encoding='utf-8', standalone=None*)

> Returns an XML document with an XML declaration made from the
> *version*, *encoding* and *standalone* provided, adding *content*
> after a line break.  
> ***Please note*** that *content* is not checked in any way,
> so you have to take care yourself to provide well-formed XML as content only.


### Classes

#### *class* smallparts.markup.generators.**ElementsCache**(*dialect*)

Provides an element generators cache.

Instances of this class store the element factory defined in **SUPPORTED_DIALECTS**
for *dialect*. When any attribute other than **._dialect** (the dialect)
or **._factory** (the element factory) is referenced, the instance returns
an instance of the element factory with the attribute name (translated via
**._factory.translate_name()**) as the tag name. These instances are cached
*in the class* per dialect (implementing a partial [Borg pattern](http://www.aleax.it/Python/5ep.html)).

## Usage examples

```python
>>> from smallparts.markup import generators
>>> XML = generators.ElementsCache(generators.XML)
>>> XML._dialect
'XML'
>>> XML._factory
<class 'smallparts.markup.elements.XmlElement'>
>>> XML.outer_element(XML.inner_element('Text content'))
'<outer-element><inner-element>Text content</inner-element></outer-element>'
>>> generators.ElementsCache._cached_elements
{'HTML 5': {}, 'XHTML 1.0 Strict': {}, 'XHTML 1.0 Transitional': {}, 'XML': {'outer-element': <smallparts.markup.elements.XmlElement object at 0x7fc0db9301c0>, 'inner-element': <smallparts.markup.elements.XmlElement object at 0x7fc0db930130>}}
>>> 
>>> generators.xml_document(XML.minimalistic_example())
'<?xml version="1.0" encoding="utf-8" ?>\n<minimalistic-example/>'
>>> 
>>> XHTML_STRICT = generators.ElementsCache(generators.XHTML_1_0_STRICT)
>>> XHTML_STRICT.p__('Text content', __class__='notice')
'<p class="notice">Text content</p>'
>>> # unsupported <center> in XHTML 1.0 Strict:
>>> XHTML_STRICT.center(XHTML_STRICT.strong('Centered content'))
Traceback (most recent call last):
  File "………/smallparts/markup/generators.py", line 93, in __getattribute__
    return type(self)._cached_elements[self._dialect][name]
KeyError: 'center'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "………/smallparts/markup/generators.py", line 97, in __getattribute__
    self._factory(name))
  File "………/smallparts/markup/elements.py", line 316, in __init__
    super(XmlBasedHtmlElement, self).__init__(tag_name)
  File "………/smallparts/markup/elements.py", line 229, in __init__
    raise ValueError('Unsupported element name {0!r}'.format(
ValueError: Unsupported element name 'center'
>>> 
>>> # <center> is supported in XHTML 1.0 Transitional:
>>> XHTML_TRAN = generators.ElementsCache(generators.XHTML_1_0_TRANSITIONAL)
>>> XHTML_TRAN.center(XHTML_TRAN.strong('Centered content'))
'<center><strong>Centered content</strong></center>'
>>> 
>>> print(generators.html_document())
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Untitled page</title>
</head>
<body></body>
</html>
>>> 
>>> # Now, there are some more cached elements in the class:
>>> generators.ElementsCache._cached_elements
{'HTML 5': {'meta': <smallparts.markup.elements.HtmlElement object at 0x7fc0db293be0>, 'title': <smallparts.markup.elements.HtmlElement object at 0x7fc0db293ca0>, 'html': <smallparts.markup.elements.HtmlElement object at 0x7fc0db293d00>, 'head': <smallparts.markup.elements.HtmlElement object at 0x7fc0db293d60>, 'body': <smallparts.markup.elements.HtmlElement object at 0x7fc0db293d90>}, 'XHTML 1.0 Strict': {'p': <smallparts.markup.elements.XhtmlStrictElement object at 0x7fc0dba3d490>}, 'XHTML 1.0 Transitional': {'center': <smallparts.markup.elements.XhtmlTransitionalElement object at 0x7fc0db293b20>, 'strong': <smallparts.markup.elements.XhtmlTransitionalElement object at 0x7fc0db293ac0>}, 'XML': {'outer-element': <smallparts.markup.elements.XmlElement object at 0x7fc0db9301c0>, 'inner-element': <smallparts.markup.elements.XmlElement object at 0x7fc0db930130>, 'minimalistic-example': <smallparts.markup.elements.XmlElement object at 0x7fc0dbb4fc40>}}
>>> 
```

----
[(smallparts docs home)](./)

