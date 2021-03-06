from main import db
from main.models import Base


class Permission(Base):
    __tablename__ = 'permissions'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), unique=True, nullable=False)
    display_name = db.Column('display_name', db.String(50), unique=True, nullable=False)

    public_keys=['id', 'name', 'display_name']
    