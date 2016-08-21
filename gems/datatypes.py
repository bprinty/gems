# -*- coding: utf-8 -*-
#
# Decorators for terminal-based wait animations
#
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import json


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
        self._data = data
        self._list, self._dict = [], {}

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

    def __getitem__(self, idx):
        return self._list[idx]

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
                    for k in other._dict:
                        newdict[k] = other._dict[k]
                    for k in self._dict:
                        newdict[k] = self._dict[k]
                    return composite(newdict)
                else:
                    return self
            elif isinstance(other, dict):
                newdict = {}
                for k in other:
                    newdict[k] = other[k]
                for k in self._dict:
                    newdict[k] = self._dict[k]
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

