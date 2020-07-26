from main import db, bcrypt
from main.models import Base


class Admin(Base):
    __tablename__ = 'admins'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(200),
                         nullable=False, unique=True)
    password = db.Column('password', db.Text, nullable=False)
    logined_at = db.Column('logined_at', db.DateTime)
    is_active = db.Column('is_active', db.Boolean, default=False)
    actived_at = db.Column('actived_at', db.DateTime)

    public_keys = ['id', 'username', 'logined_at', 'created_at', 'updated_at', 'roles']
    fillable_keys = ['username', 'logined_at', 'password', 'created_at', 'updated_at']

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
