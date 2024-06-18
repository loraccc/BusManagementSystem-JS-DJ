from cgitb import handler
import pdb
from re import L
from rest_framework.views import exception_handler
from http import HTTPStatus
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError, APIException
from django.db import DatabaseError


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    http_code_to_message= None
   
    # Now add the HTTP status code to the response.
    if response is not None:
        #errors = []
        #for msg in response.data.values():
             #errors.append({'message': msg[0]})
        http_code_to_message = {v.value: v.description for v in HTTPStatus}
        response.data['status_code'] = response.status_code
    """  else:
        from rest_framework import status
        from rest_framework.response import Response
        response = Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) """

    
    handlers = {
        'ValidationError':_handel_generic_error,
        'Http404':_handel_generic_error,
        'PermissionDenied':_handel_generic_error,
        'NotAuthenticated': _handel_authentication_error,
        'InvalidToken': _handel_invalid_error,
        'AuthenticationFailed': _handel_invalid_error,
        'APIException': _handel_apiexception_error,
        'DatabaseError': _handel_databse_error,
        'UnauthorizedAPIException': _handel_apiexception_error,
        'ConflictAPIException':  _handel_apiexception_error,
    }

    exception_class= exc.__class__.__name__
    
    if exception_class in handlers:
        
        if isinstance(exc, InvalidToken):
            http_code_to_message = response.data["detail"]
            return handlers[exception_class](exc, context, response, http_code_to_message)
        
        if isinstance(exc, AuthenticationFailed):
            http_code_to_message = response.data["detail"]
            return handlers[exception_class](exc, context, response, http_code_to_message)

        if isinstance(exc, ValidationError):
            #http_code_to_message = response.data["validation_error"][0].title()
            #return handlers[exception_class](exc, context, response, http_code_to_message)
            for field, errors in exc.detail.items():
                http_code_to_message = str(errors[0])
                return handlers[exception_class](exc, context, response, http_code_to_message)

        if isinstance(exc, APIException):
            http_code_to_message = response.data["detail"].title()
            return handlers[exception_class](exc, context, response, http_code_to_message)
        
         
        if isinstance(exc, DatabaseError):
            #import pdb
            #pdb.set_trace()
            if response is not None:
                http_code_to_message = response.data["detail"]
            else:
                http_code_to_message ='Unknown Error.'

            return handlers[exception_class](exc, context, response, http_code_to_message)
            
           
        return handlers[exception_class](exc, context, response, http_code_to_message)
    
    return response

def _handel_generic_error(exc, context, response, http_code_to_message):
    response.data = {
        'status': 'error',
        'status_code': response.status_code,
        'message': http_code_to_message,
    }
    return response


def _handel_authentication_error(exc, context, response, http_code_to_message):

    message =None
    if http_code_to_message:
        if type(http_code_to_message) == str:
            message = http_code_to_message
        elif  http_code_to_message[response.status_code]:
            message= http_code_to_message[response.status_code]

    response.data = {
        'status': 'error',
        'status_code': response.status_code,
        'message': message,
    }
    return response

def _handel_invalid_error(exc, context, response, http_code_to_message):
   
    response.data = {
        'status': 'error',
        'status_code': response.status_code,
        'message': http_code_to_message,
    }
    return response

def _handel_apiexception_error(exc, context, response, http_code_to_message):
    response.data = {
        'status': 'error',
        'status_code': response.status_code,
        'message': http_code_to_message,
    }
   
    return response

def _handel_databse_error(exc, context, response, http_code_to_message):
   
    if response:
        response.data = {
            'status': 'error',
            'status_code': response.status_code,
            'message': http_code_to_message,
        }
        
    return response
