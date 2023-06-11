from sqlalchemy_serializer import SerializerMixin

from . import db
from . import gen_id
from .type import Type


class Variety(db.Model, SerializerMixin):
    __tablename__ = 't_variety'

    id = db.Column(db.String(32), default=gen_id, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    type_id = db.Column(db.String(32), db.ForeignKey(Type.id), nullable=False)
    origin_code = db.Column(db.Integer, nullable=False)

    type = db.relationship("Type")

    def __init__(self):
        pass

    def __int__(self, name, type_id):
        self.name = name
        self.type_id = type_id
