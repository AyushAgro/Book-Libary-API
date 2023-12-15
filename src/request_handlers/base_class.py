import base64
import datetime
import json
import time
from abc import ABC

import tracebackturbo as traceback
from src.config import config, log_and_notify
from src.utils import User, exceptions, methods, users_table
from src.workers import handle_optional_params, handle_params
# import traceback
from tornado.web import HTTPError, RequestHandler

ApiEndpoints = config['ApiEndpoints']


class LibraryRequestHandler(RequestHandler, ABC):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.param = {}
        self.user_data = User()

    def write_error(self, status_code: int, **kwargs):
        if "exc_info" in kwargs:
            try:
                exception = kwargs.get('exc_info')[1]
                self.handle_exception(exception)
            except HTTPError as err:
                self.set_status(err.status_code)
                self._reason = err.reason
            except Exception:
                self.set_status(500)
                self._reason = "Internal server error"
            if self.settings.get("serve_traceback"):
                # in debug mode, try to send a traceback
                self.set_header("Content-Type", "text/plain")
                for line in traceback.format_exception(*kwargs["exc_info"]):
                    self.write(line)
            self.finish()
        else:
            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(code)d: %(message)s</body></html>" % {
                            "code": status_code,
                            "message": self._reason
                        })

    # handling all exception class of requests
    def handle_exception(self, exec):
        if isinstance(exec, exceptions.DatabaseException):
            status_code = getattr(exec, 'status_code', 400)
            self.raise_error(exec.msg, status_code)

        elif isinstance(exec, exceptions.LibraryAPIBaseException):
            status_code = getattr(exec, 'status_code', 400)
            self.raise_error(exec.msg, status_code)

        elif isinstance(exec, exceptions.AuthenticationBaseException):
            status_code = getattr(exec, 'status_code', 401)
            self.raise_error(exec.msg, status_code)
        elif isinstance(exec, HTTPError):
            raise
        else:
            log_and_notify.exception(
                f"Exception Raised for {self.email} {self.request.arguments}")
            raise

    # raising HTTPError with apt. msg
    def raise_error(self, msg: str, status_code=400):
        if isinstance(msg, set):
            msg = list(msg)
        raise HTTPError(status_code=status_code, reason=json.dumps(msg))

    def return_result(self, result):
        if isinstance(result, set):
            result = list(result)

        if not self._finished:
            self.set_header('Content-Type', 'application/json')
            # unique api id for request
            end_time = time.time()
            processing_time = methods.format_time(self.start_time, end_time)
            api_id = next(unique_sequence)
            final_result = {
                'Request ID': api_id,
                'Processing time': processing_time,
                'api_input_param': self.param,
                'api_output': result
            }
            log_and_notify.info(f'Request :- {final_result}')
            self.finish(json.dumps(final_result, cls=methods.JsonBaseEncoder))

    async def prepare(self):  # Will always called before get or post.
        self.start_time = time.time()
        await self.validate_user_through_cookie()

        authorization_header = self.request.headers.get(
            'Authorization'
        )  # get header and header has Authorization detail..
        if authorization_header is not None and self.user_data.is_user_logged_in(
        ):
            authorization_method, encoded_credentials = authorization_header.split(
                ' ')
            # FUTURE: basic token shall only be exposed to /login
            if authorization_method and 'Basic' in authorization_method:
                await self.validate_user_through_basic_token(
                    encoded_credentials=encoded_credentials)
        # FUTURE: reset cookies every time; user have been logged in
        await self.validate_params()

    async def validate_params(self):
        log_and_notify.info('Starting param valdiation')
        # handle post request
        # Create operation
        if self.request.method == "POST":
            try:
                json_body = self.request.body.decode('utf-8')
                if json_body is not None and json_body != '':
                    api_param = json.loads(json_body)
                else:
                    api_param = {}
            except:
                raise exceptions.InvalidJson()
        else:
            api_param = self.request.arguments
        api_param = await self.process_api_param(**api_param)
        endpoint = '/'.join(self.request.path.split('/')[2:])
        if endpoint not in ApiEndpoints:
            raise exceptions.EndpointNotFound(
                f'Endpoint is not present {endpoint}')

        endpoint_config = ApiEndpoints.get(endpoint, {})
        # to turn off any request set active equal to off
        if not endpoint_config.get('active', True):
            raise exceptions.EndPointNotActive(endpoint)

        allowed_method = endpoint_config.get('METHOD', '')
        if allowed_method != self.request.method:
            self.raise_error(f"Expected {allowed_method} request", 405)

        api_param_copy = api_param.copy()

        await self.pre_check_and_raise_user_permission(endpoint_config)

        # Checking in any extra param is provided
        for param_type, param_details in endpoint_config.get('params',
                                                             {}).items():
            function = param_details.get('function')
            values = param_details.get('values')
            api_param_copy = globals()[function](api_params=api_param_copy,
                                                 values=values)
        if len(api_param_copy) > 0:
            raise exceptions.ExtraParam(
                f'Param {api_param_copy} are not allowed for endpoint')
        self.param = api_param
        log_and_notify.info('Completed Param Check')

    async def process_api_param(self, **api_params):
        log_and_notify.info('Processing raw api praram')
        update_params = {}
        for key, value in api_params.items():
            if isinstance(value, list) or isinstance(value, tuple):

                if len(value) == 1:
                    if isinstance(value[0], bytes):
                        update_params[key] = value[0].decode('utf-8')
                    else:
                        update_params[key] = value[0]
                else:
                    update_params[key] = []
                    for single_value in value:
                        if isinstance(single_value, bytes):
                            update_params[key].append(
                                single_value.decode('utf-8'))
                        else:
                            update_params[key].append(single_value)
            elif isinstance(value, bytes):
                update_params[key] = value.decode('utf-8')
            else:
                update_params[key] = value

            current_value = update_params[key]
            if isinstance(current_value, str):
                if current_value.isnumeric():
                    update_params[key] = int(current_value)
                else:
                    try:
                        update_params[key] = float(current_value)
                    except:
                        pass

        return update_params

    async def validate_user_through_basic_token(self, encoded_credentials,
                                                *args, **kwargs):
        log_and_notify.info('Validating user detail with basic token')

        user_email, user_password = base64.b64decode(
            encoded_credentials).decode('utf8').split(':')
        hashed_password = methods.hash_user_password_using_Sha512(
            password=user_password)
        is_user_present = await users_table.validate_user_email_and_password(
            email=user_email, password=hashed_password)
        if is_user_present:
            await self.fetch_user_data_post_login(user_email)

    async def validate_user_through_cookie(self):
        log_and_notify.info('Validating user detail with cookies')

        user_email = self.get_current_user()
        if user_email:
            self.email = user_email.decode('utf-8')
            await self.fetch_user_data_post_login(self.email)
            self.set_secure_cookie('email', user_email, expires_days=3)

    async def fetch_user_data_post_login(self, user_email, *args, **kwargs):
        user_details = await users_table.fetch_user_details(user_email)
        if len(user_details) > 0:
            self.user_data = user_details[0]
            self.user_data.mark_user_logged_in()

    def get_current_user(self):
        return self.get_secure_cookie("email", max_age_days=3)

    async def pre_check_and_raise_user_permission(self, endpoint_config):
        # to check wheather the user is logged in or not.
        if endpoint_config.get(
                'login_required',
                False) and not self.user_data.is_user_logged_in():
            raise exceptions.MissingAuthorizationException()
        # all create, update, delete endpoint
        if endpoint_config.get('admin_only',
                               False) and not self.user_data.is_user_admin():
            raise exceptions.AdminRestrictedEndpointException()

        # No user should be logged in for login and register endpoint
        if endpoint_config.get('no_user_logged_in',
                               False) and self.user_data.is_user_logged_in():
            raise exceptions.UserLoggedInException(email=self.user_data.email)


unique_sequence = methods.uniqueid()
