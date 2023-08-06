# strict-types
Python type checking for functions and classes. Check if the datatypes of the input parameters match the datatypes you want.

```
from strict import *
```

### StrictClass

Use _`StrictClass`_ to ensure you are assigning the correct content (with the right datatype) to the desired attribute. This class will result in an object that contains all keyword arguments passed to the class and will check the datatype of each parameter with the datatype referenced in the annotation.

It is required a child class that inherits _`StrictClass`_. That class may have some annotations describing the desired attributes and their datatypes.

```
>>> class StrictClassChild(StrictClass):
...  key: str
```

Note that `key` is referring to the attribute that will store a _`str`_ datatype — i.g., `<attribute>: <datatype>` — and, in this case, any content assigned to `key` that is not _`str`_ will raise an _`AssingError`_.

Once the class is defined, you may want to initialize the object by entering the parameters (keyword arguments).
  
```
>>> obj = StrictClassChild(key = 'word')
>>> obj.key
'word'
```
### StrictFunction

The _`StrictFunction`_ is similar to _`StrictClass`_, the difference is that this class needs a function to call. The function can be executed calling the class object.

```
>>> class StrictFunctionChild(StrictFunction):
...  data: str
...
>>> def uppercase_string(data):
...  return data.upper()
...
>>> obj = StrictFunctionChild(uppercase_string, data = 'keyword')
>>> obj()
'KEYWORD'
```

Note that the parameter `data` of the `uppercase_string` function must be a _`str`_, otherwise it will raise an exception if the `upper` method is called but doesn't exist. In addition, if the datatype of `data` is _`bytes`_ (when using the function directly), it will convert the binary content to uppercase and return a _`bytes`_ datatype. This may cause some problems especially if we are working with client input. This problem is avoided by using this class.

It is also possible to access the keyword arguments just like the other class.

```
>>> obj.data
'keyword'
```

### @strict_type

The `strict_type` acts like  _`StrictFunction`_ class, but it is used as a decorator. It will check the desired datatypes of a function (annotation) and compare with the parameters datatypes.

```
>>> @strict_type
... def uppercase_string(data: str):
...  return data.upper()
...
>>> uppercase_string('in all caps!')
'IN ALL CAPS!'
```

### Exceptions

The _`AssingError`_ is the only exceptions used by this script, but other may occur dealing with functions.

Everytime this exception is called, the parameter that generated the exception is stored and can be accessed calling the `parameter` attribute (_`str`_).  The invalid and the required datatypes may be stored as well, and both can be accessed calling the `invalid` attribute (_`type`_) and the `required` attribute (_`tuple`_) respectively.

```
>>> from strict import *
>>> class StrictClassChild(StrictClass):
...     data: str
...     multiply: int
...
>>> obj = StrictClassChild(data='Hello', multiply='5')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/strict/strict.py", line 44, in __init__
    raise AssignError(
strict.AssignError: Trying to assign an invalid datatype to the parameter "multiply". Datatype must be <class 'int'>, and not <class 'str'>.
```

Note that the exception was raised because the `multiply` parameter in the _`StrictClassChild`_ class is a string and not an integer, as required. Wrapping it all using `try` and `except` and an invalid code, we can catch the error and the attributes previously mentioned:

```
>>> try:
...     (...)
... except AssignError as err:
...     print('error message:', err)
...     print('invalid parameter:', err.parameter)
...     print('invalid datatype:', err.invalid)
...     print('required datatypes:', err.required)
...
error message: Trying to assign an invalid datatype to the parameter "multiply". Datatype must be <class 'int'>, and not <class 'str'>.
invalid parameter: multiply
invalid datatype: <class 'str'>
required datatypes: (<class 'int'>,)
```