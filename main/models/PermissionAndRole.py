from main import db
from main.models import JsonMixin, TimestampMixin


class PermissionRole(TimestampMixin, db.Model):
    __tablename__ = 'permission_role'
    id = db.Column('id', db.Integer, primary_key=True)
    permission_id = db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))