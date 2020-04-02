import os

class ConfigDevEnv:
    DEV = True
    TESTING = True
    NOLOGIN = True
    TESTACCTID = 1
    PWD_FAILURES_ALLOWED = 2
    BOT_FAILURES_ALLOWED = 2
    DEFAULT_ISO = 'GB'
    HOST = os.getenv('DB_HOST')
    DB = os.getenv('DB')
    DB_USER = os.getenv('DB_USER')
    DB_ABTRUSUS = os.getenv('DB_ABTRUSUS')
    CHARSET = 'utf8'  
    SECRET_KEY = os.getenv('SIT_SECRET_KEY')


class Config:
    DEV = False
    TESTING = False
    PWD_FAILURES_ALLOWED = 3
    BOT_FAILURES_ALLOWED = 5
    DEFAULT_ISO = 'IE'
    HOST = os.getenv('DB_HOST')
    DB = os.getenv('DB')
    DB_USER = os.getenv('DB_USER')
    DB_ABTRUSUS = os.getenv('DB_ABTRUSUS')
    CHARSET = 'utf8'  
    SECRET_KEY = os.getenv('SIT_SECRET_KEY')
