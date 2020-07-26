import os
from main import app


class URL_CONFIG:
    PER_PAGE = 10
    INIT_PAGE = 1


class UNIVERSAL:
    DATETIME_FORMAT = "%m/%d/%Y, %H:%M:%S:%f"


class RESOURCE_CONFIG:
    PUBLIC_URL = 'static'
    UPLOAD_FOLDER = 'resources'
    ALLOW_EXTENSION = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class BASECONFIG(object):
    SALT = "secret_key"
    DEBUG = False
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER = os.path.join(app.root_path, RESOURCE_CONFIG.UPLOAD_FOLDER)
    DATETIME_FORMAT = UNIVERSAL.DATETIME_FORMAT


class DEV_CONFIG(BASECONFIG):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    HOST_IP = 'localhost'
    PORT = '5000'
    SERVER_NAME = HOST_IP + ":" + PORT
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = ''
    DATABASE_NAME = 'food_delivery'
    DATABASE_HOST = 'localhost'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}{':' + DATABASE_PASSWORD if DATABASE_PASSWORD else ''}@{DATABASE_HOST}/{DATABASE_NAME}"


class LOCAL_CONFIG(BASECONFIG):
    HOST_IP = '192.168.0.200'
    PORT = '5000'
    SERVER_NAME = HOST_IP + ":" + PORT

    DATABASE_USER = 'tramtran'
    DATABASE_PASSWORD = '....'
    DATABASE_NAME = 'food_delivery'
    DATABASE_HOST = 'localhost'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}{':' + DATABASE_PASSWORD if DATABASE_PASSWORD else ''}@{DATABASE_HOST}/{DATABASE_NAME}"


class PROD_CONFIG(BASECONFIG):
    HOST_IP = '192.168.0.200'
    PORT = '5000'
    SERVER_NAME = HOST_IP + ":" + PORT

    DATABASE_USER = '___'
    DATABASE_PASSWORD = '___'
    DATABASE_NAME = 'food_delivery'
    DATABASE_HOST = 'localhost'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}{':' + DATABASE_PASSWORD if DATABASE_PASSWORD else ''}@{DATABASE_HOST}/{DATABASE_NAME}"
