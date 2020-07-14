from main import db
import datetime
from main.helpers.common import without_keys, without_items
class TimestampMixin(object):
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

class JsonMixin():
    def to_json(self, except_keys=[], parent_models=set()):
        d = dict()
        parent_models.add(self.__class__)
        for key in without_items(self.public_keys, except_keys):
            data = getattr(self, key, None)
            if isinstance(data, db.Model) and data.__class__ not in parent_models :
                d[key] = data.to_json(parent_models=parent_models.copy())
            elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], db.Model):
                d[key] = [in_model.to_json(parent_models=parent_models.copy()) for in_model in data]
            elif not isinstance(data, db.Model):
                d[key]= data
        return d

