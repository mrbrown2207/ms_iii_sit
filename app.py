import os
from flask import Flask, render_template, redirect, request, url_for
import pymysql
import pymysql.cursors
import datetime
import constants

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')

# Connect to the database
conn = pymysql.connect(host=os.getenv('DB_HOST'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_ABTRUSUS'),
                        db=app.config['DB'],
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)

qry_testing = 0
issue_testing = 1
acctId = 2


def get_all_recs(tbl):
    try:
        if tbl == 'tblCat':
            if qry_testing:
                sql = constants.SQL_DICT['sel_recs']
            else:
                sql = constants.SQL_DICT['sel_all_cats']
        else:
            sql = constants.SQL_DICT['sel_all_isss']
            
        with conn.cursor() as cur:
            if qry_testing:
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
            sql = constants.SQL_DICT['del_cat_rec']
        else:
            sql = constants.SQL_DICT['del_iss_rec']
            
        with conn.cursor() as cur:
            cur.execute(sql, (rec_id))
            conn.commit()
            
    except Exception as e:
        print(e)
    finally:
        print('Success')


"""<<<<<<<<<<<<<<<<<<<<--------------------Issue Routines-------------------->>>>>>>>>>>>>>>>>>>>"""
#@app.route('/')
@app.route('/get_issues')
def get_issues():
    issues = get_all_recs('tblIssue')
    
    for row in issues:
        print(row)

    return render_template('issues.html', issues=get_all_recs('tblIssue'))


@app.route('/add_issue')
def add_issue():
    return render_template('addissue.html', cats=get_all_recs('tblCat'))

        
@app.route('/insert_issue', methods=['POST'])
def insert_issue():
    try:
        with conn.cursor() as cur:
            # If the switch isn't on, then .get() will not find it. In that case set value to false.
            # The component returns 'on' or 'off'. We store as a boolean in the database.
            issue_urgent = request.form.get('is_urgent', False)
            if issue_urgent != False:
                issue_urgent = 1
            else:
                issue_urgent = 0

            cur.execute(constants.SQL_DICT['add_iss'],
                            (request.form.get('issue_subj'),
                            request.form.get('issue_desc'),
                            request.form.get('cat_id'),
                            issue_urgent,
                            acctId)
                            #request.form.get('acct_id', 'Michael')
                        )
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        print('Success')

    return redirect(url_for('get_issues'))


@app.route('/update_issue/<issue_id>', methods=['POST'])
def update_issue(issue_id):
    try:
        # If the switch isn't on, then .get() will not find it. In that case set value to false.
        # The component returns 'on' or 'off'. We store as a boolean in the database.
        issue_urgent = request.form.get('urgent', False)
        if issue_urgent != False:
            issue_urgent = 1
        else:
            issue_urgent = 0
            
        issue_resolved = request.form.get('resolved', False)
        if issue_resolved != False:
            issue_resolved = 1
            resolved_dt = datetime.datetime.now().strftime(constants.SQL_DT_FMT)
            resolved_by = 1 #Temporary
            resolution_desc = request.form.get('resolution_desc')
        else:
            issue_resolved = resolved_by = 0
            resolved_dt = resolution_desc = ''

        with conn.cursor() as cur:
            cur.execute(constants.SQL_DICT['upd_iss'],
                            request.form.get('issue_subj'),
                            request.form.get('issue_desc'),
                            request.form.get('cat_id'),
                            issue_urgent,
                            issue_resolved,
                            resolved_by,
                            resolved_dt,
                            resolution_desc,
                            issue_id
                        )
    except Exception as e:
        print(e)
    finally:
        print('Success')
    
    return redirect(url_for('get_issues'))


@app.route('/edit_issue/<issue_id>')
def edit_issue(issue_id):
    try:
        with conn.cursor() as cur:
            ret_val = cur.execute(constants.SQL_DICT['sel_iss_rec'], (issue_id))
            row = cur.fetchone()
            print(row)
            
            # Get the categories so we can default to the correct one
            # as well as make available for change
            all_cats = get_all_recs('tblCat')
            
            # Format our dates
            row['dateAdded'] = row['dateAdded'].strftime(constants.DDMMYYYY_FMT)
            if row['viewed']:
                row['dateViewed'] = row['dateViewed'].strftime(constants.DDMMYYYY_FMT)
            else:
                row['dateViewed'] = ''
            if row['resolved']:
                row['dateResolved'] = row['dateResolved'].strftime(constants.DDMMYYYY_FMT)
            else:
                row['dateResolved'] = ''
            
    except Exception as e:
        print(e)
    finally:
        print('Success')
        
    return render_template('editissue.html', issue=row, cats=all_cats)


@app.route('/delete_issue/<issue_id>')
def delete_issue(issue_id):
    del_rec('tblIssue', issue_id)
    return redirect(url_for('get_issues'))
""" <<<<<<<<<<<<<<<<<<<<----------------End of Issue Routines---------------->>>>>>>>>>>>>>>>>>>>"""


""" <<<<<<<<<<<<<<<<<<<<--------------------Category Routines-------------------->>>>>>>>>>>>>>>>>>>>"""
@app.route('/add_cat')
def add_cat():
    return render_template('addcat.html')

@app.route('/')
@app.route('/get_cats')
def get_cats():
    return render_template('categories.html', cats=get_all_recs('tblCat'))


@app.route('/update_cat/<cat_id>', methods=['POST'])
def update_cat(cat_id):
    try:
        with conn.cursor() as cur:
            cur.execute(constants.SQL_DICT['upd_cat'], (request.form.get('cat_name'), request.form.get('cat_desc'), cat_id))
    except Exception as e:
        print(e)
    finally:
        print('Success')
    
    return redirect(url_for('get_cats'))


@app.route('/insert_cat', methods=['POST'])
def insert_cat():
    try:
        with conn.cursor() as cur:
            cur.execute(constants.SQL_DICT['add_cat'], (request.form.get('cat_name'), request.form.get('cat_desc')))
            
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        print('Success')

    return redirect(url_for('get_cats'))


@app.route('/edit_cat/<cat_id>')
def edit_cat(cat_id):
    try:
        with conn.cursor() as cur:
            ret_val = cur.execute(constants.SQL_DICT['sel_cat_rec'], (cat_id))
            row = cur.fetchone()
            print(row)
    except Exception as e:
        print(e)
    finally:
        print('Success')

    return render_template('editcat.html', cat=row)


@app.route('/delete_cat/<cat_id>')
def delete_cat(cat_id):
    del_rec('tblCat', cat_id)
    return redirect(url_for('get_cats'))
""" <<<<<<<<<<<<<<<<<<<<----------------End of Category Routines---------------->>>>>>>>>>>>>>>>>>>>"""


""" <<<<<<<<<<<<<<<<<<<<--------------------User/Profile Routines-------------------->>>>>>>>>>>>>>>>>>>>"""
@app.route('/add_acct')
def add_acct():
    return render_template('addacct.html')

@app.route('/')
@app.route('/get_accts')
def get_accts():
    return render_template('accts.html', cats=get_all_recs('tblAccounts'))


@app.route('/update_acct/<acct_id>', methods=['POST'])
def update_acct(acct_id):
    try:
        with conn.cursor() as cur:
            cur.execute(constants.SQL_DICT['upd_acct'], (request.form.get('acct_name'), request.form.get('cat_desc'), acct_id))
    except Exception as e:
        print(e)
    finally:
        print('Success')
    
    return redirect(url_for('get_accts'))


@app.route('/insert_cat', methods=['POST'])
def insert_acct():
    try:
        with conn.cursor() as cur:
            cur.execute(constants.SQL_DICT['add_cat'], (request.form.get('cat_name'), request.form.get('cat_desc')))
            
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        print('Success')

    return redirect(url_for('get_accts'))


@app.route('/edit_acct/<acct_id>')
def edit_acct(acct_id):
    try:
        with conn.cursor() as cur:
            ret_val = cur.execute(constants.SQL_DICT['sel_int_rec'], (acct_id))
            row = cur.fetchone()
            print(row)
    except Exception as e:
        print(e)
    finally:
        print('Success')

    return render_template('editacct.html', acct=row)


@app.route('/delete_acct/<acct_id>')
def delete_int(acct_id):
    del_rec('tblAccounts', acct_id)
    return redirect(url_for('get_accts'))
""" <<<<<<<<<<<<<<<<<<<<----------------End of User/Profile Routines---------------->>>>>>>>>>>>>>>>>>>>"""


if __name__ == '__main__':
    print("here in main")
    app.run(debug=True)
    """
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
    """
    