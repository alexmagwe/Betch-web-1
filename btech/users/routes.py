from flask import render_template, url_for, flash, redirect, request, Blueprint
from btech import db, bcrypt
from btech.models import User
from btech.users.forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('register'))
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(surname=form.surname.data,email=form.email.data,reg_number=form.reg_number.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Registered succesfully', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Sign Up', form=form)

@users.route("/login", methods=['GET','POST'])
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

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('homepage'))

