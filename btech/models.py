from datetime import datetime
from btech import db, login_manager, admin
from flask_login import UserMixin, LoginManager, current_user
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	surname = db.Column(db.String(20), nullable=True)
	username = db.Column(db.String(20), nullable=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	reg_number = db.Column(db.String(60), unique=True)
	password = db.Column(db.String(60), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	requests = db.relationship('Request', backref='name', lazy=True)
	posts = db.relationship('Post', backref='author', lazy=True)
	

	def __repr__(self):
		return f"User('{self.surname}',{self.email}','{self.reg_number}',{self.username})"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	title = db.Column(db.String(20), nullable=False)
	bimage  = db.Column(db.String(120), nullable=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	is_event = db.Column(db.Boolean, default=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	
	def __repr__(self):
		return f"Post('{self.title}','{self.bimage}','{self.date_posted}')"

class Component(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	image  = db.Column(db.String(120), nullable=False)
	name = db.Column(db.String(20), nullable=False)
	value = db.Column(db.String(20), nullable=False)
	description = db.Column(db.Text, nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	requests = db.relationship('Request', backref='item', lazy=True)

	def __repr__(self):
		return f"Component('{self.image}','{self.name}','{self.description}')"

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(20), nullable=False)
	description = db.Column(db.Text, nullable=False)
	components = db.relationship('Component', backref='item_class', lazy=True)

	def __repr__(self):
		return f"Category('{self.name}','{self.description}')"

class Notification(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement = True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), nullable=False)
	comments = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f"Notification('{self.name}','{self.name}')"

class Request(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement = True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	quantity = db.Column(db.Integer, nullable=False, default= 1)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	component_id = db.Column(db.Integer, db.ForeignKey('component.id'), nullable=False)

	def __repr__(self):
		return f"Request('{self.quantity}')"


class Permissions(ModelView):

	def is_accessible(self):
		if current_user.is_admin == True:
			return current_user.is_authenticated
		else:
			return "abort"
	def not_auth(self):
		return " "


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Component, db.session))
admin.add_view(ModelView(Notification, db.session))
admin.add_view(ModelView(Request, db.session))

	




