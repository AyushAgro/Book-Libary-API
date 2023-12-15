class BaseExceptionHandler(Exception, BaseException):

    def __init__(self, msg, status_code=401, **kwargs):
        self.msg = msg
        self.staus_code = status_code

    def __str__(self):
        return self.msg