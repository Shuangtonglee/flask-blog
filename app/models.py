import bleach
from . import db,login_manager
from flask import current_app
from flask_login import UserMixin
from _datetime import datetime
from markdown import markdown
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    user = db.relationship('User',backref='role')

    @staticmethod
    def insert_roles():
        roles = ['Admin','Moderator','User']
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            db.session.add(role)
        db.session.commit()


    def __repr__(self):
        return self.name


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    confirmed = db.Column(db.Boolean,default=False)
    comments = db.relationship('Comment',backref='author',lazy='dynamic')


    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(name='User').first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        token = s.dumps({'confirmed':self.id})
        return token

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirmed') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


    def generate_reset_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        token = s.dumps({'confirmed':self.id})
        return token

    def reset_password(self,token,new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirmed') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True



class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    picture = db.Column(db.String)
    category_id = db.Column(db.Integer,db.ForeignKey('categorys.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    views = db.Column(db.Integer,default=0)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    comments = db.relationship('Comment',backref='post',lazy='dynamic')

    def viewed(self):
        self.views +=1

    @staticmethod
    def on_change_body(target,value,oldvalue,initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value,output_format='html'),
                                                       tags=allowed_tags,strip=True))
db.event.listen(Post.body,'set',Post.on_change_body)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))

    def __repr__(self):
        return '<Comment %r>' % self.body


class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    posts = db.relationship('Post',backref='category',lazy='dynamic')


    @staticmethod
    def insert_categorys():
        categorys = ['Python','Spider','Front-end','Database','Essay']
        for c in categorys:
            category = Category.query.filter_by(name=c).first()
            if category is None:
                category = Category(name=c)
            db.session.add(category)
        db.session.commit()

    def __repr__(self):
        return self.name

def category_query():
    return Category.query