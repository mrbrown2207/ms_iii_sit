
from flask import Flask
from flask_login import LoginManager
from . config import ConfigDevEnv


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "auth.reauth"

def create_app(config_class=ConfigDevEnv):
    app = Flask(__name__)
    app.config.from_object(ConfigDevEnv)

    login_manager.init_app(app)

    from . main.routes import main 
    from . auth.routes import auth
    from . content.routes import content
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(content)

    return app
