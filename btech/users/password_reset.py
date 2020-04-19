
# from flask import current_app as app
from flask import render_template,current_app as app

from ..email import send_mail 

def send_reset_email(user):
    token=user.set_reset_token()
    send_mail(subject='Reset Password',sender='noreply@gmail.com',recipients=[user.email],text='Follow the link below to reset your email',html=render_template('forms/reset.htm',user=user,token=token))