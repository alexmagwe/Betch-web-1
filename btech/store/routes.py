import secrets
import os
from flask import render_template, url_for, flash, redirect, request, Blueprint
from btech import db, bcrypt
from btech.models import User, Post, Component, Category, Notification, Request, Permissions
from btech.store.forms import RequestForm, PostComponentForm, SearchForm
from flask_login import login_user, current_user, logout_user, login_required


store = Blueprint('store',__name__)


@store.route("/store", methods=['GET','POST'])
def store():
	categorys = Category.query.order_by(Category.id.desc()).all()
	components = Component.query.order_by(Component.id.desc()).all()
	form = SearchForm()
	if form.validate_on_submit():
		component = Component.query.filter_by(name = form.entry.data).first()
	return render_template('store.html', title= 'Store', components =components)
	


def save_image(form_image):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_image.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/comp_image', picture_fn)
	form_image.save(picture_path)
	return picture_fn


@store.route("/component", methods=['GET','POST'])
def component():
	categorys = Category.query.order_by(Category.id.desc()).all()
	form = PostComponentForm()
	if form.validate_on_submit():
		image_file = save_image(form.image.data)
		component = Component(name=form.name.data, value=form.value.data, description=form.description.data, image = image_file)
		db.session.add(component)
		db.session.commit()
		flash(f'Uplaod succesfully', 'success')
		return redirect(url_for('home'))
	return render_template('admin/component.html', title='Create Component', form=form, categorys = categorys)





@app.route("/requests")
def requests():
	items = Request.query.all()
	return render_template('admin/request.html', title='Request Posted', items=items)

