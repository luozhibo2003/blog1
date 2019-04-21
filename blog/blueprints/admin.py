import os

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, send_from_directory
from flask_ckeditor import upload_fail, upload_success
from flask_login import login_required

from blog.extensions import db
from blog.models import Category, Post, Comment
from blog.forms import PostForm
from blog.utils import allowed_file, redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    print('##########')
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        # same with:
        # category_id = form.category.data
        # post = Post(title=title,body=body,category_id=category_id)
        db.session.add(post)
        db.session.commit()

        flash('Post created.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))

    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post delete', 'success')
    return redirect_back()


@admin_bp.route('/category/new', methods=['GET', 'POST'])
def new_category():
    return render_template('admin/new_category.html')


@admin_bp.route('/link/new', methods=['GET', 'POST'])
def new_link():
    return render_template('admin/new_link.html')


@admin_bp.route('/post/manage')
def manage_post():
    return render_template('admin/manage_post.html')


@admin_bp.route('/category/manage')
def manage_category():
    return render_template('admin/manage_category.html')


@admin_bp.route('/comment/manage')
def manage_comment():
    return render_template('admin/manage_comment.html')


@admin_bp.route('/link/manage')
def manage_link():
    return render_template('admin/manage_link.html')


@admin_bp.route('/settings')
def settings():
    return render_template('admin/settings.html')


@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['BLOG_UPLOAD_PATH'], filename)


@admin_bp.route('/upload', methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('Image only!')
    f.save(os.path.join(current_app.config['BLOG_UPLOAD_PATH'], f.filename))
    url = url_for('.get_image', filename=f.filename)
    return upload_success(url, f.filename)


@admin_bp.route('/post/<int:post_id>/set-comment', methods=['POST'])
def set_comment(post_id):
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect_back()
