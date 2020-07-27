import os
from main import app
from main.settings import SALT, HOST_IP, PORT, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_HOST, ENV

class URL_CONFIG:
    PER_PAGE = 10
    INIT_PAGE = 1


class UNIVERSAL:
    DATETIME_FORMAT = "%m/%d/%Y, %H:%M:%S:%f"


class RESOURCE_CONFIG:
    PUBLIC_URL = 'static'
    UPLOAD_FOLDER = 'resources'
    ALLOW_EXTENSION = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class ENV_CONFIG(object):
    SALT = SALT
    DEBUG = False if ENV == 'production' else True
    SQLALCHEMY_ECHO = False if ENV == 'production' else True
    UPLOAD_FOLDER = os.path.join(app.root_path, RESOURCE_CONFIG.UPLOAD_FOLDER)
    DATETIME_FORMAT = UNIVERSAL.DATETIME_FORMAT
    HOST_IP = HOST_IP
    PORT = PORT
    # SERVER_NAME = HOST_IP + ":" + PORT
    DATABASE_USER = DATABASE_USER
    DATABASE_PASSWORD = DATABASE_PASSWORD
    DATABASE_NAME = DATABASE_NAME
    DATABASE_HOST = DATABASE_HOST

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}{':' + DATABASE_PASSWORD if DATABASE_PASSWORD else ''}@{DATABASE_HOST}/{DATABASE_NAME}"