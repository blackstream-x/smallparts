# smallparts.markup.generators

> XML, XHTML 1.0 and HTML 5 element generator functions and classes.  
> Source: [smallparts/markup/generators.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/markup/generators.py)

## Module contents

### Constants

This module defines the following constants:

smallparts.markup.generators.**HTML_5**

> ```HTML 5```

smallparts.markup.generators.**XHTML_1_0_STRICT**

> ```XHTML 1.0 Strict```

smallparts.markup.generators.**XHTML_1_0_TRANSITIONAL**

> ```XHTML 1.0 Transitional```

smallparts.markup.generators.**SUPPORTED_HTML_DIALECTS**

> A dict mapping each supported HTML dialect (one of the above constants)
> to a **[namespaces.Namespace()](./smallparts.namespaces.md#class-smallpartsnamespacesnamespace)**
> with the following attributes suitable for the dialect:  
> **.doctype** (the DOCTYPE declaration)  
> **.factory** (the generator class from this module)  
> **.xmlns** (for the XHTML dialects only: ```http://www.w3.org/1999/xhtml```)

### Functions

smallparts.markup.generators.**css_property**(*property_name, property_value*)

> Return a single CSS property (property_name: property_value;)

smallparts.markup.generators.**css_important_property**(*property_name, property_value*)

> Return a single CSS important property (property\_name: property\_value !important;)

smallparts.markup.generators.**html_document**(_dialect=_**HTML_5**_, lang='en', title='Untitled page', head='', body=''_)

> Return an HTML document in the selected dialect as defined in **SUPPORTED_HTML_DIALECTS**.
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
> ```standalone="no"``` if *standalone* is defined as **False explicitly**.

smallparts.markup.generators.**xml_document**(*content, version='1.0', encoding='utf-8', standalone=None*)

> Returns an XML document with an XML declaration made from the
> *version*, *encoding* and *standalone* provided, adding *content*
> after a line break.  
> ***Please note*** that *content* is not checked in any way,
> so you have to take care yourself to provide well-formed XML as content only.


### Classes

#### *class* smallparts.markup.generators.**XmlGenerator**()

Instances of this class keep an internal dict of
**[smallparts.markup.elements.XmlElement()](./smallparts.markup.elements.md#class-smallpartsmarkupelementsxmlelementtag_name)**
class instances that are instantiated when an attribute with a matching name
is referenced for the first time. That way, you can generate elements using the
instance with new or existing attributes.

#### *class* smallparts.markup.generators.**XhtmlStrictGenerator**()

same as above, but with
**[smallparts.markup.elements.XhtmlStrictElement()](./smallparts.markup.elements.md#class-smallpartsmarkupelementsxhtmlstrictelementtag_name)**
instances for XHTML 1.0 Strict semantics.

#### *class* smallparts.markup.generators.**XhtmlTransitionalGenerator**()

same as above, but with
**[smallparts.markup.elements.XhtmlTransitionalElement()](./smallparts.markup.elements.md#class-smallpartsmarkupelementsxhtmltransitionalelementtag_name)**
instances for XHTML 1.0 Transitional semantics.

#### *class* smallparts.markup.generators.**HtmlGenerator**()

same as above, but with
**[smallparts.markup.elements.HtmlElement()](./smallparts.markup.elements.md#class-smallpartsmarkupelementshtmlelementtag_name)**
instances for HTML 5 semantics.

#### *Please note:*

Elements are cached in each of the above classes, implementing something
similar to the [Borg pattern](http://www.aleax.it/Python/5ep.html).

## Usage examples

```python
>>> from smallparts.markup import generators
>>> XML = generators.XmlGenerator()
>>> XML.outer_element(XML.inner_element('Text content'))
'<outer-element><inner-element>Text content</inner-element></outer-element>'
>>> 
>>> XHTML_STRICT = generators.XhtmlStrictGenerator()
>>> XHTML_STRICT.p__('Text content', __class__='notice')
'<p class="notice">Text content</p>'
>>> XHTML_STRICT.center(XHTML_STRICT.p__('Centered content'))
Traceback (most recent call last):
  File "/………/smallparts/markup/generators.py", line 208, in __getattribute__
    return self._cached_elements_[name]
KeyError: 'center'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/………/smallparts/markup/generators.py", line 212, in __getattribute__
    type(self).element_type(name))
  File "/………/smallparts/markup/elements.py", line 316, in __init__
    super(XmlBasedHtmlElement, self).__init__(tag_name)
  File "/………/smallparts/markup/elements.py", line 229, in __init__
    raise ValueError('Unsupported element name {0!r}'.format(
ValueError: Unsupported element name 'center'
>>> 
>>> XHTML_TRANSITIONAL = generators.XhtmlTransitionalGenerator()
>>> XHTML_TRANSITIONAL.center(XHTML_TRANSITIONAL.p__('Centered content'))
'<center><p>Centered content</p></center>'
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
>>> print(generators.html_document(dialect=generators.XHTML_1_0_STRICT))
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>Untitled page</title>
</head>
<body></body>
</html>
>>> 
>>> generators.xml_document(XML.minimalistic_example())
'<?xml version="1.0" encoding="utf-8" ?>\n<minimalistic-example/>'
>>> 
```

----
[(smallparts docs home)](./)

