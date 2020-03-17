import os

class Config:
    DEV = 1
    TESTING = True
    HOST = os.getenv('DB_HOST')
    DB = "sitDb"
    DB_USER = os.getenv('DB_USER')
    DB_ABTRUSUS = os.getenv('DB_ABTRUSUS')
    CHARSET = 'utf8'  
    SECRET_KEY = 'mysecretthatisnotsecret'
