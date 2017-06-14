# -*- coding: utf-8 -*-
#
# Datatype testing
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import unittest
from gems import DocRequire

from nose.tools import nottest


# tests
# -----
class TestDocRequire(unittest.TestCase):

    def test_docrequire(self):
        # raises AssertionError when evaled
        with self.assertRaises(AssertionError):
            
            class A(object):
                __metaclass__ = DocRequire
                
                def method(self):
                    return
        
        # shouldn't raise an AssertionError
        with self.assertRaises(TypeError):
            
            class A(object):
                __metaclass__ = DocRequire
                
                def method(self):
                    """ okay """
                    return
            
            raise TypeError
        return
