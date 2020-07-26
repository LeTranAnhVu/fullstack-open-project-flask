from main import db
from main.models import Base


class AdminRole(Base):
    __tablename__ = 'admin_role'
    id = db.Column('id', db.Integer, primary_key=True)
    admin_id = db.Column('admin_id', db.Integer, db.ForeignKey('admins.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))