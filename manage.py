from flask_migrate import  MigrateCommand,Migrate
from flask_script import Shell,Manager

from app.models import User,Role,Category
from app.truncate import truncate_html
from app import create_app,db

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app,db)


env=app.jinja_env
env.filters['truncate_html'] = truncate_html

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Category=Category)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)




if __name__ == '__main__':
    manager.run()