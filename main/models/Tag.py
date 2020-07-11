from main import app, db
from main.models import TimestampMixin, JsonMixin
class Tag (TimestampMixin, JsonMixin, db.Model):
    __tablename__ = 'tags'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    
    public_keys=['id', 'name']