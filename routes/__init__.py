import uuid
from functools import wraps

from flask import session, request, abort

from models.user import User

# 导入redis，建立缓存
import redis
cache = redis.StrictRedis()

def current_user():
    uid = session.get('user_id', '')
    u = User.one(id=uid)
    return u


# csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        if cache.exists(token.encode()) and int(cache.get(token).decode()) == u.id:
            cache.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    cache[token] = u.id
    return token
