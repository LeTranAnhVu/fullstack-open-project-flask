from flask import Blueprint, request, abort, jsonify
from werkzeug.exceptions import NotFound
from main import app, Admin, db, Role
from main.helpers.pagination import MakePaginate
from main.helpers.common import only_keys
from main.config import URL_CONFIG, RESOURCE_CONFIG

blueprint = Blueprint('manager_admin', __name__)

# ADMIN
@blueprint.route('', methods=['GET', 'POST'])
def admins():
    if request.method == 'GET':
        make_paginate = MakePaginate()
        try:
            keyword = "" if request.args.get(
                'keyword') is None else request.args.get('keyword')
            per_page = URL_CONFIG.PER_PAGE if request.args.get(
                'per_page') is None else int(request.args.get('per_page'))
            page = URL_CONFIG.INIT_PAGE if request.args.get(
                'page') is None else int(request.args.get('page'))
            # query
            q = Admin.query

            # scope

            # search
            search_str = f'%{keyword}%'
            q = q.filter(Admin.username.like(search_str))

            # order
            q = q.order_by(Admin.username.asc())

            # pagination
            pagination = q.paginate(
                per_page=per_page, page=page)

            make_paginate.paginate(pagination)

            return jsonify(make_paginate.response), 200
        except NotFound as e:
            return jsonify(make_paginate.response), 200
        except Exception as e:
            return abort(500, e)

    # CREATE NEW
    if request.method == 'POST':
        try:
            data = request.get_json()

            insert_data = only_keys(data, *Admin.fillable_keys)
            default = {'password': '123456789'} # default password, not use
            admin = Admin(**insert_data, **default)

            db.session.add(admin)
            db.session.commit()
            return {'message': 'Created successfully'}, 200
        except Exception as e:
            abort(400, e)



@blueprint.route('/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def admin(id):
    if request.method == 'GET':
        try:
            admin = Admin.query.filter_by(id=id).first()
            return {"admin": admin.to_json()}
        except:
            abort(404)


# ROLES FOR ADMIN
@blueprint.route('/<int:admin_id>/roles', methods=['GET', 'POST'])
def admin_roles(admin_id):
    admin = Admin.query.filter_by(id=admin_id).first_or_404()
    if request.method == 'GET':
        try:
            return {"roles": admin.to_json().get('roles', [])}
        except:
            abort(404)

    if request.method == 'POST':
        try:
            role_ids = only_keys(request.get_json(), 'roles').get('roles', [])
            if not role_ids or len(role_ids) == 0:
                return {'message': 'invalid roles'}, 400
            for role_id in role_ids:
                role = Role.query.filter_by(id=role_id).first()
                if not role or role.name == 'super_admin':
                    return {'message': 'invalid roles'}, 400
                if role not in admin.roles:
                    admin.roles.append(role)
            db.session.commit()
            return {"admin": admin.to_json()}
        except Exception as e:
            abort(400, e)
