from rest_framework.exceptions import APIException

class CustomModelAlreadyExistError(APIException):
    status_code = 404
    dafault_detail =  'already exist cocktail, please change name'
    dafuult_code = 'already exist'