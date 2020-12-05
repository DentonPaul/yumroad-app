class BaseConfig:
    pass

class DevConfig(BaseConfig):
    pass

class TestConfig(BaseConfig):
    TESTING = True

class ProdConfig(BaseConfig):
    pass

configurations = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig,
}