import os
from flask import Blueprint
from main import app

blueprint = Blueprint('error', __name__)

# error handler
def error_decorator(func):
    def wrap(*args, **kwargs):
        error = args[0]
        print('-------------------------------')
        print('----Exception TYPE:', type(error.description).__name__)
        print('----Exception TYPE:', dir(error.description))
        print('-------------------------------')
        if type(error.description) == str:
            error.description = {'message': error.description}
        elif isinstance(error.description, SQLAlchemyError) or isinstance(error.description, HTTPException):
            error.description = {'message': str(error.description)}
        elif isinstance(error, BaseException):
            error.description = {'message': str(error.description)}
        return func(*args, **kwargs)
    return wrap


@blueprint.errorhandler(500)
@error_decorator
def server_error(error):
    message = error.description if app.debug == True else {
        "message": "Internal server error"}
    return message, error.code


@blueprint.errorhandler(400)
@error_decorator
def bad_request(error):
    message = error.description if app.debug == True else {
        "message": "Bad request"}
    return message, error.code


@blueprint.errorhandler(404)
@error_decorator
def not_found(error):
    message = error.description if app.debug == True else {
        "message": "Resource not found"}
    return message, error.code


@blueprint.errorhandler(422)
@error_decorator
def unprocessable_entity(error):
    message = error.description if app.debug == True else {
        "message": "Cannot process this request"}
    return message, error.code
