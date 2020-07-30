# smallparts.text.templates

> One class enhancing the string.Template class.  
> Source: [smallparts/text/templates.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/text/templates.py)

## Module contents

### Classes

#### *class* smallparts.markup.templates.**EnhancedStringTemplate**(template)

This is a subclass of [string.Template](https://docs.python.org/library/string.html#string.Template)
defining one additional property (**.variable_names**) containing the set
of variable names from the template.

## Usage examples

```python
>>> from smallparts.text import templates
>>> tmpl = templates.EnhancedStringTemplate('${salutation} $customer,\n\n'
... 'your order (${order_data}) has been placed and'
... ' will be delivered at ${delivery_date}.')
>>> tmpl.variable_names
{'customer', 'delivery_date', 'salutation', 'order_data'}
>>> 
```

----
[(smallparts docs home)](./)

