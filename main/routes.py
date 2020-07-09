import os
from flask import jsonify, json, make_response, abort, request, send_from_directory
from werkzeug.exceptions import HTTPException, NotFound
from main import app, db, Restaurant, Image, ImageRestaurant
from main.helpers.type2type import str2bool
from main.helpers.common import without_keys

from sqlalchemy.orm.exc import UnmappedInstanceError, NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_, not_
import datetime
from main.config import URL_CONFIG, RESOURCE_CONFIG
from main.helpers.upload_file import upload_file
import blurhash as blurhash_maker


@app.route('/')
def home():
    return {'data': 'success'}, 200


@app.route('/seed/restaurants')
def seed_restaurants():
    # return os.path.join(os.path.dirname(__file__), '../json/restaurants.json')
    with open(os.path.join(os.path.dirname(__file__), '../json/restaurants.json'), 'r') as f:
        restaurants = json.load(f)['restaurants']
        try:
            for restaurant in restaurants:
                res_model = Restaurant(
                    city=restaurant.get('city', None),
                    currency=restaurant.get('currency', None),
                    delivery_price=restaurant.get('delivery_price', None),
                    description=restaurant.get('description', None),
                    name=restaurant.get('name', None),
                    online=restaurant.get('online', False),
                    blurhash=restaurant.get('blurhash', None)
                )
                db.session.add(res_model)

            db.session.commit()
            return make_response({'message': 'seed success'}, 200)
        except Exception as e:
            return make_response({'message': 'seed fail', 'info': str(e)}, 500)


# CURD restaurants
@app.route('/restaurants', methods=['GET', 'POST'])
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
            # without images
            insert_data = without_keys(data, 'images')
            restaurant = Restaurant(**insert_data)
            for index, image_id in enumerate(data['images']):
                image = Image.query.filter_by(id=image_id).first()
                if image:
                    image_restaurant = ImageRestaurant(is_main =(index == 0), image=image)
                    restaurant.images.append(image_restaurant)

            db.session.add(restaurant)
            db.session.commit()
            return {'message': 'Created successfully'}, 200
        except Exception as e:
            abort(400, e)


@app.route('/restaurants/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
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
            update_data = request.get_json()
            if update_data:
                query.update(update_data)
                restaurant = query.first_or_404()
                restaurant.updated_at = datetime.datetime.utcnow()
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


# CRUD files
@app.route(f'/{RESOURCE_CONFIG.PUBLIC_URL}/<string:resource_type>/<string:resource_name>')
def get_resource(resource_type, resource_name):
    allowed_resource = {'images', 'documents', 'css'}
    if (resource_type not in allowed_resource):
        abort(400, {'message': 'Restricted resource'})
    return send_from_directory(app.config['UPLOAD_FOLDER'], f'{resource_type}/{resource_name}')


@app.route('/upload/<string:resource_type>', methods=['POST'])
def saved_files(resource_type):
    allowed_resource = {'images', 'documents', 'css'}
    if (resource_type not in allowed_resource):
        abort(400, {'message': 'Restricted resource'})
    if request.method == 'POST':
        try:
            file_list = request.files.getlist('files')
            if len(file_list) == False:
                abort(400, {'message': 'there is no file'})
            saved_filepaths = []
            for file in file_list:
                saved_filepaths.append(upload_file(file, resource_type))

            imageModels = []
            if (resource_type == 'images'):
                for filepath in saved_filepaths:
                    name = filepath.split('/')[-1]
                    hash = ''
                    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'images', name), 'rb') as imagefile:
                        hash = blurhash_maker.encode(os.path.join(
                            app.config['UPLOAD_FOLDER'], 'images', name), x_components=4, y_components=3)
                    imageModel = Image(name=name, blurhash=hash, url=filepath)
                    db.session.add(imageModel)
                    imageModels.append(imageModel)
                db.session.commit()
            return {'data': [image.to_json() for image in imageModels]}, 201
        except Exception:
            abort(400, {'message': 'Cannot upload resource'})


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


@app.errorhandler(500)
@error_decorator
def server_error(error):
    message = error.description if app.debug == True else {
        "message": "Internal server error"}
    return message, error.code


@app.errorhandler(400)
@error_decorator
def bad_request(error):
    message = error.description if app.debug == True else {
        "message": "Bad request"}
    return message, error.code


@app.errorhandler(404)
@error_decorator
def not_found(error):
    message = error.description if app.debug == True else {
        "message": "Resource not found"}
    return message, error.code


@app.errorhandler(422)
@error_decorator
def unprocessable_entity(error):
    message = error.description if app.debug == True else {
        "message": "Cannot process this request"}
    return message, error.code
