from rest_framework.exceptions import APIException


class ValidationErrorException(APIException):
    status_code = 400
    default_detail = "Validation error occurred"
    default_code = "validation_error"
