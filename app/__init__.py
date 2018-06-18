from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

from config import config


pagedown = PageDown()
moment = Moment()
db = SQLAlchemy()
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login' #访问需要登录的页面自动跳转到/login
login_manager.login_message = '请先登录' #访问需要登录的页面自动跳转到/login页面时的falsh消息

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    pagedown.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from .main import views
    app.register_blueprint(views.main)
    from .auth import views
    app.register_blueprint(views.auth)
    return app



