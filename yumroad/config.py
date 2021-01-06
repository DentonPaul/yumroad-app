import os

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'rand012345')

    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
    MAILGUN_KEY = os.getenv('MAILGUN_KEY')

    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_k1')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'sk_test_k1')
    STRIPE_WEBHOOK_KEY = os.getenv('STRIPE_WEBHOOK_KEY', 'whsec_test_secret')

    SENTRY_DSN = os.getenv('SENTRY_DSN')

    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    RQ_REDIS_URL = REDIS_URL
    RQ_DASHBOARD_REDIS_URL =  RQ_REDIS_URL

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    ASSETS_DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    # WTF_CSRF_SECRET_KEY = False
    TESTING = True
    ASSETS_DEBUG = True
    DEBUG_TB_ENABLED = False
    CACHE_TYPE = 'null'
    CACHE_NO_NULL_WARNING = True

    # run jobs instantly, without need to spin up a worker
    RQ_ASYNC = False
    RQ_CONNECTION_CLASS = 'fakeredis.FakeStrictRedis'

class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    REDIS_URL = os.getenv('REDIS_URL')
    RQ_REDIS_URL = REDIS_URL
    RQ_DASHBOARD_REDIS_URL = RQ_REDIS_URL
    RQ_ASYNC = (REDIS_URL is not None)
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'yumroad-'

configurations = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig,
}