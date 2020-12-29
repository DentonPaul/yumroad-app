import os

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'rand012345')

    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
    MAILGUN_KEY = os.getenv('MAILGUN_KEY')

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.getenv('SECRET_KEY')

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    # WTF_CSRF_SECRET_KEY = False
    TESTING = True

class ProdConfig(BaseConfig):
    SECRET_KEY = os.getenv('SECRET_KEY')

configurations = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig,
}