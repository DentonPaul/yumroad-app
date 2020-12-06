class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = True

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False
    TESTING = True

class ProdConfig(BaseConfig):
    pass

configurations = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig,
}