import uuid

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def gen_id():
    return uuid.uuid4().hex


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return db
