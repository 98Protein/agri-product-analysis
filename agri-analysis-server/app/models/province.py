from sqlalchemy_serializer import SerializerMixin

from . import db
from . import gen_id


class Province(db.Model, SerializerMixin):
    __tablename__ = 't_province'

    id = db.Column(db.String(32), default=gen_id, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    origin_index = db.Column(db.Integer, nullable=True)
    full_name = db.Column(db.String(32), nullable=True)

    def __init__(self):
        pass

    def __int__(self, name):
        self.name = name
