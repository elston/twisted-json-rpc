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
# ..
INVARIANTA = (b'self',b'request')

class Router(object):

    def __init__(self, ns=None):
        self.ns = self._init_ns(ns)

    def _init_ns(self,ns):
        # ..
        result = []
        # ..
        if ns and isinstance(ns, basestring):
            result = [ns]
        # ..
        return result
    # ...
    def register(self, direct):
        # ..
        for n, m in inspect.getmembers(self, inspect.ismethod):
            # ...
            json_sig = getattr(m, JSON_SIG, None)
            if json_sig:
                self.ns.append(json_sig)
                name = SEPERATOR.join(self.ns)
                params = getattr(m, JSON_ARGS)
                # ..
                direct.register(m, name, params)




def _conspect_name(func, name):
    setattr(func, JSON_SIG, name)

def _conspect_param(func_to,func_from):
    inv = INVARIANTA
    args = filter(lambda x: not x in inv, inspect.getargspec(func_from).args)
    setattr(func_to, JSON_ARGS, args)  
                  
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
            klass = Klass(request,*args, **kwargs)
            # ..
            result = yield defer.maybeDeferred(klass)            
            defer.returnValue(result)
        # ..
        _conspect_name(wrapper, klass_name)        
        _conspect_param(wrapper, func)
        return wrapper
    return decorator        


