from .base_class import BaseExceptionHandler


class AuthenticationBaseException(BaseExceptionHandler):
    def __init__(self, msg=None):
        self.msg = msg or f'Please login first'
        self.staus_code = 401


class UnsupportedAuthorizationException(AuthenticationBaseException):
    """Raised when the authorization is unsupported"""

    def __init__(self, authorization_method):
        self.msg = "{} authorization not supported".format(
            authorization_method)


class MissingAuthorizationException(AuthenticationBaseException):
    """Raised when the authorization is missing"""

    def __init__(self):
        self.msg = "Currently no user is logged in, " \
                   "please authorize either through login or token " \
                   "and retry hitting the endpoint"


class CorruptAuthorizationException(AuthenticationBaseException):
    """Raised when the authorization is corrupt"""

    def __init__(self):
        self.msg = "Authorization header corrupt"


class FailedAuthorizationException(AuthenticationBaseException):
    """Raised when the authorization fails"""

    def __init__(self, username):
        self.msg = "Authorization failed for user {}".format(username)


class UnknownUserException(AuthenticationBaseException):
    """Raised when the username is unknown"""

    def __init__(self, email_address):
        self.msg = f'User with email address {email_address} is not present, please check your email address'


class UnknownUserTypeException(AuthenticationBaseException):
    """Raised when the user type is unknown"""

    def __init__(self, user_type):
        self.msg = "User type {} unknown".format(user_type)


class HandlerTypeNotAllowed(AuthenticationBaseException):
    """Raised when the given user type is not allowed the handler type"""

    def __init__(self, user_type, handler_type):
        self.msg = "Handler type {} not allowed for user type {}".format(
            handler_type, user_type)


class AdminRestrictedEndpointException(AuthenticationBaseException):
    def __init__(self, msg=None):
        self.msg = msg or f'The endpoint is admin restricted.'
        self.staus_code = 401


class UserLoggedInException(AuthenticationBaseException):
    def __init__(self, email=None):
        self.msg = f'Currently user with email {email} is logged in, please logout and re-hit the endpoint'
        self.staus_code = 401
