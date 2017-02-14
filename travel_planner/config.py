from datetime import timedelta


class Config(object):
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_AUTH_URL_RULE = '/api/token'
    JWT_EXPIRATION_DELTA = timedelta(days=3)


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class ProdConfig(Config):
    pass