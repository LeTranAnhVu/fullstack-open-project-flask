from main import db, AdminRole, PermissionRole
from main.models import JsonMixin, TimestampMixin


class Role(TimestampMixin, JsonMixin, db.Model):
    __tablename__ = 'roles'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), unique=True, nullable=False)
    display_name = db.Column('display_name', db.String(50), unique=True, nullable=False)

    admins = db.relationship('Admin', secondary=AdminRole.__table__, backref=db.backref('roles', lazy='joined'), lazy='dynamic')
    permissions = db.relationship('Permission', secondary=PermissionRole.__table__, backref=db.backref('roles'), lazy='joined')

    public_keys=['id', 'name', 'display_name']
