#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# testing for animation
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import os
import uuid
import unittest
from gems import composite, filetree

from nose.tools import nottest


# config
# ______
__resources__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')


# tests
# -----
class TestComposite(unittest.TestCase):
    _dict = {
        'one': 1,
        'two': [1, 2, 3],
        'three': ['one', 2, {'three': 'four'}],
        'four': {'five': [6, 7, 8], 'nine': 10, 'eleven': 'twelve'}
    }
    _list = [
        1, {'two': 3, 'four': 'five', 'six': [7, 8, 9, 'ten']},
        [11, 12, {'thirteen': 'fourteen', 'fifteen': 16, 'seventeen': [18]}]
    ]
    _c1 = composite({
        'one': 1,
        'two': [1, 2],
        'three': {'four': 5, 'five': 7},
        'eight': 8
    })
    _c2 = composite({
        'one': 1,
        'two': [1, 2, 3],
        'three': {'four': 5, 'six': 7},
        'eight': 9,
        'nine': 10
    })

    def test_load(self):
        data = composite(self._dict)
        self.assertEqual(sorted(data.keys()), sorted(self._dict.keys()))
        self.assertEqual(len(data), 4)
        data = composite.from_string(str(self._dict))
        self.assertEqual(sorted(data.keys()), sorted(self._dict.keys()))
        self.assertEqual(len(data), 4)
        data = composite.load(open(os.path.join(__resources__, 'dict.json'), 'r'))
        self.assertEqual(sorted(data.keys()), sorted(self._dict.keys()))
        self.assertEqual(len(data), 4)

        data = composite(self._list)
        self.assertEqual(data.keys(), None)
        self.assertEqual(len(data), 3)
        data = composite.from_string(str(self._list))
        self.assertEqual(data.keys(), None)
        self.assertEqual(len(data), 3)
        data = composite.load(open(os.path.join(__resources__, 'list.json'), 'r'))
        self.assertEqual(data.keys(), None)
        self.assertEqual(len(data), 3)
        return

    def test_write(self):
        data = composite(self._dict)
        fname = '.datatypes-test-' + str(uuid.uuid1()) + '.json'
        with open(fname, 'w') as of:
            data.write(of, pretty=True)
        with open(fname, 'r') as fi:
            data2 = composite.load(fi)
        self.assertEqual(data, data2)
        os.remove(fname)
        return

    def test_properties(self):
        data = composite(self._dict)
        self.assertEqual(data.one, 1)
        self.assertEqual(data['one'], 1)
        self.assertEqual(data.two[1], 2)
        self.assertEqual(data.three[2].three, 'four')
        self.assertEqual(data.four.five[2], 8)
        self.assertEqual(data.four.five[1:3], [7, 8])
        data.one = 2
        self.assertEqual(data.one, 2)
        self.assertEqual(data._dict['one'], 2)
        data['one'] = 3
        self.assertEqual(data.one, 3)
        data.five = 6
        self.assertEqual(data.five, 6)
        self.assertEqual(data._dict['five'], 6)
        data['five'] = 7
        self.assertEqual(data.five, 7)

        data = composite(self._list)
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1].six[3], 'ten')
        self.assertEqual(data[2][1], 12)
        self.assertEqual(data[2][2].seventeen[0], 18)
        self.assertEqual(data[1].six[0:2], [7, 8])
        data[0] = 2
        self.assertEqual(data[0], 2)
        return

    def test_iteration(self):
        data = composite(self._dict)
        self.assertEqual(sorted([i for i in data]), sorted(['one', 'two', 'three', 'four']))
        self.assertEqual([i for i in data.two], [1, 2, 3])

        data = composite(self._list)
        self.assertEqual([i for i in data][0], 1)
        self.assertEqual(sorted([i for i in data[2][2]]), sorted(['thirteen', 'fifteen', 'seventeen']))
        return

    def test_add(self):
        data = composite(self._dict)
        self.assertTrue(isinstance(data + {'five': 6}, composite))
        self.assertTrue(isinstance(data + 6, composite))
        self.assertTrue(isinstance(data + [1, 2], composite))
        self.assertTrue(isinstance(data + composite([1, 2]), composite))
        obj = data + {'five': 6}
        self.assertEqual(obj.one, 1)
        self.assertEqual(obj.five, 6)
        obj = data + {'one': 2}
        self.assertEqual(obj.one, 2)
        obj += {'one': 2}
        self.assertEqual(obj.one, 2)
        obj = data + 6
        self.assertEqual(obj[0].one, 1)
        self.assertEqual(obj[1], 6)
        obj = data + [1, 2]
        self.assertEqual(obj[0].one, 1)
        self.assertEqual(obj[1][1], 2)

        data = composite(self._list)
        self.assertTrue(isinstance(data + {'five': 6}, composite))
        self.assertTrue(isinstance(data + 6, composite))
        self.assertTrue(isinstance(data + [1, 2], composite))
        self.assertTrue(isinstance(data + composite([1, 2]), composite))
        obj = data + {'five': 6}
        self.assertEqual(obj[0][0], 1)
        self.assertEqual(obj[1].five, 6)
        obj = data + 6
        self.assertEqual(obj[-1], 6)
        self.assertEqual(obj[1].two, 3)
        obj = data + [1, 2]
        self.assertEqual(obj[-2:], [1, 2])
        self.assertEqual(obj[1].six[1], 8)

        obj = composite({}) + data
        self.assertEqual(obj[1].two, 3)

        obj = data + composite({})
        self.assertEqual(obj[1].two, 3)
        return

    def test_eq(self):
        data = composite(self._dict)
        self.assertEqual(data, self._dict)
        self.assertEqual(data, composite(self._dict))
        self.assertNotEqual(data, self._list)
        self.assertNotEqual(data, composite(self._list))
        return

    def test_exceptions(self):
        data = composite(self._dict)
        with self.assertRaises(KeyError):
            data['notakey']
        with self.assertRaises(AttributeError):
            data.notakey
        return

    def test_intersection(self):
        result = composite({
            'one': 1,
            'two': [1, 2],
            'three': {'four': 5},
        })
        self.assertEqual(self._c1.intersection(self._c2), result)
        return

    def test_difference(self):
        result = composite({
            'two': [3],
            'three': {'six': 7},
            'eight': 9,
            'nine': 10
        })
        self.assertEqual(self._c2.difference(self._c1), result)
        return

    def test_union(self):
        result = composite({
            'one': 1,
            'two': [1, 2, 3],
            'three': {'four': 5, 'five': 7, 'six': 7},
            'eight': [8, 9],
            'nine': 10
        })
        self.assertEqual(self._c1.union(self._c2), result)
        return


class TestFiletree(unittest.TestCase):
    _dir = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

    def test_properties(self):
        data = filetree(self._dir)
        self.assertTrue(os.path.exists(data.tests['test_datatypes.py']))
        self.assertTrue('tests/test_datatypes.py' in data.tests['test_datatypes.py'])
        self.assertTrue(isinstance(data['tests'].resources, filetree))
        self.assertTrue(os.path.exists(data.tests.resources['dict.json']))
        self.assertTrue('tests/resources/dict.json' in data.tests.resources['dict.json'])
        return

    def test_operators(self):
        data = filetree(self._dir)
        self.assertTrue('tests/resources' in data)
        self.assertTrue('tests/resources/dict.json' in data)
        self.assertFalse('tests/resources/di.json' in data)
        self.assertFalse('fakefile' in data)
        return

    def test_get(self):
        data = filetree(self._dir)
        self.assertTrue('tests/test_datatypes.py' in data.tests.get('test_datatypes.py'))
        self.assertEqual(data.tests.get('test_datatypes.pypy'), None)
        return

    def test_json(self):
        data = filetree(self._dir)
        json = data.json()
        self.assertEqual(sorted(json.keys()), sorted([name for name in data._data]))
        self.assertEqual(json['tests']['resources']['dict.json'], data.tests.resources['dict.json'])
        return

    def test_match(self):
        data = filetree(self._dir, regex=r".*.json$")
        self.assertEqual(len(data.files()), 2)
        self.assertTrue('dict.json' in sorted(data.files())[0])
        self.assertTrue('list.json' in sorted(data.files())[1])
        return

    def test_prune(self):
        raw = filetree(self._dir)
        data = filetree(self._dir, regex=r".*.json$")
        pruned = data.prune(r".*.json$")
        self.assertEqual(data, pruned)
        return

    def test_exceptions(self):
        raw = filetree(self._dir)
        with self.assertRaises(KeyError):
            raw['notafile']
        with self.assertRaises(AttributeError):
            raw.notafile
        return

