from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError

class BadRequestError(APIException):
    status_code = 400
    default_detail = 'Bad Request'
    default_code = 'bad_request'