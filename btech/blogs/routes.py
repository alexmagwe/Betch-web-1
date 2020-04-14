import secrets
import os
from flask import render_template, url_for, flash, redirect, request, Blueprint
from btech import db, bcrypt
from btech.models import Post
from btech.blogs.forms import BlogPostForm, BlogEventForm
from flask_login import login_user, current_user, logout_user, login_required


blogs= Blueprint('blogs',__name__)


def save_picture(form_bimage):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_bimage.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/blog_image', picture_fn)
	form_bimage.save(picture_path)
	return picture_fn


@blogs.route("/blog_post", methods=['GET','POST'])
def blog_post():
	form = BlogPostForm()
	if form.validate_on_submit():
		picture_file = save_picture(form.bimage.data)
		blog = Post(title=form.title.data, content=form.content.data, bimage=picture_file, author = current_user)
		db.session.add(blog)
		db.session.commit()
		flash(f'Blog post succesfully,{form.title.data}', 'success')
		return redirect(url_for('homepage'))
	return render_template('admin/blog_post.html', title='Post Blog', form=form)


@blogs.route("/event", methods=['GET','POST'])
def event():
	form = BlogEventForm()
	if form.validate_on_submit():
		if form.bimage.data:
			picture_file = save_picture(form.bimage.data)
		blog = Post(title=form.title.data, content=form.content.data, author = current_user, is_event=True, bimage=picture_file)
		db.session.add(blog)
		db.session.commit()
		flash(f'Blog post succesfully,{form.title.data}', 'success')
		return redirect(url_for('homepage'))
	return render_template('admin/event.html', title='Event Blog', form=form)


