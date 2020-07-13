import os
from flask import Blueprint, jsonify, json, abort, request
from main import app, db, Restaurant, Tag, User, bcrypt

import datetime


blueprint = Blueprint('seed', __name__)
@blueprint.route('/restaurants')
def seed_restaurants():
    with open(os.path.join(app.root_path, '../json/restaurants.json'), 'r') as file:
        restaurants = json.load(file)['restaurants']
        try:
            for restaurant in restaurants:
                res_model = Restaurant(
                    city=restaurant.get('city', None),
                    currency=restaurant.get('currency', None),
                    delivery_price=restaurant.get('delivery_price', None),
                    description=restaurant.get('description', None),
                    name=restaurant.get('name', None),
                    online=restaurant.get('online', False)
                )
                db.session.add(res_model)

            db.session.commit()
            return jsonify({'message': 'seed success'}), 200
        except Exception as e:
            return jsonify({'message': 'seed fail', 'info': str(e)}), 500

@blueprint.route('/tags')
def seed_tags():
    try:
        with open(os.path.join(app.root_path, '../json/restaurants.json')) as file:
            restaurants = json.load(file)['restaurants']
            for res in restaurants:
                restaurant = Restaurant.query.filter_by(
                    name=res.get('name', None)).first()
                tags = res.get('tags', None)
                if tags and restaurant:
                    for t in tags:
                        tag = Tag.query.filter_by(name=t).first()
                        if not tag:
                            tag = Tag(name=t)
                            db.session.add(tag)
                        restaurant.append_tag(tag)
                    db.session.commit()
            return jsonify({'data': 'seed success'})

    except Exception as e:
        abort(500, e)


@blueprint.route('/users')
def seed_users():
    try:
        user = User(username='letrananhvu', password='admin')
        db.session.add(user)
        db.session.commit()
        return {'message': 'seed success'}
    except Exception as e:
        abort(500, e)