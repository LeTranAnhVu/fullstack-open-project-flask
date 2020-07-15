import os
from flask import Blueprint, jsonify, json, abort, request
from main import app, db, Restaurant, Tag, User, bcrypt, Admin, Permission, Role

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
        user = User(username='admin', password='admin')
        db.session.add(user)
        db.session.commit()
        return {'message': 'seed success'}
    except Exception as e:
        abort(500, e)


@blueprint.route('/admins')
def seed_admins():
    try:
        ad1 = Admin(username='admin1', password='admin')
        ad2 = Admin(username='admin2', password='admin')
        ad3 = Admin(username='admin3', password='admin')
        db.session.add(ad1)
        db.session.add(ad2)
        db.session.add(ad3)
        db.session.commit()
        return {'message': 'seed success'}
    except Exception as e:
        abort(500, e)


@blueprint.route('/roles')
def seed_roles():
    try:
        role1 = Role(name='super_admin', display_name='super admin')
        role2 = Role(name='restaurant_partner',
                     display_name='restaurant partner')
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()
        return {'message': 'seed success'}
    except Exception as e:
        abort(500, e)


@blueprint.route('/permissions')
def seed_permissions():
    try:
        action_list = ['read', 'create', 'edit', 'delete', 'all']
        entity_list = ['admin', 'role', 'permission',
                       'user', 'tag',  'restaurant', 'order', 'image']

        for entity in entity_list:
            for action in action_list:
                per = Permission(
                    name=f'{entity}:{action}', display_name=f'{action} {entity}')
                db.session.add(per)
        db.session.commit()
        return {'message': 'seed success'}
    except Exception as e:
        abort(500, e)


@blueprint.route('/permission_role')
def seed_permission_role():
    try:
        super_admins = Role.query.filter_by(name="super_admin").all()
        all_permissions = Permission.query.filter(
            Permission.name.like("%:all%")).all()
        partners = Role.query.filter_by(name="restaurant_partner").all()
        partner_pers = ['read,create,edit:restaurant',
            'read:user', 'create:image', 'read,edit:order']
        
        for sadmin in super_admins:
            for per in all_permissions:
                sadmin.permissions.append(per)

        for partner in partners:
            for per in partner_pers:
                entity = per.split(':')[-1]
                actions = per.split(':')[0].split(',')
                for action in actions:
                    per = Permission.query.filter_by(name=f'{entity}:{action}').first_or_404()
                    partner.permissions.append(per)
        db.session.commit()
        return {'message': 'seed success'}
    except Exception as e:
        abort(500, e)
