import pymysql
import pymysql.cursors
from flask import current_app, g
from ms_iii_sit.constants import SQL_DICT, ISSUE_STATUS

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

def init_filter_state():
    try:
        with get_db().cursor() as cur:
            cur.execute(SQL_DICT['sel_all_cats_1'])

        cat_list = cur.fetchall()

        # Take our list and create a dictionary with it. Seems like there is a better
        # way to do this, but I couldn't find one ˘L˘
        current_app.config['FILTER_STATE_DICT'] = {}
        for row in cat_list:
            current_app.config['FILTER_STATE_DICT'].update({row['cat']:"1"})

        # Now add the issue statuses
        for v in ISSUE_STATUS.values():
            current_app.config['FILTER_STATE_DICT'].update({"status-%s" % v['id']:"1"})

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

def build_filter_sql(filter_state_dict):

    # We need to update the status of our app config status dictionary. Again,
    # I am sure there is a cooler more python-y way to do this. But the structure
    # of the ISS_STATUS dictionary makes it a bit challenging.
    status_dict = dict((k, v) for k, v in filter_state_dict.items() if "status" in k)
    for k in status_dict:
        status_id = int(k.split("-")[1])
        for k1, v in current_app.config['ISS_STATUS'].items():
            if v['id'] == status_id:
                current_app.config['ISS_STATUS'][k1]['filter_status'] = status_dict[k]    
    
    # Our categories list of dictionaries, so slightly different logic here.
    cats_dict = dict((k, v) for k, v in filter_state_dict.items() if "cat" in k)
    for k, v in cats_dict.items():
        cat_id = int(k.split("-")[1])
        for d in current_app.config['CATS']:
            d.update(("filter_status", v) for k1, v1 in d.items() if v1 == cat_id) 

    cats_filter_dict = dict((k, v) for k, v in cats_dict.items() if v == "1")
    status_filter_dict = dict((k, v) for k, v in status_dict.items() if v == "1")

    # We need this to maintain display correct state in UI
    omitted_cats_dict = dict((k, v) for k, v in cats_dict.items() if v == "0")
    omitted_status_dict = dict((k, v) for k, v in status_dict.items() if v == "0")

    x = 0
    sql_qry = "("
    for k in cats_filter_dict:
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

    return ({"qry_str":sql_qry, "omitted_cats":(len(omitted_cats_dict) > 0), "omitted_status":(len(omitted_status_dict) > 0)})
