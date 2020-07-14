import os
from flask import Blueprint, jsonify, abort, request
from main import app, db,Tag
from main.helpers.type2type import str2bool
from main.helpers.common import without_keys
from main.helpers.pagination import MakePaginate
import datetime
from main.config import URL_CONFIG, RESOURCE_CONFIG

blueprint = Blueprint('tag', __name__)


# CRUD tags
@blueprint.route('', methods=['GET', 'POST'])
def tags():
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
            q = Tag.query

            # search
            search_str = f'%{keyword}%'
            q = q.filter(Tag.name.like(search_str))

            # order
            q = q.order_by(Tag.id.asc())

            # pagination
            pagination = q.paginate(
                per_page=per_page, page=page)

            make_paginate.paginate(pagination)
            return jsonify(make_paginate.response), 200
        except NotFound as e:
            return jsonify(make_paginate.response), 200
        except Exception as e:
            return abort(500, e)
    if request.method == 'POST':
        try:
            data = request.get_json()
            name = data.get('name', None)
            if name is None:
                return abort(400)
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
            return {'message': 'Created successfully'}, 200
        except Exception as e:
            abort(400, e)

@blueprint.route('/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def tag(id):
    tag = Tag.query.filter_by(id=id).first_or_404()
    try:
        if request.method == 'GET':
            return {'data': tag.to_json()}
        if request.method == 'PATCH':
            data = request.get_json()
            name = data.get('name', "")
            if name and name != "" and tag.name != name:
                tag.name = name
                db.session.commit()
                return {'data': tag.to_json()}, 200
            else:
                return {'message': 'not thing to update'}, 200
        if request.method == 'DELETE':
            db.session.delete(tag)
            db.session.commit()
            return {'message': 'Deleted successfully'}, 200
            
    except Exception as e:
        abort(500)
