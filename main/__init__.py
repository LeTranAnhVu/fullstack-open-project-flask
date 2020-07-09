import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from main.config import RESOURCE_CONFIG
# from flask_script import Manager

app = Flask(__name__)

# connect to database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/food_delivery"
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, RESOURCE_CONFIG.UPLOAD_FOLDER)
app.config["SERVER_NAME"] = "localhost:5000"
db = SQLAlchemy(app)

#data migrate
migrate = Migrate(app, db)



# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

from main.models.ImageAndRestaurant import ImageRestaurant
from main.models.Restaurant import Restaurant
from main.models.Image import Image

import main.routes