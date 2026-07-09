from flask import Flask

from config import Config
from app.extensions import db, migrate, login_manager
from app import models
from app.models.user import User
from app.auth import auth
from app.dashboard import dashboard
from app.donors import donors
from app.donations import donations
from app.reports import reports

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(donors)
    app.register_blueprint(donations)
    app.register_blueprint(reports)
    @app.route("/")
    def home():
        return "<h1>Donor Management System</h1>"

    return app
    
    