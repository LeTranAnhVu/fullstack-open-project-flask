from flask import request
from main.validators import Validator
from main import User


def register_validator(only=[]):
    def decorator(func):
        def wrap(*args, **kwargs):
            if request.method in only:
                # do something
                data = request.get_json()
                username = data.get('username', '')
                password = data.get('password', '')
                confirm_password = data.get('confirm_password', '')
                username_validator = Validator(name='username')._required(username)._unique(username,
                                                                                            User)._special_character_validator(
                    username)._minlen(username, 8)._maxlen(username, 10)
                errors = {}
                if username_validator.errors:
                    errors['username'] = username_validator.errors

                password_validator = Validator(name='password')._required(password)._minlen(password, 4)._maxlen(
                    password, 10)
                if password_validator.errors:
                    errors['password'] = password_validator.errors

                confirm_password_validator = Validator(name='confirm_password')._required(confirm_password)._minlen(
                    confirm_password, 4)._maxlen(password, 10)
                if confirm_password_validator.errors:
                    errors['confirm_password'] = confirm_password_validator.errors

                confirm_password_validator = Validator(name=None)._confirm_password_validator(password,
                                                                                              confirm_password)
                if confirm_password_validator.errors:
                    errors['password'] = confirm_password_validator.errors

                if errors:
                    return {'errors': errors}, 400
            return func(*args, **kwargs)

        # Renaming the function name:
        wrap.__name__ = func.__name__
        return wrap

    return decorator


def register_username_validator(only=[]):
    def decorator(func):
        def wrap(*args, **kwargs):
            if request.method in only:
                # do something
                data = request.get_json()
                username = data.get('username', None)
                username_validator = Validator(name='username')._unique(
                    username, User)._special_character_validator(username)._minlen(username, 8)._maxlen(username, 10)
                errors = {}
                if username_validator.errors:
                    errors['username'] = username_validator.errors
                if errors:
                    return {'errors': errors}, 400
            return func(*args, **kwargs)

        # Renaming the function name:
        wrap.__name__ = func.__name__
        return wrap

    return decorator
