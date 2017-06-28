# -*- coding: utf-8 -*-

from jsonrpc import handler

class Router(handler.Router):
    # ...
    @handler.as_view('api.v3.methods:Add')
    def method(self, request
        , y
        , x
    ): pass


    # ...
    @handler.as_view('api.v3.methods:Sub')
    def method(self, request
        , y
        , x
    ): pass

