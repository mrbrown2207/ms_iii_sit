
from flask import Flask
from flask_login import LoginManager
from . config import ConfigTestEnv


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "auth.reauth"

def create_app(config_class=ConfigTestEnv):
    app = Flask(__name__)
    app.config.from_object(ConfigTestEnv)

    login_manager.init_app(app)

    from ms_iii_sit.main.routes import main 
    from ms_iii_sit.auth.routes import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
