# -*- coding: utf-8 -*-
import sys, traceback, json

from twisted.web import http


class ServiceStopped(Exception):
    """
    A request was made of a stopped JSONRPCClientService.
    """


class JSONRPCError(Exception):
    """
    JSONRPCError class based on the JSON-RPC 2.0 specs.
    """

    code = 0
    message = None
    data = None

    def __init__(self, message=None):
        # ...
        if message:
            self.message = message

    def dumps(self):
        # ...basic
        error = {
            'code': self.code,
            'message': str(self.message)
        }

        # ..data
        data = getattr(self,'data', None)
        if data:
            error['data'] = data

        # ..status
        status = getattr(self,'status', None)
        if status:
            error['status'] = status

        # ...debug
        error['stack'] = traceback.format_exc()
        error['executable'] = sys.executable

        # ...
        return {
            'error':error
        }



#==============================================================================
# Exceptions
#
# The error-codes -32768 .. -32000 (inclusive) are reserved for pre-defined
# errors.
#
# Any error-code within this range not defined explicitly below is reserved
# for future use
#==============================================================================

class ParseError(JSONRPCError):
    """Invalid JSON. An error occurred on the server while parsing the JSON
    text."""
    code = -32700
    message = 'Parse error'
    status = http.BAD_REQUEST


class InvalidRequestError(JSONRPCError):
    """The received JSON is not a valid JSON-RPC Request."""
    code = -32600
    message = 'Invalid request'


class MethodNotFoundError(JSONRPCError):
    """The requested remote-procedure does not exist / is not available."""
    code = -32601
    message = 'Method not found'


class InvalidParamsError(JSONRPCError):
    """Invalid method parameters."""
    code = -32602
    message = 'Invalid params'

    def __init__(self, data=None):
        self.data = data


class InternalError(JSONRPCError):
    """Internal JSON-RPC error."""
    code = -32603
    message = 'Internal error'


# -32099..-32000 Server error. Reserved for implementation-defined
# server-errors.
class KeywordError(JSONRPCError):
    """The received JSON-RPC request is trying to use keyword arguments even
    tough its version is 1.0."""
    code = -32099
    message = 'Keyword argument error'


class TimeoutError(JSONRPCError):
    """The request took too long to process."""
    code = -32098
    message = 'Server Timeout'


class ServiceUnavailableError(JSONRPCError):
    """The service is not available (stopServing called)."""
    code = -32097
    message = 'Service Unavailable'


class ServerError(JSONRPCError):
    """Generic server error."""
    code = -32000
    message = 'Server error'




#==============================================================================
# Other Exceptions
#
#==============================================================================
class OtherError(JSONRPCError):
    """ catchall error """
    code = http.INTERNAL_SERVER_ERROR
    message = 'Error missed by other exceptions'
    status = http.INTERNAL_SERVER_ERROR


class NotFoundURLError(JSONRPCError):
    """ catchall error """
    code = http.NOT_FOUND
    message = 'Not FOUND URL'
    status = http.NOT_FOUND    

    
class NotAllowedMethodError(JSONRPCError):
    """ catchall error """
    code = http.NOT_ALLOWED
    message = 'Not Allowed Method'
    status = http.NOT_ALLOWED    


class OperatorError(JSONRPCError):

    code = http.INTERNAL_SERVER_ERROR
    message = 'Error from operator'
    status = http.INTERNAL_SERVER_ERROR

    def __init__(self, data=None):
        self.data = data    