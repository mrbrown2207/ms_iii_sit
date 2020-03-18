import os

class ConfigTestEnv:
    DEV = True
    TESTING = True
    HOST = os.getenv('DB_HOST')
    DB = "sitDb"
    DB_USER = os.getenv('DB_USER')
    DB_ABTRUSUS = os.getenv('DB_ABTRUSUS')
    CHARSET = 'utf8'  
    SECRET_KEY = 'mysecretthatisnotsecret'

class Config:
    TESTING = False
    HOST = os.getenv('DB_HOST')
    DB = "sitDb"
    DB_USER = os.getenv('DB_USER')
    DB_ABTRUSUS = os.getenv('DB_ABTRUSUS')
    CHARSET = 'utf8'  
    SECRET_KEY = 'mysecretthatisnotsecret'
