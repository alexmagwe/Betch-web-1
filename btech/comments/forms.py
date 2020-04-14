from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from btech.models import Notification




class ContactUsForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	comments= TextAreaField('Comments', validators=[DataRequired()])
	submit = SubmitField('Send')

