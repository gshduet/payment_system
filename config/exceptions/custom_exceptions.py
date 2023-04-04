from rest_framework import exceptions


class CustomDictException(exceptions.APIException):
    status_code = 200
    default_detail = 'UNKNOWN_ERROR'
    default_code = 'UNKNOWN_ERROR'

    def __str__(self):
        return str(self.detail)
    

class DuplicateEmailError(exceptions.ValidationError):
    def __init__(self, message):
        super().__init__(message)
        self.code = 'duplicate_email'