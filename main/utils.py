import pymysql
import pymysql.cursors
from flask import current_app, g
from ms_iii_sit.constants import SQL_DICT

qry_testing = 0
issue_testing = 1
acctId = 2

def get_db():
    print("In get_db()")
    if 'db' not in g:
        print("do not have a db")
        # Connect to the database
        g.db = pymysql.connect(host=current_app.config.get('HOST'),
                                user=current_app.config.get('DB_USER'),
                                password=current_app.config.get('DB_ABTRUSUS'),
                                db=current_app.config.get('DB'),
                                charset=current_app.config.get('CHARSET'),
                                cursorclass=pymysql.cursors.DictCursor)

        print("connected to database")

    return g.db

def get_all_recs(tbl):
    try:
        db = get_db()

        if tbl == 'tblCat':
            if qry_testing:
                sql = SQL_DICT['sel_recs']
            else:
                sql = SQL_DICT['sel_all_cats']
        else:
            sql = SQL_DICT['sel_all_isss']
            
        with db.cursor() as cur:
            if qry_testing:
                print("I am query testing")
                print("sql = " + sql)
                cur.execute(sql, tbl)
            else:
                cur.execute(sql)

            return cur.fetchall()
    except Exception as e:
        print('query string: {}'.format(str(e)))
    finally:
        print('Success')


def del_rec(tbl, rec_id):
    try:
        db = get_db()

        if tbl == 'tblCat':
            sql = SQL_DICT['del_cat_rec']
        else:
            sql = SQL_DICT['del_iss_rec']
            
        with db.cursor() as cur:
            cur.execute(sql, (rec_id))
            db.commit()
            
    except Exception as e:
        print(e)
    finally:
        print('Success')
