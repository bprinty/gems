# -*- coding: utf-8 -*-
#
# Decorators for terminal-based wait animations
#
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import json
import os
import re


# data management
# -----------------
class composite(object):
    """
    Data structure for traversing object relationships via attributes
    instead of keys and indices.

    Args:
        data (tuple, list, dict): Data to build composite datastructure from.

    Example:
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
    """

    def __init__(self, data):
        self._list = []
        self._dict = {}

        if isinstance(data, file):
            data = json.load(data)

        if isinstance(data, (list, tuple)):
            for dat in data:
                if not isinstance(dat, (list, tuple, dict)):
                    self._list.append(dat)
                else:
                    self._list.append(composite(dat))

        elif isinstance(data, dict):
            for key in data:
                if not isinstance(data[key], (list, tuple, dict)):
                    self._dict[key] = data[key]
                else:
                    self._dict[key] = composite(data[key])
        return

    @classmethod
    def load(cls, fh):
        """
        Load data from file handle.

        Args:
            fh (file): File handle to load from.

        Examlple:
            >>> with open('data.json', 'r') as json:
            >>>    data = composite.load(json)
        """
        return cls(json.load(fh))

    @classmethod
    def from_string(cls, string):
        """
        Load data from string.

        Args:
            string (str): String to load from.

        Examlple:
            >>> with open('data.json', 'r') as json:
            >>>     jdat = json.read()
            >>> data = composite.from_string(jdat)
        """
        return cls(eval(string))

    def __len__(self):
        return max(len(self._list), len(self._dict))

    def __str__(self):
        return str(self.json())

    def __iter__(self):
        if len(self._list) != 0:
            for entry in self._list:
                yield entry

        elif len(self._dict) != 0:
            for entry in self._dict:
                yield entry

    def __getattr__(self, name):
        return self._dict.get(name)

    def __getitem__(self, item):
        if len(self._list) != 0:
            return self._list[item]
        elif len(self._dict) != 0:
            return self._dict[item]
        else:
            return None

    def __setattr__(self, name, value):
        if name == '_list' or name == '_dict':
            super(composite, self).__setattr__(name, value)
        else:
            self._dict[name] = value

    def __setitem__(self, idx, value):
        if len(self._list) != 0:
            self._list[idx] = value
        elif len(self._dict) != 0:
            self._dict[idx] = value

    def __add__(self, other):
        if len(self._list) != 0:
            if isinstance(other, composite):
                if len(other._list) != 0:
                    return composite(self._list + other._list)
                elif len(other._dict) != 0:
                    return composite([self._list, other._dict])
                else:
                    return self
            elif isinstance(other, dict):
                return composite([self._list, other])
            elif isinstance(other, (list, tuple)):
                return composite(self._list + other)
            else:
                return composite(self._list + [other])
        elif len(self._dict) != 0:
            if isinstance(other, composite):
                if len(other._list) != 0:
                    return composite([self._dict, other._list])
                elif len(other._dict) != 0:
                    newdict = {}
                    for k in self._dict:
                        newdict[k] = self._dict[k]
                    for k in other._dict:
                        newdict[k] = other._dict[k]
                    return composite(newdict)
                else:
                    return self
            elif isinstance(other, dict):
                newdict = {}
                for k in self._dict:
                    newdict[k] = self._dict[k]
                for k in other:
                    newdict[k] = other[k]
                return composite(newdict)
            else:
                return composite([self._dict, other])
        else:
            if isinstance(other, composite):
                return other
            else:
                return composite(other)
        return

    def __contains__(self, item):
        if len(self._list) != 0:
            return item in self._list
        elif len(self._dict) != 0:
            return item in self._dict

    def __eq__(self, other):
        if len(self._list) != 0:
            if isinstance(other, composite):
                if len(other._list) != 0:
                    return self._list == other._list
                elif len(other._dict) != 0:
                    return False
            elif isinstance(other, dict):
                return False
            elif isinstance(other, (list, tuple)):
                return self._list == other
            else:
                return False
        elif len(self._dict) != 0:
            if isinstance(other, composite):
                if len(other._list) != 0:
                    return False
                elif len(other._dict) != 0:
                    return self._dict == other._dict
            elif isinstance(other, dict):
                return self._dict == other
            else:
                return False
        return

    def keys(self):
        """
        Return keys for object, if they are available.
        """
        if len(self._list) != 0:
            return None
        elif len(self._dict) != 0:
            return self._dict.keys()

    def json(self):
        """
        Return JSON representation of object.
        """
        if len(self._list) != 0:
            ret = []
            for dat in self._list:
                if not isinstance(dat, composite):
                    ret.append(dat)
                else:
                    ret.append(dat.json())
            return ret

        elif len(self._dict) != 0:
            ret = {}
            for key in self._dict:
                if not isinstance(self._dict[key], composite):
                    ret[key] = self._dict[key]
                else:
                    ret[key] = self._dict[key].json()
            return ret


# data management
# -----------------
class filetree(object):
    """
    Data structure for traversing directory structure and creating object for
    accessing relative file paths.

    .. NOTE: The filetree is completely walked through when this object is
        instantiated, so expect object creation for large trees to be
        relatively expensive.

    Args:
        directory (str): Directory to build filetree from.
        ignore (str): Regular expression with items to ignore. If you wish
            to recurse through all directories (including hidden directories),
            set ignore=None. By default, this is set to "^[._]" (i.e. any files
            beginning with "." or "_").

    Example:
        >>> data = filetree('mydir')
        >>> print data
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
        >>> print data.one['two.txt']
        /full/path/to/mydir/one/two.txt
        >>> print data.two.three['four.txt']
        /full/path/to/mydir/two/three/four.txt
        >>> print data.two['five six']['eight.config']
        /full/path/to/mydir/two/five six/eight.config
    """

    def __init__(self, directory, ignore=r"^[._]"):
        self.root = os.path.realpath(directory)
        self._data = {}
        for item in os.listdir(self.root):
            if ignore is not None:
                if re.search(ignore, item):
                    continue
            fullpath = os.path.realpath(os.path.join(self.root, item))
            if os.path.isdir(fullpath):
                self._data[os.path.basename(fullpath)] = filetree(fullpath)
            else:
                self._data[os.path.basename(fullpath)] = fullpath
        return

    def __len__(self):
        return len(self._data)

    def __str__(self):
        """
        .. NOTE:: This needs to be completed -- print filetree
        """
        def jstr(data, tab=''):
            res = ''
            for item in data:
                if isinstance(data[item], basestring):
                    res += tab + item + '\n'
                else:
                    res += tab + item + '/\n'
                    res += jstr(data[item], tab=tab+'\t')
            return res
        return jstr(self.json())

    def __iter__(self):
        for item in self._data:
            yield self._data[item]

    def __getattr__(self, name):
        if name not in self._data:
            raise AttributeError('filetree object has no attribute {}!'.format(name))
        return self._data[name]

    def __getitem__(self, item):
        if item not in self._data:
            raise AttributeError('filetree object has no attribute {}!'.format(item))
        return self._data[item]

    def __contains__(self, item):
        if item in self._data:
            return True
        item = item.replace(self.root, '')
        item = re.sub(r"^[/\\]", "", item)
        subpaths = item.split("/")
        idx, cdata = 0, self
        try:
            while idx < len(subpaths):
                cdata = cdata[subpaths[idx]]
                idx += 1
        except AttributeError:
            return False
        return True

    def __eq__(self, other):
        return self._data == other._data

    def json(self):
        """
        Return JSON representation of object.
        """
        data = {}
        for item in self._data:
            if isinstance(self._data[item], filetree):
                data[item] = self._data[item].json()
            else:
                data[item] = self._data[item]
        return data
