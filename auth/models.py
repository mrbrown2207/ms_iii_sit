from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_dict):
        self.name = user_dict.get("firstName") + " " + user_dict.get("surname")
        self.id = user_dict.get("acctId")
        self.email = user_dict.get("email")
        self.active = user_dict.get("acctDisabled")

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return True
    
