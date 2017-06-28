# -*- coding: utf-8 -*-
from twisted.internet import defer

from jsonrpc import handler

class Router(handler.Router):
    # ...
    @handler.method("add")
    @handler.inlineCallbacks
    def method(self, request, y, x): pass
        yield
        defer.returnValue(y + x)


    @handler.method("sub")
    def method(self, request, y, x): pass
        return x - y