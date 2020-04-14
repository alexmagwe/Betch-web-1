from flask import render_template, url_for, flash, redirect, request, Blueprint
from btech import db
from btech.models import Post

main = Blueprint('main',__name__)


@main.route("/")
@main.route("/homepage")
def homepage():
	posts = Post.query.all()
	return render_template('home.html',posts=posts)


