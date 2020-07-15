import datetime
from main import app, jwt

def gen_token(payload={}, minutes=60):
    now = datetime.datetime.utcnow()
    expired_at = now + datetime.timedelta(minutes=minutes)
    expired_at = expired_at.strftime(app.config['DATETIME_FORMAT'])

    token = jwt.encode({**payload, 'expired_at': expired_at}, app.config['SALT']).decode('utf-8')
    return token

def check_available_token(token):
    payload = jwt.decode(token, app.config['SALT'])
    expired_at = payload.get('expired_at', None)
    if not expired_at: 
        return None
    expired_at = datetime.datetime.strptime(expired_at, app.config['DATETIME_FORMAT'])

    now = datetime.datetime.utcnow()

    if now >= expired_at : # out of date
        return None

    # token till available
    return payload
