from ms_iii_sit import login_manager
from ms_iii_sit.constants import SQL_DICT
from ms_iii_sit.main.utils import get_db
from . models import User 

@login_manager.user_loader
def load_user(email_addr):
    try:
        db = get_db()
        with db.cursor() as cur:
            cur.execute(SQL_DICT['sel_acct_rec'], (email_addr))
            row = cur.fetchone()

            # Establish a user manager object/session
            return User(row)

    except Exception as e:
        print(e)
    finally:
        print(row)
        print('Success')
        return row
