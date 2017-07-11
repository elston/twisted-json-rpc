# -*- coding: utf-8 -*-
import collections
import inspect
import re
import importlib
import types
# ...
from decorator import decorator
# ..
from twisted.internet import defer


SEPERATOR = '.'
# ...
JSON_SIG = '_json_sig'
JSON_ARGS = '_json_args'
JSON_ARGS_DEFAULTS = '_json_args_defaults'
# ..
INVARIANTA = (b'self',b'request')

class Router(object):

    def __init__(self, ns=None):
        self.ns = self._init_ns(ns)

    def _init_ns(self, ns):
        # ..
        result = ''
        # ..
        if ns and isinstance(ns, basestring):
            result = ns
        # ..
        return result
    # ...
    def register(self, direct):
        # ..
        for n, m in inspect.getmembers(self, inspect.ismethod):
            # ...
            json_sig = getattr(m, JSON_SIG, None)
            if json_sig:
                name = '{}{}{}'.format(self.ns, SEPERATOR, json_sig)
                args = getattr(m, JSON_ARGS)
                args_defaults = getattr(m, JSON_ARGS_DEFAULTS)
                # ..
                direct.register(m, name, args, args_defaults)




def _conspect_name(func, name):
    setattr(func, JSON_SIG, name)

def _conspect_param(func_to, func_from):
    inv = INVARIANTA
    args = filter(lambda x: not x in inv, inspect.getargspec(func_from).args)
    setattr(func_to, JSON_ARGS, args)  

def _conspect_param_defaults(func_to, func_from):
    # ..
    result = {}
    defaults = inspect.getargspec(func_from).defaults    
    if defaults:
        # ..
        args = inspect.getargspec(func_from).args    
        # ..
        defaults_enum = list(enumerate(defaults))
        defaults_length = len(defaults_enum)
        result = dict((args[-defaults_length + id],value) 
            for id, value in defaults_enum)
    # ...
    setattr(func_to, JSON_ARGS_DEFAULTS, result)  

# ...
# ...
# ...
def method(name):
    def decorator(func):
        # ...
        _conspect_name(func, name)
        _conspect_param(func,func)
        # ...
        return func
    return decorator


# ...
# ...
# ...
@decorator
def inlineCallbacks(f,*args, **kwargs):
    # ...
    try:
        gen = f(*args, **kwargs)
    except defer._DefGen_Return:
        raise TypeError(
            "inlineCallbacks requires %r to produce a generator; instead"
            "caught returnValue being used in a non-generator" % (f,))
    if not isinstance(gen, types.GeneratorType):
        raise TypeError(
            "inlineCallbacks requires %r to produce a generator; "
            "instead got %r" % (f, gen))
    return defer._inlineCallbacks(None, gen, defer.Deferred())


# ...
# ...
# ...
def as_view(path):
    def decorator(func):
        # ..
        path_name, klass_name  = (path.split(':'))
        # ...
        @inlineCallbacks
        def wrapper(router, request, *args, **kwargs):
            # ...
            module = importlib.import_module(path_name)
            Klass = getattr(module,klass_name)
            klass = Klass(router, request,*args, **kwargs)
            # ..
            result = yield defer.maybeDeferred(klass)            
            defer.returnValue(result)
        # ..
        # _conspect_name(wrapper, klass_name)
        _conspect_name(wrapper, func.__name__)        
        _conspect_param(wrapper, func)
        _conspect_param_defaults(wrapper, func)        
        return wrapper
    return decorator        


