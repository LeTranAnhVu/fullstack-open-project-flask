import os
from flask import Blueprint, jsonify, json, abort, request
from main import app, db, Restaurant, Tag, User, bcrypt, Admin, Permission, Role, ImageRestaurant, Image
import urllib.request
from PIL import Image as ImageUtil
from main.helpers.upload_file import _make_fileurl
import blurhash as blurhash_maker
import datetime

blueprint = Blueprint('seed', __name__)


@blueprint.route('/image_for_restaurant')
def seed_image():
    with open(os.path.join(app.root_path, '../json/restaurants.json'), 'r') as file:
        restaurants = json.load(file)['restaurants']
        try:
            for restaurant in restaurants:
                restaurant_model = Restaurant.query.filter_by(name=restaurant.get('name')).first()
                image_url = restaurant.get('image')
                if restaurant_model and image_url:
                    print('restaurant', restaurant_model)
                    local_filename, headers = urllib.request.urlretrieve(image_url)
                    with ImageUtil.open(local_filename) as image:
                        # make img name and extension
                        image_type = headers['Content-Type'].split('/')[-1]
                        image_name = image_url.split('/')[-1] + '.' + image_type
                        # save
                        image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images', image_name))

                        # get image relative path
                        image_link = _make_fileurl(image_name, 'images')
                        hash = blurhash_maker.encode(os.path.join(app.config['UPLOAD_FOLDER'], 'images', image_name),
                                                     x_components=4, y_components=3)
                        imageModel = Image(name=image_name, blurhash=hash, url=image_link)
                        image_restaurant = ImageRestaurant(is_main=True, image=imageModel)
                        restaurant_model.append_image(image_restaurant)

            db.session.commit()
            return jsonify({'message': 'seed success'}), 200
        except Exception as e:
            return jsonify({'message': 'seed fail', 'info': str(e)}), 500


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
        now = datetime.datetime.utcnow()
        ad1 = Admin(username='admin1', password='admin', is_active=True, actived_at=now)
        ad2 = Admin(username='admin2', password='admin', is_active=True, actived_at=now)
        ad3 = Admin(username='admin3', password='admin', is_active=True, actived_at=now)
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
                       'user', 'tag', 'restaurant', 'order', 'image']

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
                    per = Permission.query.filter_by(
                        name=f'{entity}:{action}').first_or_404()
                    partner.permissions.append(per)
        db.session.commit()
        return {'message': 'seed success'}
    except Exception as e:
        abort(500, e)


@blueprint.route('/admin_role')
def seed_admin_role():
    try:
        admin1 = Admin.query.filter_by(id=1).first()
        admin2 = Admin.query.filter_by(id=2).first()
        admin3 = Admin.query.filter_by(id=3).first()
        supe = Role.query.filter_by(name='super_admin').first()
        partner = Role.query.filter_by(name='restaurant_partner').first()

        admin1.roles.append(supe)
        admin2.roles.append(partner)
        admin3.roles.append(partner)

        db.session.commit()
        return {'message': 'seed success'}
    except Exception as e:
        abort(500, e)
