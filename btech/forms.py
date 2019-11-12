from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from btech.models import User




class RegisterForm(FlaskForm):
	surname = StringField('Surname', validators=[DataRequired(), Length(min=3, max=20)])
	other_names = StringField('Other_names', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	reg_number = StringField('Reg_number', validators=[DataRequired()])
	course_id = StringField('Course_Id', validators=[DataRequired()])
	level = StringField('Level', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password =	PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is taken')

	def validate_reg_number(self, reg_number):
		user = User.query.filter_by(reg_number=reg_number.data).first()
		if user:
			raise ValidationError('Reg_number is taken')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class ContactUsForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	comments= TextAreaField('Comments', validators=[DataRequired()])
	submit = SubmitField('Send')

class BlogPostForm(FlaskForm):
	title = StringField('Blog Title', validators=[DataRequired()])
	bimage = FileField('Blog Image', validators=[FileAllowed(['jpg','png'])])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')

class BlogEventForm(FlaskForm):
	title = StringField('Blog Title', validators=[DataRequired()])
	bimage = FileField('Blog Image', validators=[FileAllowed(['jpg','png'])])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')

class PostComponentForm(FlaskForm):
	image = FileField('Image', validators=[FileAllowed(['jpg','png'])])
	name = StringField('Name', validators=[DataRequired()])
	value = StringField('Value', validators=[DataRequired()])
	description = TextAreaField('Component description', validators=[DataRequired()])
	submit = SubmitField('Upload to Database')

class AddAdminForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Invite')

class RegisterAdminForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password =	PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username is taken')

	def validate_username(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is taken')



class RequestForm(FlaskForm):
	quantity = StringField('Quantity', validators=[DataRequired()])
	submit = SubmitField('Post Request')

class SearchForm(FlaskForm):
	entry = StringField('Search', validators=[DataRequired()])
	submit = SubmitField('Search')