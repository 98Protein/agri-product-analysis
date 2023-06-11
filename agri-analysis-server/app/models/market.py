from sqlalchemy_serializer import SerializerMixin

from . import db
from . import gen_id
from .city import City


class Market(db.Model, SerializerMixin):
    __tablename__ = 't_market'

    id = db.Column(db.String(32), default=gen_id, primary_key=True)
    city_id = db.Column(db.String(32), db.ForeignKey(City.id), nullable=True)
    name = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(64), nullable=True)
    picture_url = db.Column(db.String(64), nullable=True)
    details = db.Column(db.Text, nullable=True)
    origin_id = db.Column(db.Integer, nullable=True)

    city = db.relationship("City")

    def __init__(self):
        pass

    def __int__(self, name, details, city_id):
        self.name = name
        self.details = details
        self.city_id = city_id
