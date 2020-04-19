from . import mail
from flask_mail import Message
from flask import current_app as app
from threading import Thread
def send_mail(subject,sender,recipients,text,html):
    msg=Message(subject,sender=sender,recipients=recipients)
    msg.body=text
    msg.html=html
    th=Thread(target=send_async_email,args=[app._get_current_object(),msg])
    th.start()
    
def send_async_email(the_app,msg):
    with the_app.app_context():
        print('sending email')
        mail.send(msg) 
        print('email sent')