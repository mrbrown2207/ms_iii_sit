import pymysql
import pymysql.cursors
from ms_iii_sit import login_manager
from ..constants import SQL_DICT
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