|Build status| |Maintenance yes| |GitHub license| |Documentation Status|

.. |Build status| image:: https://travis-ci.org/bprinty/gems.png?branch=master
   :target: https://travis-ci.org/bprinty/gems

.. |Maintenance yes| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity

.. |GitHub license| image:: https://img.shields.io/github/license/Naereen/StrapDown.js.svg
   :target: https://github.com/bprinty/gems/blob/master/LICENSE

.. |Documentation Status| image:: https://readthedocs.org/projects/gems/badge/?version=latest
   :target: http://gems.readthedocs.io/?badge=latest


gems
====

Python utilities for data manipulation and management.


Installation
------------

Via github:

.. code-block:: bash

    ~$ git clone http://github.com/bprinty/gems.git
    ~$ cd gems
    ~$ python setup.py install

Via pip:

.. code-block:: bash

    ~$ pip install gems


Documentation
-------------

Documentation for the package can be found `here <http://gems.readthedocs.io/en/latest/index.html>`_.


Usage
-----

The `gems <http://github.com/bprinty/gems>`_ module provides specialized data structures to augment development. It's similar to the `collections <https://docs.python.org/2/library/collections.html>`_ module, but contains different types of objects.

Currently, the following objects are available (this list will grow with time and feedback):

+------------+---------------------------------------------------------+ 
| Name       | Description                                             | 
+============+=========================================================+ 
| composite  | JSON-like data structure for easy data traversal.       | 
+------------+---------------------------------------------------------+ 
| filetree   | JSON-like data structure for easy filesystem traversal. | 
+------------+---------------------------------------------------------+ 


composite
+++++++++

The ``composite`` object abstracts away the complexity associated with managing heavily nested JSON-based structures, allowing easier access to internal properties, and providing operators that work with the data in an intuitive way. Here is a simple example of how to use the ``composite`` type in a project:

.. code-block:: python

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


In the example above, an arbitrary data structure is provided as an argument to the ``composite`` object, and is transformed into an object where properties can be traversed more gracefully (syntactically). You can also load a composite object from a json or yaml file like so:

.. code-block:: python

    >>> from gems import composite
    >>>
    >>> with open('data.json', 'r') as fi:
    >>>     data = composite.load(fi)
    >>>
    >>> print data.four.five[1]
    6
    >>>
    >>> with open('data.yml', 'r') as fi:
    >>>     data = composite.load(fi)
    >>>
    >>> print data.four.five[1]
    6


There are also operations tied to ``composite`` objects. If two composite objects or a composite object and another similar type are added, you get a ``composite`` object as a result that combines the objects in an intuitive way:

.. code-block:: python

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


Other operations like this also can be used with the ``composite`` object. For example:

.. code-block:: python

    >>> # using the 'data' object from above
    >>> 'three' in data
    True
    >>> 7 in data.four.five
    True
    >>> data.four.five == [6, 7, 8]
    True
    >>> data == data2
    False


filetree
++++++++

Traversal of a filetree is typically a pain in python. You could use ``os.path.walk`` to within a recursive function to accomplish it, but there should be an easier way. That's where the ``gems.filetree`` comes in handy. Here is an example of how to use the ``gems.filetree`` type in a project:

.. code-block:: python

    >>> from gems import filetree
    >>>
    >>> # mydir is a directory with the structure below
    >>> ftree = filetree('mydir')
    >>> print ftree
    mydir/
         one/
            two.txt
            three.json
        two/
            three/
                  four.txt
            five six/
                     seven.txt
            eight.config

The ``gems.filetree`` structure also allows for traversal of the file data like so:

.. code-block:: python

    >>> print data.one['two.txt']
    /full/path/to/mydir/one/two.txt
    >>>
    >>> print data.two.three['four.txt']
    /full/path/to/mydir/two/three/four.txt
    >>>
    >>> print data.two['five six']['eight.config']
    /full/path/to/mydir/two/five six/eight.config

Using JSON-based access is much easier and cleaner than doing many ``os.path.join`` operations to create the full paths to objects on your filesystem. 


Questions/Feedback
------------------

File an issue in the `GitHub issue tracker <https://github.com/bprinty/gems/issues>`_.
