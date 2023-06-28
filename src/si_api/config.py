class Config:
    DEBUG = False
    TESTING = False
    RUN_EVOLUTION = True
    EVOLUTION_DIR = '../evolutions'
    DB_URL = ''
    DB_USER = ''
    DB_PWD = ''
    JWT_SECRET_KEY = "dsbkdjbfkjdkgjfnkjbnj ljhkm;l,h;lghmbc.vmcs m"

class Development(Config):
    DEBUG = True
    EVOLUTION_DIR = '/Users/ihor/prj/si/si-api/src/evolutions'
    DB_URL = 'postgresql://localhost:5432/ihor'
    DB_USER = ''
    DB_PWD = ''


class Production(Config):
    RUN_EVOLUTION = True
