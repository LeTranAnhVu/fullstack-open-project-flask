
from main import db
import blurhash
import datetime
from main.models import TimestampMixin, JsonMixin
from main import app
from main.config import RESOURCE_CONFIG

class Image(TimestampMixin, JsonMixin, db.Model):
    __tablename__ = 'images'
    id = db.Column('id', db.Integer, primary_key=True)
    __url = db.Column('url', db.Text)
    name = db.Column('name', db.String(200))
    blurhash = db.Column('blurhash', db.String(500))

    public_keys = [
        'id',
        'url',
        'name',
        'blurhash',
        'created_at',
        'updated_at'
    ]

    @property
    def url(self):
        return 'http://' + app.config["SERVER_NAME"] + '/api/' +self.__url
    @url.setter
    def url(self, value):
        self.__url = value
