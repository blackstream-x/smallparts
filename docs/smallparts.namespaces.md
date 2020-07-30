# smallparts.namespaces

> Simple namespaces initialized like dicts (in fact, they are based on dicts).  
> Source: [smallparts/namespaces.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/namespaces.py)

## Module contents

### Classes

#### *class* smallparts.namespaces.**Namespace**(...)

This is a subclass of **[dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)**
instantiated the same way as you would call **dict()**.
Members with keys that represent
[valid identifiers](https://docs.python.org/3/reference/lexical_analysis.html#identifiers)
can be accessed as instance attributes. The only reserved attribute is **.items**.
In reverse, **.items()** is the only inherited **dict** method accessible in a
Namespace instance.

Namespace instances can be serialized like dicts by the
standard library’s [json module](https://docs.python.org/3/library/json.html).

_(tbc)_
 
## Usage examples

```python
>>> from smallparts import namespaces
>>> from smallparts import namespaces
>>> import json
>>> simple_namespace = namespaces.Namespace(one=1, two=2, owner='me')
>>> simple_namespace.one
1
>>> simple_namespace.two
2
>>> simple_namespace.three
Traceback (most recent call last):
  File "/………/smallparts/namespaces.py", line 52, in __getattribute__
    return self[name]
KeyError: 'three'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/………/smallparts/namespaces.py", line 54, in __getattribute__
    raise AttributeError(
AttributeError: 'Namespace' object has no attribute 'three'
>>> simple_namespace.owner
'me'
>>> json.dumps(simple_namespace)
'{"one": 1, "two": 2, "owner": "me"}'
>>> 
```

----
[(smallparts docs home)](./)

