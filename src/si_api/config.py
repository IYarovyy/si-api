class Config:
    BASE_DIR = '/Users/ihor/prj/si/si-api/'
    DEBUG = False
    TESTING = False
    RUN_EVOLUTION = True
    EVOLUTION_DIR = '../evolutions'
    DB_URL = ''
    DB_USER = ''
    DB_PWD = ''
    JWT_SECRET_KEY = "dsbkdjbfkjdkgjfnkjbnj ljhkm;l,h;lghmbc.vmcs m"
    PREDICT_MODEL_DIR = BASE_DIR + "src/predict_models/"
    PREDICT_MODEL_DEFAULT = "best_model_mm.pt"
    PREDICT_SCALER_DEFAULT = "scaler_mm.pkl"


class Development(Config):
    DEBUG = True
    EVOLUTION_DIR = '/Users/ihor/prj/si/si-api/src/evolutions'
    DB_URL = 'postgresql://localhost:5432/ihor'
    DB_USER = ''
    DB_PWD = ''
    OPENAPI_VERSION = '0.1.0'
    OPENAPI_SERVER = [{"url": 'http://localhost:5000'}]


class Production(Config):
    RUN_EVOLUTION = True
