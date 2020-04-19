from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from btech.models import User
from flask_wtf.file import FileField,FileAllowed


class RegisterForm(FlaskForm):
	surname = StringField('Surname', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	reg_number = StringField('Reg_number', validators=[DataRequired()])
	img=FileField('Add profile picture',validators=[FileAllowed(['jpg','png','jpeg'])])
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

class ConfirmEmailForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('confirm')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('That account does not exist')
        
class PasswordResetForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('reset')

class AccountForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    img=FileField('Change profile picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField('Update')