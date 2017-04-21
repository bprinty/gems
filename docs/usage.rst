Usage
========

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
~~~~~~~~~

The :class:`gems.composite` object abstracts away the complexity associated with managing heavily nested JSON-based structures, allowing easier access to internal properties, and providing operators that work with the data in an intuitive way. Here is a simple example of how to use the :class:`composite` type in a project:

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


Some of the main features of ``composite`` objects that make them particularly useful are operators for interacting with the structure. For instance, if two composite objects or a composite object and another similar type are added, you get a ``composite`` object as a result that combines the objects in an intuitive way:

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

Along with these operators, ``composite`` objects also extend set-based functionality for reducing data. For example:

.. code-block:: python
    
    >>> # initialize some data
    >>> c1 = composite({
    >>>     'one': 1,
    >>>     'two': [1, 2],
    >>>     'three': {'four': 5, 'five': 7},
    >>>     'eight': 8
    >>> })
    >>> c2 = composite({
    >>>     'one': 1,
    >>>     'two': [1, 2, 3],
    >>>     'three': {'four': 5, 'six': 7},
    >>>     'eight': 9,
    >>>     'nine': 10
    >>> })
    >>>
    >>> # take the recursive intersection of the data structures
    >>> print c1.intersection(c2)
    {
        'one': 1,
        'two': [1, 2],
        'three': {'four': 5},
    }
    >>>
    >>> # take the recursive difference of the data structures
    >>> print c2.difference(c1)
    {
        'two': [3],
        'three': {'six': 7},
        'eight': 9,
        'nine': 10
    }
    >>>
    >>> # take the recursive union of the data structures
    >>> print c1.union(c2)
    {
        'one': 1,
        'two': [1, 2, 3],
        'three': {'four': 5, 'five': 7, 'six': 7},
        'eight': [8, 9],
        'nine': 10
    }


Finally, you can write composite objects back to JSON files easily:

.. code-block:: python

    >>> # change the data in the object
    >>> data.four.five = 2
    >>>
    >>> with open('newdata.json', 'w') as nd:
    >>>     data.write(nd)


By default, this will sort keys and pretty-print to the file, but if you just want to print the raw json to file, use ``pretty=False``.


filetree
~~~~~~~~

Traversal of a filetree is typically a pain in python. You could use ``os.path.walk`` recursively to accomplish it, but there should be an easier way. That's where the :class:`gems.filetree` comes in handy. Here is an example of how to use the :class:`gems.filetree` type in a project:

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

The :class:`gems.filetree` structure also allows for traversal of the file data like so:

.. code-block:: python

    >>> print data.one['two.txt']
    /full/path/to/mydir/one/two.txt
    >>>
    >>> print data.two.three['four.txt']
    /full/path/to/mydir/two/three/four.txt
    >>>
    >>> print data.two['five six']['eight.config']
    /full/path/to/mydir/two/five six/eight.config

As you can see in the example above, using JSON-based access is much easier and cleaner than doing many ``os.path.join`` operations to create the full paths to objects on your filesystem. You can also create a json structure from the filetree:

.. code-block:: python

    >>> print data.json()
    {
        "one": {
            "two.txt": "/path/to/mydir/one/two.txt",
            "three.json": "/path/to/mydir/one/three.json"
        },
        "two": {
            "three": {
                "four.txt": "/path/to/mydir/two/three/four.txt"
            },
            "five six": {
                "seven.txt": "/path/to/mydir/two/five six/seven.txt"
            },
            "eight.config": "/path/to/mydir/two/eight.config"
        }
    }

Or, if you just want to see a list of all files in the filetree, you can do the following:

.. code-block:: python

    >>> print data.files()
    '/path/to/mydir/one/two.txt'
    '/path/to/mydir/one/three.json'
    '/path/to/mydir/two/three/four.txt'
    '/path/to/mydir/two/five six/seven.txt'
    '/path/to/mydir/two/eight.config'

Finally, to prune the tree for specific files and create a new filetree object:

.. code-block:: python
    
    >>> newtree = data.prune(regex=".*.txt$")
    >>> print newtree.files()
    '/path/to/mydir/one/two.txt'
    '/path/to/mydir/two/three/four.txt'
    '/path/to/mydir/two/five six/seven.txt'
