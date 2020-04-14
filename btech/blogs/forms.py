from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from btech.models import Post



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

