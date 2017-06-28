twisted-json-rpc
========================

Description
-----------

Yet another JSON-RPC 2.0 library for Twisted. Unbelievably simple, super fast, extremely lightweight and very extensible!!!


Features
--------

* Only over HTTP

* Only JSON-RPC 2.0 compliant

* Only POST method

* Only root resource

* Without any batch operations for the server (one request - one method  - one response)

* Param only dict

* Fully compliant for names with request param and method param

* Router method may be expanded to Class (like Django as_view)

* Tested for Python 2.7


First release server usage (simple)
------------


1. Define a router and methods:

```python
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

```

As this api then it location such api/v3/routers.py ..for example



2. Define a server:


```python
from twisted.application import service, internet
from twisted.internet import defer
from jsonrpc.server import JSONRPCServerFactory
from api.v3.routers import Router

factory = JSONRPCServerFactory()
factory.registerRouter(Router('v3'))
# ..
application = service.Application("Example JSON-RPC Server")
server = internet.TCPServer(8000, factory)
server.setServiceParent(application)

```

Then run server for example ```twistd -ny app.py```


3. Test request

```bash
curl --data-binary '{
    "jsonrpc": "2.0", 
    "id": "1", 
    "method": "v3.add",
    "params": {
        "x":1,
        "y":3
    }
}' \
-H 'content-type:application/json;' \
${API_URL} \
| python -m json.tool
```

4. Get response

```python
{
    "id": "1",
    "jsonrpc": "2.0",
    "result": 3
}
```

Second release server usage (as_view)
------------


1. Define a class of method:

```python
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
```

And locate it  api/v3/methods.py 



2. Define a router :

```python
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

```

locate it api/v3/routers.py 

3. Define a server:


```python
from twisted.application import service, internet
from twisted.internet import defer
from jsonrpc.server import JSONRPCServerFactory
from api.v3.routers import Router

factory = JSONRPCServerFactory()
factory.registerRouter(Router('v3'))
# ..
application = service.Application("Example JSON-RPC Server")
server = internet.TCPServer(8000, factory)
server.setServiceParent(application)

```

run server ```twistd -ny app.py```


4. Test request

```bash
curl --data-binary '{
    "jsonrpc": "2.0", 
    "id": "1", 
    "method": "v3.add",
    "params": {
        "x":1,
        "y":3
    }
}' \
-H 'content-type:application/json;' \
${API_URL} \
| python -m json.tool
```

5. Get response

```python
{
    "id": "1",
    "jsonrpc": "2.0",
    "result": 3
}
```


Acknowledgment
-------
* [oubiwann/txjsonrpc](https://github.com/oubiwann/txjsonrpc)
* [flowroute/txjason](https://github.com/flowroute/txjason) 
* [NCMI/jsonrpc](https://github.com/NCMI/jsonrpc) 