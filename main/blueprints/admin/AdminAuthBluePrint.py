from flask import Blueprint, request, abort, g

from main import jwt, app, Admin, db
from main.helpers.token import gen_token, check_available_token
from sqlalchemy import or_, and_, not_
import datetime
blueprint = Blueprint('admin_auth', __name__)


def check_admin_is_login(message = None):
    fail_message = {'message': message if message else 'token invalid'}
    try:
        bearer = request.headers.get('token', None)
        if not bearer:
            return fail_message, 401
        
        token = bearer.split('Bearer ')[1]

        payload = check_available_token(token)

        if payload is None:
            return fail_message, 401
            
        username = payload.get('username', None)
        admin_id = payload.get('id', None)

        if not username and not admin_id:
            return fail_message, 401

        # get admin
        admin = Admin.query.filter_by(id=admin_id, username=username).first()
        if admin is None:
            return fail_message, 401
        
        # store in global context
        g.admin = admin
        return {'admin': admin.to_json(except_keys=[])} ,200
    except Exception as e:
        return fail_message, 500


def admin_login_required(only=[]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(only) == 0 or request.method in only:
                result = check_admin_is_login("admin need login")
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

        admin = Admin.query.filter_by(username=username).first()
        # check admin & verify password
        if admin is None or not admin.verify_password(password):
            return fail_message, 400

        # generate token
        payload = {'username': admin.username, 'id': admin.id}
        token = gen_token(payload=payload)

        # update admin
        admin.logined_at = datetime.datetime.utcnow()
        db.session.commit()
        return {'user': {**(admin.to_json(except_keys=['orders'])), 'token': token}}, 200
    except Exception as e:
        abort(500, e)

@blueprint.route('/is_login')
def is_login():
    return check_admin_is_login()