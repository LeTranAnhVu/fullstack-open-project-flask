from flask import Blueprint, request, abort

from main import jwt, app, User, db
from sqlalchemy import or_, and_, not_
import datetime
blueprint = Blueprint('auth', __name__)

def _gen_token(payload={}, minutes=60):
    now = datetime.datetime.utcnow()
    expired_at = now + datetime.timedelta(minutes=minutes)
    expired_at = expired_at.strftime(app.config['DATETIME_FORMAT'])

    token = jwt.encode({**payload, 'expired_at': expired_at}, app.config['SALT']).decode('utf-8')
    return token

def _check_available_token(token):
    payload = jwt.decode(token, app.config['SALT'])
    expired_at = payload.get('expired_at', None)
    if not expired_at: 
        return None
    expired_at = datetime.datetime.strptime(expired_at, app.config['DATETIME_FORMAT'])

    now = datetime.datetime.utcnow()

    if now >= expired_at : # out of date
        return None

    # token till available
    return payload

def check_is_login(message = None):
    fail_message = {'message': message if message else 'token invalid'}
    try:
        bearer = request.headers.get('token', None)
        if not bearer:
            return fail_message, 400
        
        token = bearer.split('Bearer ')[1]

        payload = _check_available_token(token)

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
        return {'user': user.to_json(except_keys=['orders'])} ,200
    except Exception as e:
        return fail_message, 500


def login_required(only=[]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('++++++++++++++', request.method)
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
        token = _gen_token(payload=payload)

        # update user
        user.logined_at = datetime.datetime.utcnow()
        db.session.commit()
        return {'user': {**(user.to_json(except_keys=['orders'])), 'token': token}}, 200
    except Exception as e:
        abort(500, e)


@blueprint.route('/is_login')
def is_login():
    return check_is_login()