import os
"""
    This will be the base setting of the entire 
    application. They are the default configs
"""

class Config(object):
    """
        Parent configuration class.
    """
    DEBUG = False
    TESTING = False
    # Database
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SEED_ADMIN_EMAIL = os.getenv('SEED_ADMIN_EMAIL')
    SEED_ADMIN_PASSWORD = os.getenv('SEED_ADMIN_PASSWORD')
    SEED_ADMIN_USERNAME = os.getenv('SEED_ADMIN_USERNAME')



class DevelopmentConfig(Config):
    """
        Configurations for Development.
    """
    DEVELOPMENT = True
    DEBUG = True
    DB_NAME = os.getenv('DEV_DB_NAME')


class TestingConfig(Config):
    """
        Configurations for Testing
    """
    TESTING = True
    DEBUG = True
    DB_NAME = os.getenv('TEST_DB_NAME')


class ProductionConfig(Config):
    """configuration for the production environment"""
    DB_NAME = os.getenv('DB_NAME')
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}