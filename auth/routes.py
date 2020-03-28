import pymysql
import pymysql.cursors
from flask import (Flask, Blueprint, render_template, current_app,
                    redirect, request, url_for, flash, session)
from flask_login import (LoginManager, login_user, confirm_login,
                            logout_user, login_required, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from . models import User
from . utils import load_user, gen_bot_test, clr_bot_session_qa
from ..main.utils import get_db
from ..constants import SQL_DICT, USER_LEVEL


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


@auth.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("main.index"))
    return render_template("reauth.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_data = request.form.to_dict()
        if form_data['nobota'] != session['bota']:
            session['failed_bota_count'] += 1
            if session['failed_bota_count'] < current_app.config.get('BOT_FAILURES_ALLOWED'):
                # Generate a new question and flash the error.
                gen_bot_test()
                flash("Robot challenge answer incorrect. Are you part of Skynet? (%d of %d)" % (session['failed_bota_count'], current_app.config.get('BOT_FAILURES_ALLOWED')), "danger")
            else:
                clr_bot_session_qa()
                flash("Robot challenge failed. You are part of Skynet!", "danger")
                return redirect(url_for("main.index"))
        else:
            try:
                db = get_db()

                with db.cursor() as cur:
                    cur.execute(SQL_DICT['add_account'], 
                                    (form_data['email'],
                                    form_data['surname'],
                                    form_data['first-name'],
                                    generate_password_hash(form_data['pwd']))
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
    pass

@auth.route("/logout")
@login_required
def logout():
    flash("Good bye %s!" % (current_user.name.split(" ")[0]), "success")
    logout_user()
    return redirect(url_for("main.index"))
