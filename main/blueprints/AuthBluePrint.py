from flask import Blueprint, request, abort

from main import jwt, app, User, db
from sqlalchemy import or_, and_, not_
import datetime
blueprint = Blueprint('auth', __name__)

def _is_login(message = None):
    fail_message = {'message': message if message else 'token invalid'}
    try:
        bearer = request.headers.get('token', None)
        if not bearer:
            return fail_message, 400
        
        token = bearer.split('Bearer ')[1]

        payload = jwt.decode(token, app.config['SALT'])
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


def login_required(func):
    def wrapper(*args, **kwargs):
        result = _is_login("need login")
        if 200 in result: 
            return func(*args, **kwargs)
        else: 
            return result
    return wrapper


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
        token = jwt.encode(payload, app.config['SALT']).decode('utf-8')

        # update user
        user.logined_at = datetime.datetime.utcnow()
        db.session.commit()
        return {'user': {**(user.to_json(except_keys=['orders'])), 'token': token}}, 200
    except Exception as e:
        abort(500, e)


@blueprint.route('/is_login')
def is_login():
    return _is_login()