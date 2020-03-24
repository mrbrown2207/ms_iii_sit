import datetime
import pymysql
import pymysql.cursors
from flask import (Blueprint, Flask, current_app, redirect, render_template,
                   request, url_for)
from ms_iii_sit.constants import DDMMYYYY_FMT, SQL_DICT, SQL_DT_FMT, ISSUE_STATUS
from .utils import *

main = Blueprint('main', __name__)

# main page
@main.route('/')
def index():
    """
    The number of categories can change. Therefore, what gets displayed in
    the filter modal should be dynamic. To that end, I am loading this into the app
    config if it doesn't already exist. Seems like there should be a better way,
    but this is going to have to do. I tried to put an __init__ method in the config
    class that gets loaded when creating the app (see __init__.py). However, it didn't 
    work; I am assuming it is because of the way the class is being instantiated.
    """
    if current_app.config.get("FILTER_STATE_DICT") == None:
        load_cats()            
        init_filter_state()

    """
    Issue statuses are not quite as dynamic as categories. However, let's
    still remain flexible and do the right thing so we don't have to  
    hard code stuff on the client side.
    """
    if current_app.config.get("ISS_STATUS") == None:
        current_app.config['ISS_STATUS'] = ISSUE_STATUS

    return render_template('index.html')

# <<<<<<<<<<<<<<<<<<<<-------------------- Issue Routes -------------------->>>>>>>>>>>>>>>>>>>>
@main.route('/get_issues', methods=["GET", "POST"])
def get_issues():

    if request.method == "POST":
        # Need this to be mutable...
        current_app.config['FILTER_STATE_DICT'] = request.form.to_dict()
        #... so we can do this...
        del current_app.config['FILTER_STATE_DICT']['submit-btn']

    filter_info = build_filter_sql(current_app.config['FILTER_STATE_DICT'])

    # Build our query based on the filters selected.
    qry = SQL_DICT['sel_filtered_isss'] % (filter_info['qry_str'])

    try:
        with get_db().cursor() as cur:
            cur.execute(qry)
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')

    return render_template('issues.html', issues=cur.fetchall(), omitted_status=filter_info['omitted_status'], omitted_cats=filter_info['omitted_cats'])


@main.route('/add_issue')
def add_issue():
    try:
        with get_db().cursor() as cur:
            cur.execute(SQL_DICT['sel_active_cats'])
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')


    return render_template('addissue.html', cats=cur.fetchall())

        
@main.route('/add_issue_todb', methods=['POST'])
def add_issue_todb():
    try:
        db = get_db()

        if current_app.config.get("NOLOGIN"):
            acctId = current_app.config.get("TESTACCTID")
        else:
            acctId = 99 # ˘L˘

        with db.cursor() as cur:
            # If the switch isn't on, then .get() will not find it. In that case set value to false.
            # The component returns 'on' or 'off'. We store as a boolean in the database.
            issue_urgent = request.form.get('is-urgent', False)
            if issue_urgent != False:
                issue_urgent = 1
            else:
                issue_urgent = 0
            cur.execute(SQL_DICT['add_iss'],
                            (request.form.get('iss-subj'),
                            request.form.get('iss-desc'),
                            int(request.form.get('cat-id')),
                            issue_urgent,
                            acctId)
                        )
            db.commit()
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')

    return redirect(url_for('main.get_issues'))

@main.route('/resolve_issue', methods=['POST'])
def resolve_issue():
    """
    Mark issue resolved. I tried to roll this all into upd_issue_status
    however my use of a modal for entering resolution details and the
    actual marking it as resolved, made is challenging. Thus, this. How funny! ˚L˘
    """
    try:
        db = get_db()

        if current_app.config.get("NOLOGIN"):
            acctId = current_app.config.get("TESTACCTID")
        else:
            acctId = 99 # ˘L˘

        with db.cursor() as cur:
            cur.execute(SQL_DICT['upd_resolve_iss'],
                        (
                            acctId,
                            request.form.get('iss-res-desc'),
                            ISSUE_STATUS['resolved'],
                            request.form.get('curr-iss-id')
                        )
                    )
            db.commit()
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')

    return redirect(url_for('main.get_issues'))


@main.route('/update_issue/<issue_id>', methods=['POST'])
def update_issue(issue_id):
    try:
        db = get_db()

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
            resolved_dt = datetime.datetime.now().strftime(SQL_DT_FMT)
            resolved_by = 1 #Temporary
            resolution_desc = request.form.get('resolution_desc')
        else:
            issue_resolved = resolved_by = 0
            resolved_dt = resolution_desc = ''

        with db.cursor() as cur:
            cur.execute(SQL_DICT['upd_iss'],
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
        print("Error: {}".format(str(e)))
    finally:
        print('Success')
    
    return redirect(url_for('main.get_issues'))

@main.route('/upd_issue_status/<issue_id>/<issue_status>')
def upd_issue_status(issue_id, issue_status):
    try:
        db = get_db()

        with db.cursor() as cur:
            if int(issue_status) == ISSUE_STATUS['notviewed']['id']:
                cur.execute(SQL_DICT['upd_iss_reset'], (issue_id))
            else:
                cur.execute(SQL_DICT['upd_iss_status'], (issue_status, issue_id))
            db.commit()
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print("Status update successful")

    return redirect(url_for('main.get_issues'))

@main.route('/edit_issue/<issue_id>')
def edit_issue(issue_id):
    try:
        db = get_db()

        with db.cursor() as cur:
            cur.execute(SQL_DICT['sel_iss_rec'], (issue_id))
            row = cur.fetchone()
            print(row)
            
            # Get the categories so we can default to the correct one
            # as well as make available for change
            all_cats = get_all_recs('tblCat')
            
            # Format our dates
            row['dateAdded'] = row['dateAdded'].strftime(DDMMYYYY_FMT)
            if row['viewed']:
                row['dateViewed'] = row['dateViewed'].strftime(DDMMYYYY_FMT)
            else:
                row['dateViewed'] = ''
            if row['resolved']:
                row['dateResolved'] = row['dateResolved'].strftime(DDMMYYYY_FMT)
            else:
                row['dateResolved'] = ''
            
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')
        
    return render_template('editissue.html', issue=row, cats=all_cats)


@main.route('/delete_issue/<issue_id>')
def delete_issue(issue_id):
    del_rec('tblIssue', issue_id)
    return redirect(url_for('main.get_issues'))
# <<<<<<<<<<<<<<<<<<<<---------------- End of Issue Routes ---------------->>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<-------------------- Category Routes -------------------->>>>>>>>>>>>>>>>>>>>
@main.route('/add_cat')
def add_cat():
    return render_template('addcat.html')


@main.route('/get_cats')
def get_cats():
    return render_template('categories.html', cats=get_all_recs('tblCat'))


@main.route('/update_cat/<cat_id>', methods=['POST'])
def update_cat(cat_id):
    try:
        db = get_db()

        with db.cursor() as cur:
            cur.execute(SQL_DICT['upd_cat'], (request.form.get('cat_name'), request.form.get('cat_desc'), cat_id))
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')
    
    return redirect(url_for('main.get_cats'))


@main.route('/add_cat_todb', methods=['POST'])
def add_cat_todb():
    try:
        db = get_db()

        with db.cursor() as cur:
            cur.execute(SQL_DICT['add_cat'], (request.form.get('cat_name'), request.form.get('cat_desc')))
            
            db.commit()
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')

    return redirect(url_for('main.get_cats'))


@main.route('/edit_cat/<cat_id>')
def edit_cat(cat_id):
    try:
        db = get_db()

        with db.cursor() as cur:
            cur.execute(SQL_DICT['sel_cat_rec'], (cat_id))
            row = cur.fetchone()
            print(row)
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')

    return render_template('editcat.html', cat=row)


@main.route('/delete_cat/<cat_id>')
def delete_cat(cat_id):
    del_rec('tblCat', cat_id)
    return redirect(url_for('main.get_cats'))
# <<<<<<<<<<<<<<<<<<<<---------------- End of Category Routes ---------------->>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<-------------------- User/Profile Routes -------------------->>>>>>>>>>>>>>>>>>>>
@main.route('/add_acct')
def add_acct():
    return render_template('addacct.html')

@main.route('/')
@main.route('/get_accts')
def get_accts():
    return render_template('accts.html', cats=get_all_recs('tblAccounts'))


@main.route('/update_acct/<acct_id>', methods=['POST'])
def update_acct(acct_id):
    try:
        db = get_db()

        with db.cursor() as cur:
            cur.execute(SQL_DICT['upd_acct'], (request.form.get('acct_name'), request.form.get('cat_desc'), acct_id))
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')
    
    return redirect(url_for('main.get_accts'))


@main.route('/insert_cat', methods=['POST'])
def insert_acct():
    try:
        db = get_db()

        with db.cursor() as cur:
            cur.execute(SQL_DICT['add_cat'], (request.form.get('cat_name'), request.form.get('cat_desc')))
            
            db.commit()
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')

    return redirect(url_for('main.get_accts'))


@main.route('/edit_acct/<acct_id>')
def edit_acct(acct_id):
    try:
        db = get_db()

        with db.cursor() as cur:
            cur.execute(SQL_DICT['sel_int_rec'], (acct_id))
            row = cur.fetchone()
            print(row)
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        print('Success')

    return render_template('editacct.html', acct=row)


@main.route('/delete_acct/<acct_id>')
def delete_int(acct_id):
    del_rec('tblAccounts', acct_id)
    return redirect(url_for('main.get_accts'))
# <<<<<<<<<<<<<<<<<<<<---------------- End of User/Profile Routes ---------------->>>>>>>>>>>>>>>>>>>>

@main.route('/howitworks')
def howitworks():
    return render_template('howitworks.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')
