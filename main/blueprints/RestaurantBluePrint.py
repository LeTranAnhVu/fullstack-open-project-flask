import os
from flask import Blueprint, jsonify, json, make_response, abort, request
from werkzeug.exceptions import NotFound
from main import app, db, Restaurant, ImageRestaurant, Tag, Image
from main.helpers.type2type import str2bool
from main.helpers.common import without_keys

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_, not_
import datetime
from main.config import URL_CONFIG, RESOURCE_CONFIG

blueprint = Blueprint('restaurant', __name__)

# CURD restaurants
@blueprint.route('', methods=['GET', 'POST'])
def restaurants():
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
            is_online = None if request.args.get(
                'is_online') is None else str2bool(request.args.get('is_online'))
            # query
            q = Restaurant.query

            # scope
            if is_online is not None:
                q = q.filter_by(online=is_online)

            # search
            search_str = f'%{keyword}%'
            q = q.filter(or_(Restaurant.name.like(search_str),
                             Restaurant.description.like(search_str)))

            # order
            q = q.order_by(Restaurant.name.asc())

            # pagination
            pagination = q.paginate(
                per_page=per_page, page=page)

            data = []
            for restaurant in pagination.items:
                data.append(restaurant.to_json())
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

    # CREATE NEW
    if request.method == 'POST':
        try:
            data = request.get_json()
            # without keys
            insert_data = without_keys(data, 'images', 'tags')
            restaurant = Restaurant(**insert_data)

            for tag_id in data.get('tags', []):
                tag = Tag.query.filter_by(id=tag_id).first()
                if tag:
                    restaurant.append_tag(tag)
                else: pass
            for index, image_id in enumerate(data['images']):
                image = Image.query.filter_by(id=image_id).first()
                if image:
                    image_restaurant = ImageRestaurant(
                        is_main=(index == 0), image=image)
                    restaurant.append_image(image_restaurant)

            db.session.add(restaurant)
            db.session.commit()
            return {'message': 'Created successfully'}, 200
        except Exception as e:
            abort(400, e)


@blueprint.route('/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def restaurant(id):
    if request.method == 'GET':
        try:
            restaurant = Restaurant.query.filter_by(id=id).first()
            return {"restaurant": restaurant.to_json()}
        except:
            abort(404)

    if request.method == 'PATCH':
        try:
            query = Restaurant.query.filter_by(id=id)
            data = request.get_json()
            insert_data = without_keys(data, 'images', 'tags')
            restaurant = query.first_or_404()
            if insert_data or data.get('tags', []) or data.get('images', []):
                if insert_data:
                    query.update(insert_data)
                for tag_id in data.get('tags', []):
                    tag = Tag.query.filter_by(id=tag_id).first()
                    if tag:
                        restaurant.append_tag(tag)
                    else: pass
                for index, image_id in enumerate(data.get('images', [])):
                    image = Image.query.filter_by(id=image_id).first()
                    if image:
                        image_restaurant = ImageRestaurant(image=image)
                        restaurant.append_image(image_restaurant)
                db.session.commit()
                return {'message': 'Updated successfully'}, 200
            return {'message': 'Not thing to update'}, 200
        except NoResultFound as e:
            abort(404, e)
        except Exception as e:
            abort(422, e)

    if request.method == "DELETE":
        try:
            restaurant = Restaurant.query.filter_by(id=id).first_or_404()
            db.session.delete(restaurant)
            db.session.commit()
            return {'message': 'Deleted successfully'}, 200
        except NoResultFound as e:
            abort(404, e)
