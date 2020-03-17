import pymysql
from flask import current_app
from ms_iii_sit.constants import SQL_DICT

qry_testing = 0
issue_testing = 1
acctId = 2

# Connect to the database
conn = pymysql.connect(host=current_app.config('HOST'),
                        user=current_app.config('DB_USER'),
                        password=current_app.config('DB_ABTRUSUS'),
                        db=current_app.config('DB'),
                        charset=current_app.config('CHARSET'),
                        cursorclass=pymysql.cursors.DictCursor)

def get_all_recs(tbl):
    try:
        if tbl == 'tblCat':
            if qry_testing:
                sql = SQL_DICT['sel_recs']
            else:
                sql = SQL_DICT['sel_all_cats']
        else:
            sql = SQL_DICT['sel_all_isss']
            
        with conn.cursor() as cur:
            if qry_testing:
                print("I am query testing")
                print("sql = " + sql)
                ret_values = cur.execute(sql, tbl)
            else:
                ret_values = cur.execute(sql)

            return cur.fetchall()
    except Exception as e:
        print('query string: {}'.format(str(e)))
    finally:
        print('Success')


def del_rec(tbl, rec_id):
    try:
        if tbl == 'tblCat':
            sql = SQL_DICT['del_cat_rec']
        else:
            sql = SQL_DICT['del_iss_rec']
            
        with conn.cursor() as cur:
            cur.execute(sql, (rec_id))
            conn.commit()
            
    except Exception as e:
        print(e)
    finally:
        print('Success')
