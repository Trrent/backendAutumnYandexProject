from decouple import config

class Config:
    TESTING = False
    SECRET_KEY = config('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = config('DEBUG', cast=bool)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev-db.db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test-db.db'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod-db.db'


config_dict = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig
}