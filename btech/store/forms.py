from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from btech.models import Component, Category, Request




class PostComponentForm(FlaskForm):
	image = FileField('Image', validators=[FileAllowed(['jpg','png'])])
	name = StringField('Name', validators=[DataRequired()])
	value = StringField('Value', validators=[DataRequired()])
	description = TextAreaField('Component description', validators=[DataRequired()])
	submit = SubmitField('Upload to Database')


class RequestForm(FlaskForm):
	quantity = StringField('Quantity', validators=[DataRequired()])
	submit = SubmitField('Post Request')

class SearchForm(FlaskForm):
	entry = StringField('Search', validators=[DataRequired()])
	submit = SubmitField('Search')