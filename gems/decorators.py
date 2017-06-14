# -*- coding: utf-8 -*-
#
# Useful decorators.
#
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
from functools import wraps


# decorators
# ----------
def require(method):
    """
    Decorator for managing chained dependencies of different class
    properties. The @require decorator allows developers to specify
    that a function call must be operated on before another property
    or function call is accessed, so that data and processing for an
    entire class can be evaluated in a lazy way (i.e. not all upon
    instantiation).

    Examples:

        >>> class Foo(Bar):
        >>>
        >>>    def a(self):
        >>>        print 'a!'
        >>>        return 1
        >>>
        >>>    @require('a')
        >>>    @property
        >>>    def b(self):
        >>>        print 'b!'
        >>>        return self.a + 1
        >>>
        >>> foo = Foo()
        >>> print foo.b
        >>>
        'a!'
        'b!'
        2
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # throw exception if input class doesn't have requirement
            if not hasattr(args[0], method):
                raise AssertionError('{} class has no method {}()'.format(args[0].__class__.__name__, method))

            # create property to record that method has been called
            callmethod = method + '_called'
            if not hasattr(args[0], callmethod):
                setattr(args[0], callmethod, False)

            # call the method if it hasn't yet been called
            if not getattr(args[0], callmethod):
                getattr(args[0], method)()
                setattr(args[0], callmethod, True)
            return func(*args, **kwargs)
        return wrapper
    return decorator
