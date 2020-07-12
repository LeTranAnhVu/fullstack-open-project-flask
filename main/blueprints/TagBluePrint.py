import os
from flask import Blueprint, jsonify, abort, request
from main import app, db,Tag
from main.helpers.type2type import str2bool
from main.helpers.common import without_keys

import datetime
from main.config import URL_CONFIG, RESOURCE_CONFIG

blueprint = Blueprint('tag', __name__)


# CRUD tags
@blueprint.route('', methods=['GET', 'POST'])
def tags():
    if request.method == 'GET':
        res_json = {
            'data': [],
            'total': None,
            'pages': None,
            'current_page': None,
            'next_page': None,
            'prev_page': None
        }
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

            data = []
            for tag in pagination.items:
                data.append(tag.to_json())
            res_json['data'] = data
            res_json['total'] = pagination.total
            res_json['pages'] = pagination.pages
            res_json['current_page'] = pagination.page
            res_json['next_page'] = pagination.next_num if pagination.has_next is True else None
            res_json['prev_page'] = pagination.prev_num if pagination.has_prev is True else None

            return jsonify(res_json), 200
        except NotFound as e:
            return jsonify(res_json), 200
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
