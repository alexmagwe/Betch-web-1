from flask import render_template, url_for, flash, redirect, request, Blueprint
from btech import db
from btech.models import Notification 
from btech.comments.forms import ContactUsForm


comments = Blueprint('comments',__name__)


@comments.route("/contact_us", methods=['GET','POST'])
def contact_us():
	form = ContactUsForm()
	if form.validate_on_submit():
		notification = Notification(name=form.name.data, email=form.email.data, comments=form.comments.data)
		db.session.add(notification)
		db.session.commit()
		flash(f'Thank you for your feedback', 'success')
		return redirect(url_for('main.homepage'))
	return render_template('contact_us.html', title='Contact Us', form=form)


