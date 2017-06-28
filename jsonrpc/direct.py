# -*- coding: utf-8 -*-
import inspect
import types
import json

from twisted.application import service
from twisted.internet import defer, reactor
from twisted.python import log

import errors, utils


class JSONRPCDirect(object):
    # ..
    DEFAULT_JSONRPC = b'2.0'
    # .
    RESOURCES = (
        b'/',
    )
    # ..
    ALLOWED_METHODS = (
        b'POST',
    )
    # ..
    REQUIRED_FIELDS = (
        b'id',
        b'jsonrpc',
        b'params',
        b'method',
    )

    RESULT_SIG = 'result'

    # ..
    def __init__(self):
        # ...
        self.methods = {}

    # ...
    # ...
    # ...
    def register(self, method, name, params):
        # ..

        self.methods[name] = {
            'method':method,
            'params':params,            
        }


    # ...
    # ...
    # ...
    @defer.inlineCallbacks
    def response(self,result):
        # ...
        response =  {
            "id": b"1",
            "jsonrpc": self.DEFAULT_JSONRPC
        }
        # ..
        response.update(result)
        response  = yield json.dumps(
            response, 
            cls=utils.JSONRPCEncoder
        )

        # ...
        defer.returnValue(response)


    # ...
    # ...
    # ...
    @defer.inlineCallbacks
    def call(self, request):
        # ...
        self._init_request_resource(request)
        self._init_request_method(request)
        # ...
        request.content.seek(0, 0)
        rdata = yield self._init_json_data(request.content)
        # ...
        params = self._get_params(rdata)
        method = self._get_method(rdata)
        # ..
        result = yield defer.maybeDeferred(method, request, **params)
        result = self._make_result(result)
        # ...
        defer.returnValue(result)


    # ..init
    # ==================================
    def _init_request_resource(self,request):
        # ...
        resources = self.RESOURCES
        if not request.path in resources:
            raise errors.NotFoundURLError()

    def _init_request_method(self,request):
        # ...
        methods = self.ALLOWED_METHODS
        if not request.method in methods:
            raise errors.NotAllowedMethodError()

    @defer.inlineCallbacks        
    def _init_json_data(self,content):
        # ...
        string = yield content.read()
        rdata = yield json.loads(string)

        # ..test dict
        if not isinstance(rdata, dict):
            raise errors.ParseError(
                'Reqest data must be a dict ..list is not allowed yet..'
            )

        # ..test fields 
        if not set(self.REQUIRED_FIELDS) == set(rdata.keys()):
            raise errors.ParseError(
                '"{fields}" are required '
                'fields in Reqest'.format(
                    fields = ', '.join(self.REQUIRED_FIELDS)
                )
            )

        # ..test id
        if not int(rdata['id']) == 1:
            raise errors.ParseError(
                'Eror parse "id" field ..it must be 1'
            )

        # ..test version
        if not rdata['jsonrpc'] == self.DEFAULT_JSONRPC:
            raise errors.ParseError(
                'Eror parse "jsonrpc" field ..it must be "2.0"'
            )

        # ..test method
        # ==================================
        if not isinstance(rdata['method'], basestring) \
            or not len(rdata['method']):
                raise errors.ParseError(
                    '"method" field must be "str" and  not be empty'
                )

        method = self._get_methods_item(rdata)
        if not method:
            raise errors.ParseError(
                'method "{method}" not allowed'.format(
                    method = rdata['method']
                )
            )

        # ..test params
        # ==================================       
        params = rdata['params']
        if not isinstance(params, dict):
            raise errors.ParseError(
                '"params" field must be dict'
            )

        if not set(params.keys()) == set(method['params']):
            errstr = 'params must be empty'
            if len(method['params']):
                errstr = 'params must contain "{params}"'.format(
                    params = ', '.join(method['params'])
                )
            # ..
            raise errors.ParseError(errstr)            
        # ...
        defer.returnValue(rdata)


    # ..get
    # ==================================
    def _get_methods_item(self, rdata):
        return self.methods.get(rdata['method'],None)

    def _get_method(self, rdata):
        item = self.methods.get(rdata['method'])
        return item['method']

    def _get_params(self, rdata):
        return rdata['params']

    # ..make 
    # ==================================

    def _make_result(self,result):
        return {
            'result':result
        }