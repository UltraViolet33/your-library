from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask import Flask
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_type=None):
    app = Flask(__name__)

    if config_type == None:
        config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")

    app.config.from_object(config_type)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.models.User import User
    from app.models.Book import Book 
    
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    from .auth import auth
    from .books import books
    from .lists import lists
    from .posts import posts


    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(books, url_prefix="/")
    app.register_blueprint(lists, url_prefix="/")
    app.register_blueprint(posts, url_prefix="/")
