from main import db
import datetime
class TimestampMixin(object):
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

class JsonMixin():
    def to_json(self):
        return { key: getattr(self, key) for key in self.public_keys}