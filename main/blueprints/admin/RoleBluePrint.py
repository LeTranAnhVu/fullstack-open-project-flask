from flask import Blueprint, request, abort, jsonify
from werkzeug.exceptions import NotFound
from main import app, db, Role, Permission
from main.helpers.pagination import MakePaginate
from main.helpers.common import only_keys
from main.config import URL_CONFIG, RESOURCE_CONFIG
from sqlalchemy import or_, and_, not_

blueprint = Blueprint('manager_role', __name__)

# ROLES
@blueprint.route('', methods=['GET', 'POST'])
def roles():
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
            q = Role.query

            # scope

            # search
            search_str = f'%{keyword}%'
            q = q.filter(or_(Role.name.like(search_str),
                             Role.display_name.like(search_str)))

            # order
            q = q.order_by(Role.name.asc())

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

            insert_data = only_keys(data, *Role.fillable_keys)
            role = Role(**insert_data)
            
            permissions = data.get('permissions', [])

            if len(permissions) != 0:
                for permission_id in permissions:
                    permission = Permission.query.filter_by(id=permission_id).first()
                    if permission:
                        role.permissions.append(permission)

            db.session.add(role)
            db.session.commit()
            return {'message': 'Created successfully'}, 200
        except Exception as e:
            abort(400, e)


@blueprint.route('/<int:id>', methods=['GET', 'PATCH'])
def role(id):
    role = Role.query.filter_by(id=id).first_or_404()
    if request.method == 'GET':
        try:
            return {"role": role.to_json(extra_keys=['permissions'])}
        except:
            abort(404)
    if request.method == 'PATCH':
        try:
            data = request.get_json()
            permission_ids = data.get('permissions', [])
            
            # remove permission
            exist_permission_ids = [permission.id for permission in role.permissions]
            for exist_id in exist_permission_ids:
                if exist_id not in permission_ids:
                    del_permission = Permission.query.filter_by(id=exist_id).first()
                    role.permissions.remove(del_permission)
            # add permission
            for permission_id in permission_ids:
                permission = Permission.query.filter_by(id=permission_id).first()
                if permission and permission not in role.permissions:
                    role.permissions.append(permission)
            
            db.session.commit()
            return {"role": role.to_json(extra_keys=['permissions'])}
        except Exception as e:
            abort(404, e)

