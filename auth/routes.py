import pymysql
import pymysql.cursors
from flask import Flask, Blueprint, render_template, redirect, request, url_for, flash
from flask_login import (LoginManager, login_user, confirm_login,
                            logout_user, login_required, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from . models import User
from . utils import load_user
from ..main.utils import get_db
from ..constants import SQL_DICT


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


@auth.route("/logout")
@login_required
def logout():
    flash("Good bye %s!" % (current_user.name.split(" ")[0]), "success")
    logout_user()
    return redirect(url_for("main.index"))
