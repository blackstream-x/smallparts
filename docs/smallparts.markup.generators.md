# smallparts.markup.generators

> XML, XHTML 1.0 and HTML 5 element generator functions and classes.  
> Source: [smallparts/markup/generators.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/markup/generators.py)

## Module contents

### Constants

This module defines the following constants:

smallparts.markup.generators.**SUPPORTED_HTML_DIALECTS**

> A dict mapping each supported HTML dialect (one of the
> [smallparts.markup.elements](./smallparts.markup.elements.md#constants)
> constants **LABEL_HTML_5**, **LABEL_XHTML_1_0_STRICT** or
> **LABEL_XHTML_1_0_TRANSITIONAL**)
> to a [namespaces.Namespace()](./smallparts.namespaces.md#class-smallpartsnamespacesnamespace)
> with the following attributes suitable for the dialect:  
> **.doctype** (the DOCTYPE declaration)  
> **.xmlns** (set to ```None``` for HTML 5)

### Functions

smallparts.markup.generators.**css_property**(*property_name, property_value*)

> Return a single CSS property (property_name: property_value;)

smallparts.markup.generators.**css_important_property**(*property_name, property_value*)

> Return a single CSS important property (property\_name: property\_value !important;)

smallparts.markup.generators.**html_document**(*dialect='HTML 5', lang='en', title='Untitled page', head='', body=''*)

> Return an HTML document in one of the supported HTML dialects from
> **SUPPORTED_HTML_DIALECTS**.
> Fill in head and body content if provided.

smallparts.markup.generators.**js_function**(*function_name, arguments*)

> Return a JavaScript function call like
> ```'function_name(arg1, arg2, …, argN)'```
> where *arg1, args2, …, argN* are the items in the arguments sequence.

smallparts.markup.generators.**js_return**(*function_name,* _*arguments_)

> Return the content for an HTML onclick (or similar) attribute
> calling a JavaScript function. The result looks like
> ```'return function_name(arg1, arg2, …, argN);'```
> where *arg1, args2, …, argN* are the items given as positional arguments.

smallparts.markup.generators.**wrap_cdata**(*character_data*)

> Wrap *character_data* in a CDATA section.
> If necessary use multiple CDATA sections as suggested in
> <https://en.wikipedia.org/wiki/CDATA#Nesting>

smallparts.markup.generators.**xml_declaration**(*version='1.0', encoding='utf-8', standalone=None*)

> Returns an XML declaration with version and encoding as provided.
> With defaults, this function returns ```'<?xml version="1.0" encoding="utf-8" ?>'```  
> Adds ```' standalone="yes"'``` if *standalone* is defined als **True**, and
> ```' standalone="no"'``` if *standalone* is defined as **False** explicitly.

smallparts.markup.generators.**xml_document**(*content, version='1.0', encoding='utf-8', standalone=None*)

> Returns an XML document with an XML declaration made from the
> *version*, *encoding* and *standalone* provided, adding *content*
> after a line break.  
> ***Please note*** that *content* is not checked in any way,
> so you have to take care yourself to provide well-formed XML as content only.


## Usage examples

```python
>>> from smallparts.markup import generators
>>> print(generators.xml_document('<empty-document/>'))
<?xml version="1.0" encoding="utf-8" ?>
<empty-document/>
>>> print(generators.html_document())
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Untitled page</title>
</head>
<body></body>
</html>
>>> print(generators.html_document(dialect='XHTML 1.0 Transitional'))
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>Untitled page</title>
</head>
<body></body>
</html>
>>> 
```

----
[(smallparts docs home)](./)

