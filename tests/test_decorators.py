# -*- coding: utf-8 -*-
#
# Decorator testing
#
# ------------------------------------------------


# imports
# -------
import unittest
from datetime import datetime
from gems import require, exception, keywords, cached


# tests
# -----
class TestRequire(unittest.TestCase):
    _a = None

    def requirement(self):
        self._a = 1
        return None

    @property
    @require('requirement')
    def property(self):
        return self._a

    def test_require(self):
        self.assertEqual(self._a, None)
        self.assertEqual(self.property, 1)
        return


class CacheExample(object):

    @cached.tag('reset')
    def time(self):
        return str(datetime.now().time())

    @cached.tag('reset')
    def ftime(self):
        return 'time: ' + str(datetime.now().time())


class CacheChildExample(CacheExample):

    @cached.tag('reset')
    def ctime(self):
        return str(datetime.now().time())


class TestCached(unittest.TestCase):

    def test_cached(self):
        # multiple properties
        foo = CacheExample()
        time = foo.time
        ftime = foo.ftime
        self.assertEqual(foo.time, time)
        self.assertEqual(foo.ftime, ftime)
        cached.invalidate(foo, 'reset')
        newtime = foo.time
        newftime = foo.ftime
        self.assertNotEqual(newtime, time)
        self.assertNotEqual(newftime, ftime)
        self.assertEqual(newtime, foo.time)
        self.assertEqual(newftime, foo.ftime)

        # multiple classes
        bar = CacheExample()
        btime = bar.time
        self.assertEqual(bar.time, btime)
        self.assertEqual(newtime, foo.time)
        cached.invalidate(bar, 'reset')
        finaltime = foo.time
        newbtime = bar.time
        self.assertNotEqual(newbtime, btime)
        self.assertEqual(finaltime, newtime)
        self.assertEqual(newbtime, bar.time)

        # object independence
        cached.invalidate(foo, 'reset')
        self.assertNotEqual(finaltime, foo.time)
        return

    def test_inheritance_cached(self):
        foo = CacheChildExample()
        time = foo.time
        ctime = foo.ctime
        self.assertEqual(foo.time, time)
        self.assertEqual(foo.ctime, ctime)
        cached.invalidate(foo, 'reset')
        newtime = foo.time
        newctime = foo.ctime
        self.assertNotEqual(newtime, time)
        self.assertNotEqual(newctime, ctime)
        self.assertEqual(newtime, foo.time)
        self.assertEqual(newctime, foo.ctime)
        return


class CustomException(Exception):
    pass


class TestException(unittest.TestCase):

    @exception(CustomException)
    def throw(self):
        raise AssertionError('This is an exception!')

    def test_exception(self):
        with self.assertRaises(CustomException):
            self.throw()
        return


class TestKeywords(unittest.TestCase):

    @keywords
    def function(self, *args, **kwargs):
        return args, kwargs

    def test_keywords(self):
        args, kwargs = self.function(one=1, two=2)
        self.assertEqual(len(args), 0)
        self.assertEqual(kwargs, {'one': 1, 'two': 2})

        args, kwargs = self.function(1, two=2)
        self.assertEqual(len(args), 1)
        self.assertEqual(kwargs, {'two': 2})

        args, kwargs = self.function({'one': 1}, two=2)
        self.assertEqual(len(args), 0)
        self.assertEqual(kwargs, {'one': 1, 'two': 2})

        args, kwargs = self.function({'one': 1}, two=2)
        self.assertEqual(len(args), 0)
        self.assertEqual(kwargs, {'one': 1, 'two': 2})
        return
