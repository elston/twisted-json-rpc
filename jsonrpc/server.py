# -*- coding: utf-8 -*-
from twisted.web import http
import protocol
import direct

class BaseServerFactory(http.HTTPFactory):
    # ...
    def __init__(self):
        http.HTTPFactory.__init__(self)
        # ...
        self.direct = direct.JSONRPCDirect()
    # ...
    def buildProtocol(self, addr):
        return self.protocol(self.direct)        

    def registerRouter(self, router):
        router.register(self.direct)


class JSONRPCServerFactory(BaseServerFactory):
    protocol = protocol.JSONRPCServerProtocol