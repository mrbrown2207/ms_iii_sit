import os
import pymysql
import pymysql.cursors
import unittest
import flask_testing

class MyTest(unittest.TestCase):

    # Existence of environment variables tests
    def test_env_var_DB_exists(self):
        assert os.getenv('DB') is not None

    def test_env_var_DB_ABTRUSUS_exists(self):
        assert os.getenv('DB_ABTRUSUS') is not None

    def test_env_var_DB_HOST_exists(self):
        assert os.getenv('DB_HOST') is not None

    def test_env_var_DB_USER_exists(self):
        assert os.getenv('DB_USER') is not None

    def test_env_var_FLASK_APP_HOST_exists(self):
        assert os.getenv('FLASK_APP_HOST') is not None

    def test_env_var_FLASK_APP_PORT_exists(self):
        assert os.getenv('FLASK_APP_PORT') is not None

    def test_env_var_SIT_SECRET_KEY_exists(self):
        assert os.getenv('SIT_SECRET_KEY') is not None

    # DB connection test
    def test_db_connection(self):
        db_conn = pymysql.connect(host=os.getenv('DB_HOST'),
                                user=os.getenv('DB_USER'),
                                password=os.getenv('DB_ABTRUSUS'),
                                db=os.getenv('DB'),
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)
        if db_conn.open:
            x = True
            db_conn.close()
        else:
            x = False

        assert(x)


if __name__ == '__main__':
    unittest.main()