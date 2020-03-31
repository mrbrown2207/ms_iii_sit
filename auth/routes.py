import pymysql
from flask import (Flask, Blueprint, render_template, current_app,
                    redirect, request, url_for, flash, session)
from flask_login import (LoginManager, login_user, confirm_login,
                            logout_user, login_required, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from . models import User
from . utils import load_user, gen_bot_test, clr_bot_session_qa
from ..main.utils import get_db
from ..constants import SQL_DICT, USER_LEVEL, COUNTRIES


auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]

        try:
            with get_db().cursor() as cur:
                cur.execute(SQL_DICT['sel_acct_rec'], (email))
                row = cur.fetchone()

            if row == None:
                flash("User not found!", "danger")
            else:
                if check_password_hash(row['abtrusus'], request.form["password"]):
                    auth_user = User(row)
    
                    # Pylint says that auth_user.is_active() is not callable. Yet, I can
                    # call it and I receive no runtime errors. ˘L˘
                    if not auth_user.is_active():
                        flash("This account has been disabled.", "danger")
                        return render_template("login.html")

                    if login_user(auth_user, remember=True): # This is what calls load_user()
                        if current_user.is_superuser():
                            flash("Welcome back %s! You have superuser rights." % (row['firstName']), "success")
                        else:
                            flash("Welcome back %s!" % (row['firstName']), "success")
                    else:
                        flash("Unable to log you in.", "danger")
                else:
                    flash("Login failed due to invalid password.", "danger")
                    return render_template("login.html")

            return redirect(url_for("main.index"))
        except Exception as e:
            flash("Unexpected error. Unable to log you in.", "danger")
            print("Error: {}".format(str(e)))
        finally:
            pass

    return render_template("login.html")

"""
Unused now, but leaving it in for later enhancements

@auth.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("main.index"))
    return render_template("reauth.html")
"""

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_data = request.form.to_dict()
        if form_data['nobota'] != session['bota']:
            session['failed_bota_count'] += 1
            if session['failed_bota_count'] < current_app.config['BOT_FAILURES_ALLOWED']:
                # Generate a new question and flash the error.
                gen_bot_test()
                flash("Robot challenge answer incorrect. Are you part of Skynet? (%d of %d)" % (session['failed_bota_count'], current_app.config['BOT_FAILURES_ALLOWED']), "danger")
            else:
                clr_bot_session_qa()
                flash("Robot challenge failed. You are part of Skynet!", "danger")
                return redirect(url_for("main.index"))
        else:
            try:
                db = get_db()

                with db.cursor() as cur:
                    cur.execute(SQL_DICT['add_account'], 
                                    (
                                    form_data['email'],
                                    form_data['surname'],
                                    form_data['first-name'],
                                    generate_password_hash(form_data['pwd']),
                                    current_app.config['DEFAULT_ISO']
                                    )
                                )
                db.commit()

                # Let's log the user in now
                user = User({
                                "firstName": form_data['first-name'],
                                "surname": form_data['surname'],
                                "email": form_data['email'],
                                "acctId": cur.lastrowid,
                                "isActive": 1,
                                "maudindo": USER_LEVEL['plebe']
                            })
                login_user(user)
                clr_bot_session_qa()
                flash("Welcome to the MBPM community {}!".format(form_data['first-name']), "success")
                return redirect(url_for("main.index"))
            except (db.Error) as e:
                # Duplicate entry
                if e.args[0] == 1062:
                    flash(u"That account already exists.", "danger")
                else:
                    flash(u"Database error. Unable to create account.", "danger")
                    print("Error: {}".format(str(e)))

                return render_template("register.html")
            except Exception as e:
                flash(u"Account created but there was an error during authentication.", "warning")
                print("Error: {}".format(str(e)))
            finally:
                pass

    else:
        # Generate our bot question and answer.
        session['failed_bota_count'] = 0
        gen_bot_test()

    return render_template("register.html")

@auth.route("/profile", methods=["GET", "POST"])
def profile():
    
    db = get_db()
    
    if request.method == "POST":
        form_data = request.form.to_dict()

        try:
            # I always try to minimise the exposure of passwords. To that end,
            # I don't retrieve the password when rendering the template (GET)
            # thereby not requiring it in the update statement. However, if the
            # user does change their password, then we use a different sql statement.
            if form_data['pwd-changed'] == "0":
                with db.cursor() as cur:
                    cur.execute(SQL_DICT['upd_profile'],
                                (
                                    form_data['first-name'],
                                    form_data['surname'],
                                    form_data['addr-line1'],
                                    form_data['addr-line2'],
                                    form_data['city'],
                                    form_data['county'],
                                    form_data['country-iso'],
                                    form_data['postcode'],
                                    form_data['mobile'],
                                    form_data['other-phone'],
                                    current_user.id
                                ))
            else:
                with db.cursor() as cur:
                    cur.execute(SQL_DICT['upd_profile_abtrusus'],
                                (
                                    form_data['first-name'],
                                    form_data['surname'],
                                    form_data['addr-line1'],
                                    form_data['addr-line2'],
                                    form_data['city'],
                                    form_data['county'],
                                    form_data['country-iso'],
                                    form_data['postcode'],
                                    form_data['mobile'],
                                    form_data['other-phone'],
                                    generate_password_hash(form_data['pwd-1']),
                                    current_user.id
                                ))
            db.commit()
            flash(u"Profile updated.", "success")
            return redirect(url_for("main.index"))
        except (db.Error) as e:
            flash(u"Database error. Unable to update profile.", "danger")
            print("Error: {}".format(str(e)))

            return redirect(url_for("main.index"))
        except Exception as e:
            flash(u"Unexpected error. Unable to update profile.", "danger")
            print("Error: {}".format(str(e)))
        finally:
            pass

    else:
        with db.cursor() as cur:
            cur.execute(SQL_DICT['sel_profile'], (current_user.id))
            row = cur.fetchone()

            if row == None:
                flash("Unexpected error. Unable to locate account record.", "danger")
                return redirect(url_for("main.index"))

            # Seems like there should be a more pythonic way to do this. ˘L˘
            for k in row:
                if row[k] == None:
                    row[k] = ""

            # Get our dictionary of countries and sort them
            countries = sorted((v, k) for (k, v) in COUNTRIES.items())

    return render_template("profile.html", user=row, countries=countries)

@auth.route("/logout")
@login_required
def logout():
    flash("Good bye %s!" % (current_user.name.split(" ")[0]), "success")
    logout_user()
    return redirect(url_for("main.index"))


# <<<<<<<<<<<<<<<<<<<<-------------------- User/Profile Routes -------------------->>>>>>>>>>>>>>>>>>>>
"""
This is unused code. However, I am leaving it in as the application can easily be enhanced
to allow an administrator to do more managing of accounts. It is not needed for the application
as it is right now. Well, it would be good to have it, but just running out of time. I do plan
to go back to this, fork it and make it more robust.

I actually envision an administration blueprint where all admin functionality would reside. This would 
go there as opposed to here. If an administrator logs in -- the maudindo field of the tblAccounts record
= to 255 -- then there would be an administrator menu item with drop down admin items: Manager Users, Categories, etc.

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
        pass
    
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
        pass

    return render_template('editacct.html', acct=row)


@main.route('/delete_acct/<acct_id>')
def delete_int(acct_id):
    del_rec('tblAccounts', acct_id)
    return redirect(url_for('main.get_accts'))
"""
# <<<<<<<<<<<<<<<<<<<<---------------- End of User/Profile Routes ---------------->>>>>>>>>>>>>>>>>>>>
