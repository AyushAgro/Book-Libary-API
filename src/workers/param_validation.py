import re

from src.config import config, log_and_notify
from src.utils import exceptions

email_regex_pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")

# Minimum eight characters, at least one letter, one number and one special character:
password_regex_pattern = re.compile(
    "^(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")


def convert_str_to_dtype(param_dtype):
    if param_dtype == 'str':
        return str
    elif param_dtype == 'int':
        return int
    elif param_dtype == 'float':
        return float
    elif param_dtype == 'dict':
        return dict
    elif param_dtype == 'int_or_str':
        return [int, str]
    elif param_dtype == 'int_or_float':
        return [int, float]
    else:
        return None


def handle_params(**kwargs):
    log_and_notify.info(f'Checking Mandatory Param with {kwargs}')
    allowed_params = kwargs.get('values')
    param_checked = set()
    api_params = kwargs.get('api_params', {})
    for param_key, single_param_config in allowed_params.items():
        param_name = single_param_config.get('param_name')
        param_dtype = single_param_config.get('param_dtype')
        param_python_dtype = convert_str_to_dtype(param_dtype)
        param_validatin_function = single_param_config.get(
            'param_validation_function')
        param_value = api_params.get(param_name)
        # Param Not Present
        if param_name not in api_params:
            raise exceptions.MissingParam(param_name)
        # Invalid Data Type
        if isinstance(param_python_dtype, list):
            is_type_allowed = any([
                isinstance(param_value, single_dtype)
                for single_dtype in param_python_dtype
            ])
        else:
            is_type_allowed = isinstance(param_value, param_python_dtype)
        if not is_type_allowed:
            msg = f'Param {param_name} allowed data type is {param_dtype} but passed data type is {type(param_value).__name__}'
            raise exceptions.InvalidParamDatatype(msg)
        else:
            param_checked.add(param_name)
            validation_function_kwargs = single_param_config.copy()
            validation_function_kwargs['param_value'] = param_value
            globals()[param_validatin_function](**validation_function_kwargs)
    param_left = {}
    for key, value in api_params.items():
        if key not in param_checked:
            param_left[key] = value
    return param_left


# handle all optional params
def handle_optional_params(**kwargs):
    log_and_notify.info(f'Checking Optional Param with {kwargs}')
    allowed_params = kwargs.get('values', {})
    api_params = kwargs.get('api_params', {})
    param_checked = set()
    for params_key, single_param_config in allowed_params.items():
        if params_key in api_params:
            param_name = single_param_config.get('param_name')
            param_dtype = single_param_config.get('param_dtype')
            param_python_dtype = convert_str_to_dtype(param_dtype)
            param_validatin_function = single_param_config.get(
                'param_validation_function')
            param_value = api_params.get(param_name)
            # Invalid Data Type
            # Invalid Data Type
            if isinstance(param_python_dtype, list):
                is_type_allowed = any([
                    isinstance(param_value, single_dtype)
                    for single_dtype in param_python_dtype
                ])
            else:
                is_type_allowed = isinstance(param_value, param_python_dtype)
            if not is_type_allowed:
                msg = f'Param {param_name} allowed data type is {param_dtype} but passed data type is {type(param_value)}'
                raise exceptions.InvalidParamDatatype(msg)
            param_checked.add(params_key)
            validation_function_kwargs = single_param_config.copy()

            validation_function_kwargs['param_value'] = param_value
            globals()[param_validatin_function](**validation_function_kwargs)
    param_left = {}
    for key, value in api_params.items():
        if key not in param_checked:
            param_left[key] = value
    return param_left


# Check if the param value is valid string
def check_string(**kwargs):
    param_value = str(kwargs.get('param_value'))
    param_name = kwargs.get('param_name')
    param_value = param_value.replace(' ', '')
    if param_value == '':
        raise exceptions.ParamException(
            f"Invalid Param value {param_value} for {param_name}, the parameter can't be empty string"
        )


def check_year(**kwargs):
    param_value = kwargs.get('param_value')
    param_name = kwargs.get('param_name')
    if not isinstance(param_value, int):
        raise exceptions.ParamException(
            f'Param {param_name} expected integer value but passed {type(param_value)}'
        )
    if len(str(param_value)) != 4:
        raise exceptions.ParamException(
            f'Param {param_name} expected year format is YYYYY')


def check_email(**kwargs):
    param_value = kwargs.get('param_value')
    if not re.match(email_regex_pattern, param_value):
        raise exceptions.ParamException(
            f'Not a valid email address {param_value}')


def check_register_password(**kwargs):
    param_value = kwargs.get('param_value')
    if not re.match(password_regex_pattern, param_value):
        raise exceptions.ParamException(
            'Minimum Password length Must be 8 character, contain one letter, one number and one special character'
        )


def check_login_password(**kwargs):
    pass


def check_param(**kwargs):
    pass


# Currently, no check for username
def check_decimal(**kwargs):
    pass


# to check true and false
def check_int(**kwargs):
    param_value = kwargs.get('param_value')
    if param_value < 0:
        raise exceptions.ParamException(
            f"Only Positive Interger Value are allowed for the param {kwargs.get('param_name')}"
        )


def check_tags(**kwargs):
    pass


def check_filter_operation(**kwargs):
    param_value = kwargs.get('param_value').lower()
    if param_value not in ['or', 'and']:
        raise exceptions.ParamException(
            f"Filter operation param accept only value ['OR', 'AND'], but value passes is {param_value}, default value is AND"
        )
