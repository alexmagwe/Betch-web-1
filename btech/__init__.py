from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail 
from flask_admin import Admin
from btech.config import configs
from flask_bootstrap import Bootstrap



db = SQLAlchemy()
bcrypt = Bcrypt()
bootstrap=Bootstrap()
mail=Mail()

migrate=Migrate()
login_manager = LoginManager()
admin = Admin(name='Admin Panel')
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(configs['development'])
    migrate.init_app(app,db)
    db.init_app(app)
    bootstrap.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from btech.users import users
    from btech.admins import admins
    from btech.blogs import blogs
    from btech.store import store
    from btech.comments.routes import comments
    from btech.main import main
    from btech.errors.handlers import errors
    app.register_blueprint(errors)
    app.register_blueprint(admins,url_prefix='/admin')
    app.register_blueprint(blogs,url_prefix='/blog')
    app.register_blueprint(users)
    app.register_blueprint(store,url_prefix='/store')
    app.register_blueprint(comments)
    app.register_blueprint(main)

    return app
