from flask import request
from main.validators import Validator
from main import User


def register_validator(only=[]):
    def decorator(func):
        def wrap(*args, **kwargs):
            if request.method in only:
                # do something
                data = request.get_json()
                username = data.get('username', None)
                password = data.get('password', None)
                confirm_password = data.get('confirm_password', None)
                username_validator = Validator(name='username')._unique(
                    username, User)._special_character_validator(username)._minlen(username, 8)._maxlen(username, 10)
                errors = {}
                if username_validator.errors:
                    errors['username'] = username_validator.errors

                confirm_password_validator = Validator(
                    name=None)._confirm_password_validator(password, confirm_password)
                if confirm_password_validator.errors:
                    errors['password'] = confirm_password_validator.errors

                if errors:
                    return {'errors': errors}, 400
            return func(*args, **kwargs)
        return wrap
    return decorator
