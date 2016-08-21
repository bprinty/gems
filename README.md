gems
===============================

Python utilities for data manipulation and management.


Installation
------------

Via github:

```bash
git clone http://github.com/bprinty/gems.git
cd gems
python setup.py install
```

Via pip:

```bash
pip install gems
```


Documentation
-------------

Documentation for the package can be found [here](http://gems.readthedocs.io/en/latest/index.html).


Usage
-----

The [gems](http://github.com/bprinty/gems) module provides specialized data structures to augment development. It's similar to the [collections](https://docs.python.org/2/library/collections.html) module, but contains different types of objects.

Currently, the following objects are available (this list will grow with time and feedback):

Name         | Description
------------ | -------------
composite    | JSON-like data structure for easy data traversal.


### composite

Here is an example of how to use the ``composite`` type in a project:

```python
>>> from gems import composite
>>>
>>> data = composite({
>>>     'one': 1,
>>>     'two': [1, 2, 3],
>>>     'three': ['one', 2, {'three': 'four'}],
>>>     'four': {'five': [6, 7, 8], 'nine': 10, 'eleven': 'twelve'}
>>> })
>>> data.four.five[1] == 6
True
>>> data.two[0] == 1
True
```

In the example above, an arbitrary data structure is provided as an argument to the ``composite`` object, and is transformed into an object where properties can be traversed more gracefully (syntactically).

There are also operations tied to ``composite`` objects. If two composite objects or a composite object and another similar type are added, you get a ``composite`` object as a result that combines the objects in an intuitive way:

```python
>>> # using the 'data' object from above
>>> obj = data + {'five': 6}
>>> obj.five == 6
True
>>> obj.two === [1, 2, 3]
True

>>> obj = data + [1, 2, 3]
>>> obj[0].one.two[0] == 1
True
>>> obj[1][1] == 2
True

>>> data2 = composite([
    1, 2, 3, {'four': 5}
])
>>> obj = data2 + {'five': 6}
>>> obj[0][0] == 1
True
>>> obj[0][2].four == 5
True
>>> obj = data2 + ['seven', 8, 9]
>>> obj[4:6] == ['seven', 8]
True
```

Other operations like this also can be used with the ``composite`` object. For example:

```python
>>> # using the 'data' object from above
>>> 'three' in data
True
>>> 7 in data.four.five
True
>>> data.four.five == [6, 7, 8]
True
>>> data == data2
False
```


Questions/Feedback
------------------

File an issue in the [GitHub issue tracker](https://github.com/bprinty/animation/issues).
