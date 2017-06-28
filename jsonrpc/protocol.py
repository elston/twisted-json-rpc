# -*- coding: utf-8 -*-
import traceback
import json

# ..
from twisted._version import __version__ as version
from twisted.internet import reactor, defer
from twisted.web import http

# ...
import errors


class JSONRPCRequestHandler(http.Request):
    # .
    def __init__(self, *args, **kwargs):
        http.Request.__init__(self,*args, **kwargs)
        # ...
        self.direct = self.channel.direct

    @defer.inlineCallbacks
    def process(self):
        # ...
        # ..1. get result
        try:
            result = yield self.direct.call(self)
        # ...
        except Exception as e:
            # ...
            if isinstance(e,errors.JSONRPCError):
                result  = e.dumps()
            else:
                result  = errors.OtherError(e).dumps()    
            # ...
            status = result.get('status',http.INTERNAL_SERVER_ERROR)
            self.setResponseCode(status)

        # ..2. get response
        response = yield self.direct.response(result)

       

        # ..3. headers
        self.setHeader(b'server', version)
        self.setHeader(b'date', http.datetimeToString())
        self.setHeader(b'content-type', 'application/json')
        self.setHeader(b'content-length', len(response))

        # ...4. finish
        self.write(response)
        self.finish()

class JSONRPCServerProtocol(http.HTTPChannel):
    # ..
    requestFactory = JSONRPCRequestHandler        

    def __init__(self, direct):
        http.HTTPChannel.__init__(self)
        # ..
        self.direct = direct
