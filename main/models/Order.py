from main import db
from main.models import JsonMixin, TimestampMixin


class Order(JsonMixin, TimestampMixin, db.Model):
    __tablename__ = 'orders'
    id = db.Column('id', db.Integer, primary_key=True)
    code = db.Column('code', db.String(100), nullable=False)
    ordered_at = db.Column('ordered_at', db.DateTime, nullable=False)
    order_place = db.Column('order_place', db.String(1000), nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column('item_id', db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy='dynamic'), lazy='joined')
    item = db.relationship('Restaurant', backref=db.backref('orders', lazy='dynamic'), lazy='joined')
    amount = db.Column('amount', db.Integer, nullable=False)
    note = db.Column('note', db.String(1000))
    status = db.Column('status', db.SmallInteger, default=0)

    public_keys = ['user', 'item', 'created_at', 'updated_at', 'id', 'code', 'ordered_at', 'order_place', 'amount',
                   'note', 'status']
