from . import create_app,db
from flask_script import Shell,Manager
from flask_migrate import Migrate,MigrateCommand
from btech.models import User,Post,Component,Permissions,Request,Notification,Category

app = create_app()
manager=Manager(app)

@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Posts':Post,'Component':Component,'Caregory':Category,'Notification':Notification,'Request':Request,'Permissions':Permissions}

manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
