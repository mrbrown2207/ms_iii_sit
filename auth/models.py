from flask_login import UserMixin
from ..constants import USER_LEVEL


class User(UserMixin):
    def __init__(self, user):
        self.name = user["firstName"] + " " + user["surname"]
        self.id = user["acctId"]
        self.email = user["email"]
        self.active = user["isActive"]
        self.maudindo = user["maudindo"]

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True
    
    def is_superuser(self):
        return self.maudindo == USER_LEVEL['superuser']