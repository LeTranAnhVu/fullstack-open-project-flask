import os
from main import db, app
import blurhash
import datetime
from main import ImageRestaurant, RestaurantTag
from main.models import TimestampMixin, JsonMixin


class Restaurant(TimestampMixin, JsonMixin, db.Model):
    __tablename__ = 'restaurants'
    id = db.Column('id', db.Integer, primary_key=True)
    city = db.Column('city', db.String(200))
    currency = db.Column('currency', db.String(5))
    delivery_price = db.Column('delivery_price', db.Float)
    description = db.Column('description', db.String(500))
    __images = db.relationship('ImageRestaurant')
    __tags = db.relationship('Tag', secondary=RestaurantTag.__table__, lazy='dynamic', backref=db.backref('restaurants', lazy=True)) 
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
        "tags",
        "name",
        "online",
        "blurhash",
        "created_at",
        "updated_at"
    ]

    @property
    def images(self):
        return [_image.to_json() for _image in self.__images]
    @property
    def tags(self):
        return [_tag.to_json() for _tag in self.__tags]
    
    def append_tag(self, tag):
        if tag not in self.__tags:
            self.__tags.append(tag)

    def append_image(self, image):
        if image not in self.__images:
            self.__images.append(image)

