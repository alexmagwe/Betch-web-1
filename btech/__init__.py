#!/usr/bin/python3
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from btech.config import Config



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
admin = Admin(name='Admin Panel')
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from btech.users.routes import users
    from btech.admins.routes import admins
    from btech.blogs.routes import blogs
    from btech.store.routes import store
    from btech.comments.routes import comments
    from btech.main.routes import main
    from btech.errors.handlers import errors
    app.register_blueprint(errors)
    app.register_blueprint(admins)
    app.register_blueprint(blogs)
    app.register_blueprint(users)
    app.register_blueprint(store)
    app.register_blueprint(comments)
    app.register_blueprint(main)

    return app
