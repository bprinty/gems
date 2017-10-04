# -*- coding: utf-8 -*-
#
# Decorator testing
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import unittest
from gems import require, exception, keywords

from nose.tools import nottest


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
