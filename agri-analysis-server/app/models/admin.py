from sqlalchemy_serializer import SerializerMixin

from . import db
from . import gen_id


class Admin(db.Model, SerializerMixin):
    __tablename__ = 't_admin'

    id = db.Column(db.String(32), default=gen_id, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(102), nullable=False)
    identity = db.Column(db.String(32), default="ordinary-admin", nullable=False)

    def __int__(self):
        pass

    def __init__(self, username, password, identity):
        self.username = username
        self.password = password
        self.identity = identity
