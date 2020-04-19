from flask import render_template, url_for, flash, redirect, request, Blueprint
from btech import db, bcrypt
# from btech import bootstrap
from btech.models import User
from .password_reset import send_reset_email
from time import ctime
import secrets,os
from btech.users import users
from PIL import Image
from btech.users.forms import RegisterForm, LoginForm,ConfirmEmailForm,PasswordResetForm,AccountForm
from flask_login import login_user, current_user, logout_user, login_required


static_folder=users.root_path.split('/')
static_folder="/".join(static_folder[:-1])+'/static'
def save_pic(static_folder,file,folder):
    pic_hex=secrets.token_hex(8)
    _,pic_ext=os.path.splitext(file.filename)
    pic_name=pic_hex+pic_ext
    size=(400,400)
    img=Image.open(file)
    img.thumbnail(size)
    pic_path=os.path.join(static_folder,folder,pic_name)
    if not os.path.exists(os.path.join(static_folder,folder)):
    	print('directory does not exist,creating one...')
    	os.mkdir(os.path.join(static_folder,folder))
    	
    img.save(pic_path)
    print('image saved')
    return pic_name

def delete_current_pic(static_folder,current_img,folder):
    pic_path=os.path.join(static_folder,folder,current_img)
    print('pic path:'+pic_path)
    if os.path.exists(pic_path):
        try:
            os.remove(pic_path)
        except:
            print('failed to delete')
    else:
        print('picture not found ')
    

@users.route('/Account/<name>',methods=['GET','POST'])
@login_required
def account(name):
    folder='profile_pics'
    user=current_user
    if not user:
        return redirect(url_for('users.login'))
    form=AccountForm()
    if form.validate_on_submit():
        if form.img.data:
            current_img=current_user.profile_pic
            delete_current_pic(static_folder,current_img,folder)
            file=form.img.data
            picture_name=save_pic(static_folder,file,folder)
            current_user.profile_pic=picture_name
        current_user.surname=form.surname.data
        current_user.email=form.email.data
        db.session.commit()
        flash('account updated successfully','success')
        return redirect(url_for('users.account',name=current_user.surname))
    profile_pic=url_for('static',filename='/profile_pics/'+current_user.profile_pic)
    form.surname.data=user.surname
    form.email.data=user.email
    return render_template('user/account.htm',form=form,profile_pic=profile_pic)

@users.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('register'))
	form = RegisterForm()
	if form.validate_on_submit():
		password=form.password.data
		user = User(surname=form.surname.data,email=form.email.data,reg_number=form.reg_number.data)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()
		flash(f'Registered succesfully', 'success')
		return redirect(url_for('users.login'))
	return render_template('forms/register.htm', title='Sign Up', form=form)

@users.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.homepage'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and user.verify_password(form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else  redirect(url_for('main.homepage'))
		else:
			flash('login was unsuccessful. Please check your Email and Password','danger')
	return render_template('forms/login.htm', title='Sign In', form=form)

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.homepage'))
@users.route('/activate')
def activate():
    render_template('user/activate.htm')
    
    
@users.route('/reset_email',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form=ConfirmEmailForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        return redirect(url_for('.activation',name=user.email))
    return render_template('forms/email_reset.htm',form=form)


@users.route('/new_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.hompage'))
    print('user is already logged in')
    user=User.verify_reset_token(token)
    print('this is what returned:',user)
    if not user:
        return redirect(url_for('main.homepage'))
    form=PasswordResetForm()
    if form.validate_on_submit():
        pswd=form.password.data
        user.set_password(pswd)
        db.session.commit()
        flash('Password updated succesfully','success')
        return redirect(url_for('users.login'))
    return render_template('forms/new_pswd.htm',form=form,user=user)

@users.route('/activate/<name>')
def activation(name):
    return render_template('user/activate.htm',email=name) 