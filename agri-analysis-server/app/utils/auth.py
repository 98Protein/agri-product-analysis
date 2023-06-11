import jwt
from flask import current_app, request

from app.models.admin import Admin


def get_user():
    try:
        token = request.headers.get('X-Token', None)
        if token is None:
            return None

        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = decoded.get('id', None)
        if user_id is None:
            return None
        user = Admin.query.filter_by(id=user_id).all()
        if user is None or len(user) == 0:
            return None
        user = user[0].to_dict()
        return user
    except Exception as e:
        print(e)
        return None

