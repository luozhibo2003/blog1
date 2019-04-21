from flask import Blueprint, render_template, current_app, request, url_for, flash, redirect
from flask_login import current_user

from blog.extensions import db
from blog.emails import send_new_reply_email
from blog.forms import AdminCommentForm, CommentForm
from blog.models import Post, Comment, Category

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)  # 从查询字符串获取当前页数
    per_page = current_app.config['BLOG_POST_PER_PAGE']  # 单页数量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items  # 当前页数的记录列表
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    print('@@@@@@@@@@@@@@@@@')
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page
    )
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body, from_admin=from_admin, post=post, reviewed=reviewed
        )
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('Comment published.', 'success')
        else:
            flash('Thanks,your comment will be published after reviewed.', 'info')
            send_new_reply_email(post)
        return redirect(url_for('.show_post', post_id=post_id))

    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page,per_page)
    return render_template('blog/category.html')


@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    return "change_theme"


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    return "dkdkd"
