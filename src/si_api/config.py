class Config:
    DEBUG = False
    TESTING = False
    RUN_EVOLUTION = True
    EVOLUTION_DIR = '../evolutions'
    DB_URL = ''
    DB_USER = ''
    DB_PWD = ''


class Development(Config):
    DEBUG = True
    DB_URL = 'postgresql://localhost:5432/ihor'
    DB_USER = ''
    DB_PWD = ''


class Production(Config):
    RUN_EVOLUTION = True
