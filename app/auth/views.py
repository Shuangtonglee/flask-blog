from flask import Blueprint
from flask import render_template,flash,redirect,url_for,request
from flask_login import login_required,login_user,logout_user,current_user
from .forms import *
from ..models import db
from ..send_email import send_email

auth = Blueprint('auth', __name__)

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint != 'static'\
        and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,'账户确认','mail/confirm',token=token,user=user)
        flash('确认邮件已发送')
        return redirect(url_for('.login'))
    return render_template('auth/register.html',form=form)


@auth.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            flash('已登录')
            return redirect((request.args.get('next') or url_for('main.index')))
        flash('账号或密码不对')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出')
    return redirect(url_for('main.index'))



@auth.route('/change_password',methods=['POST','GET'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
            if current_user.verify_password(form.old_password.data):  #登录之后current_user=User.query.filter_by(username=current_user.username).first()
                current_user.password = form.password.data
                db.session.add(current_user)
                flash('修改成功')
                return redirect(url_for('main.index'))
            else:
                flash('旧密码不正确！')
    return render_template('auth/change_password.html',form=form)


@auth.route('/reset',methods=['POST','GET'])
def password_request_reset():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordEmail()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(form.email.data,'重设密码','mail/reset_password',user=user,token=token)
            flash('邮件已发送')
            return redirect(url_for('.login'))
    return render_template('auth/reset_password_email.html',form=form)

@auth.route('/reset_password/<token>',methods=['POST','GET'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('.index'))
        elif user.reset_password(token,form.password.data):
            flash('密码重设成功')
            return redirect(url_for('.login'))
        else:
            flash('链接无效或过期')
    return render_template('auth/reset_password.html',form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('账户已成功确认！')
    else:
        flash('链接无效或过期')
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
        if current_user.confirmed:
                flash('账户已经确认！')
                return redirect(url_for('main.index'))
        token = current_user.generate_confirmation_token()
        send_email(current_user.email,'账户确认','mail/confirm',token=token,user=current_user)
        flash('确认邮件已发送')
        return redirect(url_for('main.index'))



@auth.app_errorhandler(404)
def page_not_found(e):
    return render_template('auth/404.html'),404

@auth.app_errorhandler(500)
def page_not_found(e):
    return render_template('auth/500.html'),500
