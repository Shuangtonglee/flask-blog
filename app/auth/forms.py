from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,length,regexp,ValidationError


from ..models import User


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(message='请输入邮箱地址'),length(1,32,message='邮箱地址请不要超过32个字符'),Email(message='无效的邮箱地址')])
    password = PasswordField(validators=[DataRequired(message='请输入密码'),length(6,16,message='密码长度介于6到16个字符')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(message='请输入邮箱地址'),length(1,32,message='邮箱地址请不要超过32个字符'),Email(message='无效的邮箱地址')])
    username = StringField(validators=[DataRequired(message='请输入用户名'),length(1,64,message='用户名长度介于4到64个字符'),
                                       regexp('^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$',0,'用户名只能包含汉字，数字，字母和下划线，且不能以下划线开头和结尾')])
    password = PasswordField(validators=[DataRequired(message='请输入密码'),length(6,16,message='密码长度介于6到16个字符')])
    password1 = PasswordField(validators=[DataRequired(message='请输入密码'),EqualTo('password',message='密码前后不一致')])
    submit = SubmitField('注册')


    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(message='请输入密码'),length(6,16,message='密码长度介于6到16个字符')])
    password1 = PasswordField(validators=[DataRequired(message='请输入密码'),EqualTo('password',message='密码前后不一致')])
    submit = SubmitField('更新密码')

class ResetPasswordEmail(FlaskForm):
    email = StringField(validators=[DataRequired(message='请输入邮箱地址'),length(1,32,message='邮箱地址请不要超过32个字符'),Email(message='无效的邮箱地址')])
    submit = SubmitField('重设密码')

    # def validate_email(self,field):
    #     if not User.query.filter_by(email=field.data).first():
    #         raise ValidationError('邮箱不存在 ')


class ResetPasswordForm(FlaskForm):
    email = StringField(validators=[DataRequired(message='请输入邮箱地址'),length(1,32,message='邮箱地址请不要超过32个字符'),Email(message='无效的邮箱地址')])
    password = PasswordField(validators=[DataRequired(message='请输入密码'),length(6,16,message='密码长度介于6到16个字符')])
    password1 = PasswordField(validators=[DataRequired(message='请输入密码'),EqualTo('password',message='密码前后不一致')])
    submit = SubmitField('重设密码')

    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱不存在 ')

