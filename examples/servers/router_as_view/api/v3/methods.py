# -*- coding: utf-8 -*-
from twisted.internet import defer
from jsonrpc import errors

class Add(object):

    # ...
    def __init__(self, request, *args, **kwargs):
        self.x = kwargs['x']
        self.y = kwargs['y']

    def __call__(self):
        # raise errors.ParseError()
        return self.x + self.y



class Sub(object):

    # ...
    def __init__(self, request, *args, **kwargs):
        self.x = kwargs['x']
        self.y = kwargs['y']

    @defer.inlineCallbacks
    def __call__(self):
        yield
        # raise errors.ParseError()
        defer.returnValue(self.x - self.y)
