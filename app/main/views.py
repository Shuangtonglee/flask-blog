from flask import Blueprint
from flask import render_template,flash,redirect,url_for,request,current_app
from flask_login import login_required,current_user
from .forms import *
from app.models import Post,Comment,db,Category,Role

main = Blueprint('main', __name__)


@main.route('/')
def index():
    comments =Comment.query.order_by(Comment.timestamp.desc())
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html',posts=posts,comments=comments)

@main.route('/write',methods=['POST','GET'])
@login_required
def write():
    if current_user.role != Role.query.filter_by(name='Admin').first():
        return '只有管理员有此权限'
    form = PostForm()
    form1 = CategoryForm()
    endpoint=request.endpoint[-6:]
    if form.validate_on_submit() and form1.validate_on_submit():
        post = Post(title=form.title.data,body=form.body.data,picture=form.picture.data,
                    category_id=form1.categorys.data.id,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit() #使redirect 时能够获得post.id
        flash('发布成功！')
        return redirect(url_for('.articles',id=post.id))
    return render_template('write.html',form=form,endpoint=endpoint,form1=form1)

@main.route('/edit/<int:id>',methods=['POST','GET'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    form1 = CategoryForm()
    endpoint=request.endpoint[-6:]
    if endpoint != '.write':
        endpoint = '.edit'
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category_id = form1.categorys.data.id
        post.picture = form.picture.data
        db.session.add(post)
        flash('修改成功！')
        return redirect(url_for('.articles',id=id))
    form.title.data = post.title
    form.body.data = post.body
    form1.categorys.data = post.category
    form.picture.data = post.picture
    return render_template('write.html',form=form,endpoint=endpoint,form1=form1)

@main.route('/articles/<int:id>',methods=['POST','GET'])
def articles(id):
    post = Post.query.get_or_404(id)
    post.viewed()
    endpoint=request.endpoint[-9:]
    next = '/articles/' + str(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,post=post,author=current_user._get_current_object())
        db.session.add(comment)
        flash('评论成功！')
        return redirect(url_for('.articles',id=id))
    comments = post.comments.order_by(Comment.timestamp.desc()).all()
    return render_template('article.html',post=post,form=form,endpoint=endpoint,next=next,comments=comments)

@main.route('/all')
def all():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False
    )
    posts = pagination.items
    return render_template('articles.html',posts=posts,pagination=pagination)

@main.route('/category/<category>')
def category(category):
    category = Category.query.filter_by(name=category).first()  #是否还有简单的查询方法，直接通过变量和Post查询
    page = request.args.get('page',1,type=int)
    pagination = Post.query.filter_by(category_id=category.id).order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False
    )
    posts = pagination.items
    return render_template('articles.html',posts=posts,pagination=pagination,category=category)







