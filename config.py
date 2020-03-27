import os

class ConfigDevEnv:
    DEV = True
    TESTING = True
    NOLOGIN = True
    TESTACCTID = 1
    PWD_FAILURES_ALLOWED = 2
    BOT_FAILURES_ALLOWED = 2
    HOST = os.getenv('DB_HOST')
    DB = "sitDb"
    DB_USER = os.getenv('DB_USER')
    DB_ABTRUSUS = os.getenv('DB_ABTRUSUS')
    CHARSET = 'utf8'  
    SECRET_KEY = 'mysecretthatisnotsecret'

    def __init__(self):
        print("Init is called")

class Config:
    DEV = False
    TESTING = False
    PWD_FAILURES_ALLOWED = 3
    BOT_FAILURES_ALLOWED = 5
    HOST = os.getenv('DB_HOST')
    DB = "sitDb"
    DB_USER = os.getenv('DB_USER')
    DB_ABTRUSUS = os.getenv('DB_ABTRUSUS')
    CHARSET = 'utf8'  
    SECRET_KEY = 'mysecretthatisnotsecret'
