import pymysql, random
import pymysql.cursors
from flask import Flask, session
from ms_iii_sit import login_manager
from ..constants import SQL_DICT, NO_BOTS
from ..main.utils import get_db
from . models import User


def get_user(id):
    with get_db().cursor() as cur:
        cur.execute(SQL_DICT['sel_acct_rec_by_id'], (id))
        row = cur.fetchone()

    if (row):
        user = User(row)
    else:
        user = None

    return user


@login_manager.user_loader
def load_user(id):
    return get_user(id)


def gen_bot_test():
    """
    Generate a random question that helps to prevent robots from creating accounts.
    In the real world the result stored in the session would be encrypted and
    then decrypted when verifying.
    """
    session['botq'], session['bota'] = random.choice(list(NO_BOTS.items()))

def clr_bot_session_qa():
    session.pop('botq', None)
    session.pop('bota', None)
    session.pop('failed_bota_count', None)
