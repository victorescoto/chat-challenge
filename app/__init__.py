import pathlib

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect

from .models import User
from .models import configure as config_db
from .serializers import configure as config_ma

socketio = SocketIO()
csrf = CSRFProtect()
login_manager = LoginManager()

login_manager.login_view = "main.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def load_blueprints(app):
    from .blueprints import main

    app.register_blueprint(main)


def create_app():
    app = Flask(__name__)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"sqlite:///{pathlib.Path().absolute()}/jobsity.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "any secret string"

    config_db(app)
    config_ma(app)

    Migrate(app, app.db)

    load_blueprints(app)

    login_manager.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app, manage_session=True)

    return app


app = create_app()

if __name__ == "__main__":
    socketio.run(app)
