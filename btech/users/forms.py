from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from btech.models import User




class RegisterForm(FlaskForm):
	surname = StringField('Surname', validators=[DataRequired(), Length(min=3, max=20)])
	reg_number = StringField('Reg_number', validators=[DataRequired()])
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


