

from main import app, db
from main.models import Base

class RestaurantTag(Base):
    __tablename__ = 'restaurant_tag'
    id = db.Column('id', db.Integer, primary_key=True)
    restaurant_id = db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurants.id'))
    tag_id = db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))