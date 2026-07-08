from flask import Flask

from config import Config
from app.extensions import db, migrate, login_manager
from app import models


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    @app.route("/")
    def home():
        return "<h1>Donor Management System</h1>"

    return app