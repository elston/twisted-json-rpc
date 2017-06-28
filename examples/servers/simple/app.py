# -*- coding: utf-8 -*-

from twisted.application import service, internet
from twisted.internet import defer

# ...
from jsonrpc.server import JSONRPCServerFactory
from api.v3.routers import Router


factory = JSONRPCServerFactory()
factory.registerRouter(Router('v3'))
# ..
application = service.Application("Example JSON-RPC Server")
server = internet.TCPServer(8000, factory)
server.setServiceParent(application)