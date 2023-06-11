from sqlalchemy_serializer import SerializerMixin

from . import db
from . import gen_id


class Type(db.Model, SerializerMixin):
    __tablename__ = 't_type'

    id = db.Column(db.String(32), default=gen_id, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def __init__(self):
        pass

    def __int__(self, name, market_id):
        self.name = name
        self.market_id = market_id
