import secrets
import os
from flask import render_template, url_for, flash, redirect, request
from btech import app, db, bcrypt, admin
from btech.models import User, Post, Component, Category, Notification, Request, Permissions
from btech.forms import RegisterForm, LoginForm, ContactUsForm, BlogPostForm, AddAdminForm, RegisterAdminForm, RequestForm, PostComponentForm, SearchForm, BlogEventForm
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/homepage")
def homepage():
	posts = Post.query.all()
	return render_template('home.html',posts=posts)


@app.route("/store", methods=['GET','POST'])
def store():
	category = Category.query.all()
	component = Component.query.all()
	form = SearchForm()
	if form.validate_on_submit():
		component = Component.query.filter_by(name = form.entry.data).first()
	return render_template('store.html', title= 'Store', category=category, component=component)
	

@app.route("/contact_us", methods=['GET','POST'])
def contact_us():
	form = ContactUsForm()
	if form.validate_on_submit():
		notification = Notification(name=form.name.data, email=form.email.data, comments=form.comments.data)
		db.session.add(notification)
		db.session.commit()
		flash(f'Thank you for your feedback', 'success')
		return redirect(url_for('homepage'))
	return render_template('contact_us.html', title='Contact Us', form=form)


@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(surname=form.surname.data,other_names=form.other_names.data,email=form.email.data,reg_number=form.reg_number.data,course_id=form.course_id.data,level=form.level.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Registered succesfully', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Sign Up', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else  redirect(url_for('homepage'))
		else:
			flash('login was unsuccessful. Please check your Email and Password','danger')
	return render_template('login.html', title='Sign In', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('homepage'))

@app.route("/admin1")
def admin1():
	return render_template('admin/admin1.html', title='Admin_Panel')
	

def save_picture(form_bimage):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_bimage.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/blog_image', picture_fn)
	form_bimage.save(picture_path)
	return picture_fn


@app.route("/blog_post", methods=['GET','POST'])
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


@app.route("/event", methods=['GET','POST'])
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


@app.route("/bpost")
def bpost():
	posts = Post.query.all()
	return render_template('posts.html', picture_file=post.bimage, title=post.title, posts=posts)

def save_image(form_image):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_image.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/comp_image', picture_fn)
	form_image.save(picture_path)
	return picture_fn


@app.route("/component", methods=['GET','POST'])
def component():
	category = Category.query.all()
	form = PostComponentForm()
	if form.validate_on_submit():
		image_file = save_image(form.image.data)
		component = Component(name=form.name.data, value=form.value.data, description=form.description.data, image = image_file)
		db.session.add(component)
		db.session.commit()
		flash(f'Uplaod succesfully', 'success')
		return redirect(url_for('home'))
	return render_template('admin/component.html', title='Create Component', form=form, category = category)



@app.route("/admin")
def admin():
	return render_template('admin/database.html', title='Database')

@app.route("/add_admin", methods=['GET','POST'])
def add_admin():
	form = AddAdminForm()
	return render_template('admin/add_admin.html', title='Invite Admin', form=form)

@app.route("/admin_register", methods=['GET','POST'])
def admin_register():
	form = RegisterAdminForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_admin=True)
		db.session.add(user)
		db.session.commit()
		flash(f'Registered succesfully', 'success')
		return redirect(url_for('login'))
	return render_template('admin/admin_register.html', title = 'Register as Admin', form=form)

	
@app.route("/requests")
def requests():
	items = Request.query.all()
	return render_template('admin/request.html', title='Request Posted', items=items)

@app.route("/comments")
def comments():
	notes = Notification.query.all()
	return render_template('admin/comments.html', title='Comments', notes=notes)

