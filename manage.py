import os
from flask_migrate import  MigrateCommand,Migrate
from flask_script import Shell,Manager
from app.models import User,Role,Category
from app.truncate import truncate_html
from app import create_app,db

app = create_app(os.getenv('BLOG_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)


env=app.jinja_env
env.filters['truncate_html'] = truncate_html

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Category=Category)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import Role,Category

    upgrade()

    Role.insert_roles()
    Category.insert_categorys()

if __name__ == '__main__':
    manager.run()