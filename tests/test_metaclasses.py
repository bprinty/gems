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
import six


# tests
# -----
class TestDocRequire(unittest.TestCase):

    def test_docrequire(self):
        # raises AssertionError when evaled
        with self.assertRaises(AssertionError):
            
            @six.add_metaclass(DocRequire)
            class A(object):    
                def method(self):
                    return
        
        # shouldn't raise an AssertionError
        with self.assertRaises(TypeError):
            
            @six.add_metaclass(DocRequire)
            class A(object):
                def method(self):
                    """ okay """
                    return
            
            raise TypeError
        return
