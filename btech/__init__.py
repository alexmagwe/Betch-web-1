from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin




app = Flask(__name__)
app.config['SECRET_KEY']='20661143fd81501206948abe1df6ce38'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
admin = Admin(app, name='Admin Panel')
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

from btech import routes
