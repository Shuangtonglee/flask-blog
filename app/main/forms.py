from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from ..models import category_query




class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired(message='请输入标题')])
    body = PageDownField(validators=[DataRequired(message='请输入文章')])
    picture = StringField(validators=[DataRequired(message='请输入图片链接')])
    submit = SubmitField('发布')

class CommentForm(FlaskForm):
    body = TextAreaField(validators=[DataRequired(message='请输入评论')])
    submit = SubmitField('发布')


class CategoryForm(FlaskForm):
    categorys = QuerySelectField(query_factory=category_query,allow_blank=False)
