import os

class ConfigTestEnv:
    DEV = True
    TESTING = True
    NOLOGIN = True
    TESTACCTID = 1
    HOST = os.getenv('DB_HOST')
    DB = "sitDb"
    DB_USER = os.getenv('DB_USER')
    DB_ABTRUSUS = os.getenv('DB_ABTRUSUS')
    CHARSET = 'utf8'  
    SECRET_KEY = 'mysecretthatisnotsecret'

    def __init__(self):
        print("Init is called")

class Config:
    TESTING = False
    HOST = os.getenv('DB_HOST')
    DB = "sitDb"
    DB_USER = os.getenv('DB_USER')
    DB_ABTRUSUS = os.getenv('DB_ABTRUSUS')
    CHARSET = 'utf8'  
    SECRET_KEY = 'mysecretthatisnotsecret'
