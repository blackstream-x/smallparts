# smallparts.markup.generators

> XML, XHTML 1.0 and HTML 5 element generation
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

> A dict of supported HTML dialects (the above constants)
> and a namespaces.Namespace() with the following attributes
> suitable for the dialect:  
> **.doctype** (the DOCTYPE declaration)  
> **.factory** (the generator class from this module)  
> **.xmlns** (for the XHTML dialects only: ```http://www.w3.org/1999/xhtml```)

### Functions

smallparts.markup.generators.**css_property**(*property_name, property_value*)

> Return a single CSS property (property_name: property_value;)

smallparts.markup.generators.**css_important_property**(*property_name, property_value*)

> Return a single CSS important property (property\_name: property\_value !important;)

smallparts.markup.generators.**html_document**(*dialect='HTML_5', lang='en', title='Untitled page', head='', body=''*)

> Return an HTML document in the selected dialect as defined in **SUPPORTED_HTML_DIALECTS**.
> Fill in head and body content if provided.

_(tbc)_

### Classes

*class* smallparts.markup.generators.**XmlGenerator**()

Instances of this class keep an internal dict of
**[smallparts.markup.elements](./smallparts.markup.elements.md).XmlElement()**
class instances that are instantiated when an attribute with a matching name
is referenced for the first time. That way, you can generate elements using the
instance with new or existing attributes.

*class* smallparts.markup.generators.**XhtmlStrictGenerator**()

same as above, but with
**[smallparts.markup.elements](./smallparts.markup.elements.md).XhtmlStrictElement()**
instances for XHTML 1.0 Strict semantics.

*class* smallparts.markup.generators.**XhtmlTransitionalGenerator**()

same as above, but with
**[smallparts.markup.elements](./smallparts.markup.elements.md).XhtmlTransitionalElement()**
instances for XHTML 1.0 Transitional semantics.

*class* smallparts.markup.generators.**HtmlGenerator**()

same as above, but with
**[smallparts.markup.elements](./smallparts.markup.elements.md).HtmlElement()**
instances for HTML 5 semantics.


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

```

