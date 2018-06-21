import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SSL_DISABLE = True
    SECRET_KEY = 'HARD TO GUESS'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN = os.environ.get('ADMIN')
    MAIL_SUBJECT_PREFIX = '[李小离的博客]'
    MAIL_SENDER = 'Admin <1219800771@qq.com>'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_POSTS_PER_PAGE = 6
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data_test.sqlite')

class HerokuConfig(Config):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_POSTS_PER_PAGE = 6
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

config = {
    'development':DevelopmentConfig,
    'heroku' : HerokuConfig,
    'default': DevelopmentConfig,
}