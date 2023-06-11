import yaml
from flask_cors import CORS
from sqlalchemy.engine import URL

from app.spark import init_sql


class BaseConfig:  # 基本配置类
    ITEMS_PER_PAGE = 10

    def __init__(self):
        self.app = None

    @classmethod
    def init_app(cls, app):
        cls.app = app


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'some secret words'

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        cls.SECRET_KEY = yaml.load(open('app/config/auth.secret.yml'), Loader=yaml.SafeLoader) \
            ['development']['auth']['secret']
        mysql_config = yaml.load(open('app/config/database.secret.yml'),
                                 Loader=yaml.SafeLoader)['development']['database']

        cls.SQLALCHEMY_DATABASE_URI = URL(drivername=mysql_config['drivername'], username=mysql_config['username'],
                                          password=mysql_config['password'],
                                          host=mysql_config['host'], port=mysql_config['port'],
                                          database=mysql_config['database'])
        CORS(app, supports_credentials=True)
        init_sql('development')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'some secret words'

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        cls.SECRET_KEY = yaml.load(open('app/config/auth.secret.yml'), Loader=yaml.SafeLoader)['production']['auth'][
            'secret']
        mysql_config = yaml.load(open('app/config/database.secret.yml'),
                                 Loader=yaml.SafeLoader)['production']['database']

        cls.SQLALCHEMY_DATABASE_URI = URL(drivername=mysql_config['drivername'], username=mysql_config['username'],
                                          password=mysql_config['password'],
                                          host=mysql_config['host'], port=mysql_config['port'],
                                          database=mysql_config['database'])
        CORS(app, supports_credentials=True)
        init_sql('production')


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'production': ProductionConfig
}
