# smallparts.namespaces

> Simple namespaces initialized like dicts (in fact, they are based on dicts).  
> Source: [smallparts/namespaces.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/namespaces.py)

## Module contents

### Classes

#### *class* smallparts.namespaces.**Namespace**(…)

This is a subclass of **[dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)**
instantiated the same way like you would call **dict()**.
Members with keys that represent
[valid identifiers](https://docs.python.org/3/reference/lexical_analysis.html#identifiers)
can be accessed as instance attributes.  
The only reserved attribute is **.items**.
In reverse, **.items()** is the only inherited **dict** method accessible in a
Namespace instance.

Namespace instances can be serialized like dicts by the
standard library’s [json module](https://docs.python.org/3/library/json.html).

#### *class* smallparts.namespaces.**DefaultNamespace**(*\*args, \*\*kwargs*)

This is a subclass of **Namespace** returning a default value (and caching it
at the same time) when not-yet-existing attributes are accessed, instead of
raising an AttributeError. The default value is given using the keyword parameter
*default* when instantiating, and stored in the **.default__value__** attribute.
It defaults to ```None```.

#### *class* smallparts.namespaces.**EnhancedNamespace**(…)

This is a subclass of **Namespace** with additional constructor methods:

**.from_object**(*object_, names=None*)  
**.from_mapping**(*mapping, names=None*)  
**.from_sequence**(*sequence, names=None*)

Each of these methods returns an **EnhancedNamespace** instance
constructed from the given object, mapping or sequence (of (key, value) pairs).
If a sequence of names is provided, only add attributes with one of these
names to the namespace if found in the original item.


#### *class* smallparts.namespaces.**InstantNames**(*\*translation_functions, \*\*set_values_directly*)

This is a subclass of **dict** which can be used to generate and cache strings
instantly when an attribute is accessed.  
If an accessed attribute does not exist yet, its name is processed
through all translation functions given as positional arguments.
You can use functions like str.lower, str.upper as well as – for example – those
from the [smallparts.text.translate](./smallparts.text.translate.md) module.
All functions taking a string as single argument and returning a string
are suitable.
The attribute value is calculated one time only, then cached.  
If keyword arguments are provided to a new instance,
these attributes are set directly.

InstantNames instances do not expose any of the **dict** methods.
They only have one fixed attribute: **.translation_functions** is a tuple
containing the translation functions which are applied to all newly accessed
attribute names as described above.

## Usage examples

```python
>>> from smallparts import namespaces
>>> simple_namespace = namespaces.Namespace(one=1, two=2, owner='me')
>>> simple_namespace.one
1
>>> simple_namespace.two
2
>>> simple_namespace.owner
'me'
>>> # Accessing undefined attributes raises an AttributeError:
>>> simple_namespace.three
Traceback (most recent call last):
  File "………/smallparts/namespaces.py", line 52, in __getattribute__
    return self[name]
KeyError: 'three'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "………/smallparts/namespaces.py", line 54, in __getattribute__
    raise AttributeError(
AttributeError: 'Namespace' object has no attribute 'three'
>>> 
>>> # The json module can serialize Namespace instances:
>>> import json
>>> json.dumps(simple_namespace)
'{"one": 1, "two": 2, "owner": "me"}'
>>> 
>>> factor = namespaces.DefaultNamespace(zero=0, double=2, triple=3, default=1)
>>> dir(factor)
['double', 'triple', 'zero']
>>> 4 * factor.double
8
>>> 4 * factor.triple
12
>>> 4 * factor.zero
0
>>> 4 * factor.undefined
4
>>> dir(factor)
['double', 'triple', 'undefined', 'zero']
>>> factor.undefined
1
>>> factor.any
1
>>> 
>>> enhanced_namespace = namespaces.EnhancedNamespace.from_object(simple_namespace, names=('two', 'owner'))
>>> enhanced_namespace
EnhancedNamespace({'two': 2, 'owner': 'me'})
>>> 
>>> # You can duplicate simple namespaces more easily:
>>> another_simple_namespace = namespaces.Namespace(simple_namespace.items())
>>> 
>>> from smallparts.text import translate
>>> shout = namespaces.InstantNames(str.upper, translate.underscores_to_blanks)
>>> shout.this_is_a_simple_example
'THIS IS A SIMPLE EXAMPLE'
>>> 
```

----
[(smallparts docs home)](./)

