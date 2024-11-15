from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form is fine, HTTP request is POST
    if (register.validate_on_submit()==True): 
            #get username, password and email from the form
            uname = register.user_name.data
            fname = register.first_name.data
            lname = register.last_name.data
            pwd = register.password.data
            email = register.email_id.data
            contact_number = register.contact_num.data
            address = register.address.data
            #check if a user exists
            user = db.session.scalar(db.select(User).where(User.username==uname))
            if user:#this returns true when user is not None
                flash('Username already exists, please try another')
                return redirect(url_for('auth.register'))
            # don't store the password in plaintext!
            pwd_hash = generate_password_hash(pwd)
            #create a new User model object
            new_user = User(username=uname, firstname=fname, lastname=lname, emailid=email, password_hash=pwd_hash, contact=contact_number, address=address)
            db.session.add(new_user)
            db.session.commit()
            
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('user.html', form=register, heading='Register')


# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    try:
        login_form = LoginForm()
        error = None
        if login_form.validate_on_submit():
            user_name = login_form.user_name.data
            password = login_form.password.data
            user = db.session.scalar(db.select(User).where(User.username==user_name))
            if user is None:
                error = 'Incorrect user name'
            elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
                error = 'Incorrect password'
            if error is None:
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash(error)
        return render_template('user.html', form=login_form, heading='Login')
    except Exception as e:
        print(e)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

