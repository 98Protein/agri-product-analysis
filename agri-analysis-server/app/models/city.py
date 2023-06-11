from sqlalchemy_serializer import SerializerMixin

from . import db
from . import gen_id
from .province import Province


class City(db.Model, SerializerMixin):
    __tablename__ = 't_city'

    id = db.Column(db.String(32), default=gen_id, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    province_id = db.Column(db.String(32), db.ForeignKey(Province.id), nullable=False)
    origin_index = db.Column(db.Integer, nullable=True)
    full_name = db.Column(db.String(32), nullable=True)

    province = db.relationship("Province")

    def __init__(self):
        pass

    def __int__(self, name, province_id):
        self.name = name
        self.province_id = province_id
