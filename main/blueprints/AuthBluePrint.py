from flask import Blueprint, request, abort, g

from main import jwt, app, User, db
from main.helpers.token import gen_token, check_available_token
from main.helpers.common import only_keys
from main.validators.UserValidators import register_validator
from sqlalchemy import or_, and_, not_
import datetime
blueprint = Blueprint('auth', __name__)

def check_is_login(message = None):
    fail_message = {'message': message if message else 'token invalid'}
    try:
        bearer = request.headers.get('token', None)
        if not bearer:
            return fail_message, 400
        
        token = bearer.split('Bearer ')[1]

        payload = check_available_token(token)

        if payload is None:
            return fail_message, 400
            
        username = payload.get('username', None)
        user_id = payload.get('id', None)

        if not username and not user_id:
            return fail_message, 400

        # get user
        user = User.query.filter_by(id=user_id, username=username).first()
        if user is None:
            return fail_message, 400
        
        # store in global context
        g.user = user
        return {'user': user.to_json(except_keys=['orders'])} ,200
    except Exception as e:
        return fail_message, 500

# decorator
def login_required(only=[]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(only) == 0 or request.method in only:
                result = check_is_login("need login")
                if 200 in result: 
                    return func(*args, **kwargs)
                else: 
                    return result
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator


@blueprint.route('/login', methods=['POST'])
def login():
    fail_message = {'message': 'invalid login'}
    try:
        body = request.get_json()
        username = body.get('username', None)
        password = body.get('password', None)
        if not username or not password:
            return fail_message, 400

        user = User.query.filter_by(username=username).first()
        # check user & verify password
        if user is None or not user.verify_password(password):
            return fail_message, 400

        # generate token
        payload = {'username': user.username, 'id': user.id}
        token = gen_token(payload=payload)

        # update user
        user.logined_at = datetime.datetime.utcnow()
        db.session.commit()
        return {'user': {**(user.to_json(except_keys=['orders'])), 'token': token}}, 200
    except Exception as e:
        abort(500, e)


@blueprint.route('/is_login')
def is_login():
    return check_is_login()


@blueprint.route('/register', methods=['POST'])
@register_validator(only=['POST'])
def register():
    try: 
        data = request.get_json()
        insert_data = only_keys(data, 'username', 'password')
        user = User(**insert_data)
        db.session.add(user)
        db.session.commit()
        return {'user': user.to_json()}, 200
    except Exception as e:
        return {'message': str(e)}, 400