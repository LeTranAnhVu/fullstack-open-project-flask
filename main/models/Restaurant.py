import os
from main import db, app
import blurhash
import datetime
from main import ImageRestaurant
from main.models import TimestampMixin, JsonMixin


class Restaurant(TimestampMixin, JsonMixin, db.Model):
    __tablename__ = 'restaurants'
    id = db.Column('id', db.Integer, primary_key=True)
    city = db.Column('city', db.String(200))
    currency = db.Column('currency', db.String(5))
    delivery_price = db.Column('delivery_price', db.Float)
    description = db.Column('description', db.String(500))
    __images = db.relationship('ImageRestaurant')
    name = db.Column('name', db.String(300))
    online = db.Column('online', db.Boolean)
    blurhash = db.Column('blurhash', db.String(200))

    public_keys = [
        "id",
        "city",
        "currency",
        "delivery_price",
        "description",
        "images",
        "name",
        "online",
        "blurhash",
        "created_at",
        "updated_at"
    ]

    @property
    def images(self):
        return [_image.to_json() for _image in self.__images]

