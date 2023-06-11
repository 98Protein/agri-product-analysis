from datetime import date

from flask import Flask
from flask.json import JSONEncoder
from werkzeug.security import generate_password_hash

from app.config import config
from app.models import db
from app.models.admin import Admin
from . import models, routes


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()

        return super().default(o)


def create_app(config_name='default'):
    app = Flask(__name__)
    config[config_name].init_app(app)
    app.config.from_object(config[config_name])
    app.json_encoder = MyJSONEncoder

    models.init_app(app)
    routes.init_app(app)

    with app.app_context():
        admin = Admin.query.filter(Admin.username == 'admin').all()
        if admin is None or len(admin) == 0:
            db.session.add(Admin("admin", generate_password_hash('admin'), 'super-admin'))
            db.session.commit()

    return app
