import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'HARD TO GUESS'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN = os.environ.get('ADMIN')
    MAIL_SUBJECT_PREFIX = '[李小离的博客]'
    MAIL_SENDER = 'Admin <1219800771@qq.com>'

class DevelopmentConfig(Config):
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_POSTS_PER_PAGE = 6
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data_test.sqlite')


config = {
    'development':DevelopmentConfig,
    'default': DevelopmentConfig,
}