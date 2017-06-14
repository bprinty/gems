# -*- coding: utf-8 -*-
#
# Decorator testing
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import unittest
from gems import require

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
