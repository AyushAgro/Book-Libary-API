from .base_class import BaseExceptionHandler


class LibraryAPIBaseException(BaseExceptionHandler):
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        self.staus_code = 400


class UnknownFeatures(LibraryAPIBaseException):
    def __init__(self, unknown_features, existing_features, **kwargs):
        super().__init__(**kwargs)
        self.status_code = 400
        self.msg = f"Unknown features>> {unknown_features}.             " \
                   f" Allowed features>> {existing_features}"


class ParamException(LibraryAPIBaseException):
    def __init__(self, msg, **kwargs):
        # 406 Not Acceptable
        super().__init__(msg, **kwargs)
        self.status_code = 406
        self.msg = msg


class InvalidJson(ParamException):
    def __init__(self, msg='', **kwargs):
        super().__init__(msg, **kwargs)
        self.msg = "Invalid Json format. Kindly recheck"


class MissingParam(ParamException):
    def __init__(self, param, msg='', **kwargs):
        super().__init__(msg, **kwargs)
        self.msg = f'Following param are Missing for your request: {param}'


class ExtraParam(ParamException):
    def __init__(self, param='', msg='', **kwargs):
        super().__init__(msg, **kwargs)
        self.msg = f'Following param are given but are not allowed: {param}'


class OnlyOneParamAllowed(ParamException):
    def __init__(self, param):
        self.msg = f'Only one param can be present in request {param}'


class MissingOneMandatoryParam(ParamException):
    def __init__(self, params):
        self.msg = f'Any one of the following param must be passed {params[0]} or {params[1]}'


class InvalidParamDatatype(ParamException):
    def __init__(self, msg):
        self.msg = msg


class DatabaseException(LibraryAPIBaseException):
    def __init__(self, msg='', **kwargs):
        self.status_code = 200
        self.msg = msg


class EndpointNotFound(LibraryAPIBaseException):
    def __init__(self, msg='', **kwargs):
        self.status_code = 404
        self.msg = msg


class EndPointNotActive(LibraryAPIBaseException):
    def __init__(self, name):
        self.status_code = 404
        self.msg = f'Endpoint {name} is not Active right now '


class BookNotFoundException(LibraryAPIBaseException):
    def __init__(self, book_id):
        self.staus_code = 404
        self.msg = f'Book with id {book_id} is not present in library database'


class OrderCheckoutException(LibraryAPIBaseException):
    def __init__(self):
        self.msg = 'Error occrred while placing order, please try after some time.'


class CategoryNameNotFoundException(LibraryAPIBaseException):
    def __init__(self, category_name, *args, **kwargs):
        self.staus_code = 404
        self.msg = f'Category with name {category_name} is not present'


class CategoryIndexNotFound(CategoryNameNotFoundException):
    def __init__(self, category_idx):
        self.msg = f'Category with id {category_idx} is not present'


class EmailAlreadyExists(LibraryAPIBaseException):
    def __init__(self, email_address):
        self.staus_code = 400
        self.msg = f'User with email address {email_address} already existed , please try different email address'
    pass
