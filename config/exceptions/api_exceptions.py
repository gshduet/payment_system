from rest_framework import exceptions
from rest_framework.views import exception_handler
from rest_framework.response import Response

from config.exceptions.exception_codes import STATUS_RSP_INTERNAL_ERROR
from config.exceptions import custom_exceptions


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_dict = {}

        if isinstance(exc, exceptions.ParseError):
            error_dict['code'] = response.status_code
            error_dict['message'] = exc.detail

        elif isinstance(exc, exceptions.AuthenticationFailed):
            error_dict['code'] = response.status_code
            error_dict['message'] = exc.get_full_details()
            del error_dict['message']['code']

        elif isinstance(exc, exceptions.NotAuthenticated):
            error_dict['code'] = response.status_code
            error_dict['message'] = exc.get_full_details()
            del error_dict['message']['code']

        elif isinstance(exc, exceptions.PermissionDenied):
            error_dict['code'] = response.status_code
            error_dict['message'] = exc.detail

        elif isinstance(exc, exceptions.NotFound):
            error_dict['code'] = response.status_code
            error_dict['message'] = exc.detail

        elif isinstance(exc, exceptions.MethodNotAllowed):
            error_dict['code'] = response.status_code
            error_dict['message'] = exc.detail

        elif isinstance(exc, exceptions.NotAcceptable):
            error_dict['code'] = response.status_code
            error_dict['message'] = exc.detail

        elif isinstance(exc, exceptions.UnsupportedMediaType):
            error_dict['code'] = response.status_code
            error_dict['message'] = exc.detail

        elif isinstance(exc, exceptions.Throttled):
            error_dict['code'] = response.status_code
            error_dict['message'] = exc.detail

        elif isinstance(exc, exceptions.ValidationError):
            error_dict['code'] = response.status_code
            error_dict['message'] = exc.detail

        elif isinstance(exc, custom_exceptions.CustomDictException):
            error_dict['code'] = exc.detail.get('code')
            error_dict['message'] = exc.detail.get('default_message')

        else:
            error_dict['code'] = response.status_code
            error_dict['message'] = 'UNKNOWN_ERROR'

        response.status_code = exc.status_code
        response.data = {
            'code': error_dict['code'],
            'message': error_dict['message'],
        }

        return response

    else:
        error_dict = STATUS_RSP_INTERNAL_ERROR.copy()
        error_dict['message'] = error_dict.pop('default_message', None)
        error_dict.pop('lang_message', None)

        return Response(error_dict, status=200)
