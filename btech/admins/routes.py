
import secrets
from flask import render_template, url_for, flash, redirect, request, Blueprint
from btech import db, bcrypt, admin
from btech.models import User, Permissions
from btech.admins.forms import LoginForm, AddAdminForm, RegisterAdminForm
from flask_login import login_user, current_user, logout_user, login_required

admins = Blueprint('admins',__name__)


@admins.route("/admin1")
def admin1():
	return render_template('admin/admin1.html', title='Admin_Panel')
	

@admins.route("/admin")
def admin():
	return render_template('admin/database.html', title='Database')

@admins.route("/add_admin", methods=['GET','POST'])
def add_admin():
	form = AddAdminForm()
	return render_template('admin/add_admin.html', title='Invite Admin', form=form)

@admins.route("/admin_register", methods=['GET','POST'])
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


