import os
basedir=os.path.abspath(os.path.dirname(__name__))
class Config():
    FLASK_APP=os.path.join(basedir,'btech','run.py')
    SECRET_KEY ='20661143fd81501206948abe1df6ce38'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Dev_config(Config):
    # MAIL_USE_TLS=True
    MAIL_PORT=8025
    MAIL_SERVER='localhost'
    # MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'site-db.sqlite')
    DEBUG=True
class Testing_config(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'dev-db.sqlite')
class Production_config():
    pass

configs={
    'development':Dev_config,
    'testing':Testing_config,
    'production':Production_config,
    'default':Config
    
}