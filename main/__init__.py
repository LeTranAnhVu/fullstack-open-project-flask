import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import jwt
# from flask_script import Manager

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

from main.config import LOCAL_CONFIG, DEV_CONFIG
# connect to database

app.config.from_object(DEV_CONFIG)


db = SQLAlchemy(app)

#data migrate
migrate = Migrate(app, db)



# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

from main.models.RestaurantAndTag import RestaurantTag
from main.models.ImageAndRestaurant import ImageRestaurant
from main.models.AdminAndRole import AdminRole
from main.models.PermissionAndRole import PermissionRole

from main.models.Restaurant import Restaurant
from main.models.Image import Image
from main.models.Tag import Tag
from main.models.User import User
from main.models.Order import Order
from main.models.Admin import Admin
from main.models.Role import Role
from main.models.Permission import Permission



import main.routes