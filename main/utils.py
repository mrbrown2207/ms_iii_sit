import pymysql
import pymysql.cursors
from flask import current_app, g
from ms_iii_sit.constants import SQL_DICT

qry_testing = 0
issue_testing = 1
acctId = 2

def get_db():
    if 'db' not in g:
        # Connect to the database
        g.db = pymysql.connect(host=current_app.config.get('HOST'),
                                user=current_app.config.get('DB_USER'),
                                password=current_app.config.get('DB_ABTRUSUS'),
                                db=current_app.config.get('DB'),
                                charset=current_app.config.get('CHARSET'),
                                cursorclass=pymysql.cursors.DictCursor)
                                
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
                print("SQL: {}".format(sql))
                cur.execute(sql, tbl)
            else:
                cur.execute(sql)

            return cur.fetchall()
    except Exception as e:
        print('Error: {}'.format(str(e)))
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
        print('Error: {}'.format(str(e)))
    finally:
        print('Success')

def load_cats():
    try:
        with get_db().cursor() as cur:
            cur.execute(SQL_DICT['get_cats'])
            current_app.config['CATS'] = cur.fetchall()

    except Exception as e:
        print('Error: {}'.format(str(e)))
    finally:
        print('Success')

def build_filter_sql(form_dict):
    cat_filter_dict = dict((k, v) for k, v in form_dict.items() if "cat" in k and v == "1")
    status_filter_dict = dict((k, v) for k, v in form_dict.items() if "status" in k and v == "1")

    x = 0
    sql_qry = "("
    for k in cat_filter_dict:
        cat = "i.catId=%s" % (k.split("-")[1])
        if x > 0 :
            sql_qry += " or i.catId=%s" % (k.split("-")[1])
        else:
            sql_qry += cat

        x += 1

    sql_qry += ") and ("

    x = 0
    for k in status_filter_dict:
        status = "i.issueStatus=%s" % (k.split("-")[1])
        if x > 0 :
            sql_qry += " or i.issueStatus=%s" % (k.split("-")[1])
        else:
            sql_qry += status

        x += 1

    sql_qry += ")"

    return sql_qry
