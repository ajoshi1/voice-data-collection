import json
import os

class DefaultConfig(object):
    DEBUG = False

class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    DATABASE_URI = "postgresql://localhost:5432/soundc"
    PORT = 5000
    HOST = '127.0.0.1'

class ProductionConfig(DefaultConfig):
    DEBUG = True
    DATABASE_URI = ''
    if os.getenv("VCAP_SERVICES") is not None:
        DATABASE_URI = json.loads(os.getenv("VCAP_SERVICES"))["elephantsql"][0]["credentials"]["uri"]
    PORT=0
    if os.getenv("PORT") is not None:
        PORT = int(os.getenv("PORT"))
    HOST = '0.0.0.0'

class TestConfig(DefaultConfig):
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


config_env_files = {
    'test': 'ivr_phone_tree_python.config.TestConfig',
    'development': 'ivr_phone_tree_python.config.DevelopmentConfig',
    'production': 'ivr_phone_tree_python.config.ProductionConfig',
}
