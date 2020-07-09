
from main import app, db
import datetime
from main.models import TimestampMixin, JsonMixin


class ImageRestaurant(TimestampMixin, JsonMixin, db.Model):
    __tablename__ = 'image_restaurant'
    id = db.Column('id', db.Integer, primary_key=True)
    image_id = db.Column('image_id', db.Integer, db.ForeignKey('images.id'))

    restaurant_id = db.Column(
        'restaurant_id', db.Integer, db.ForeignKey('restaurants.id'))

    __image = db.relationship('Image')
    restaurant = db.relationship('Restaurant')
    is_main = db.Column('is_main', db.Boolean, default=False)

    public_keys=[
        'id',
        'image',
        'is_main'
    ]

    @property
    def image(self):
        return self.__image.to_json()
