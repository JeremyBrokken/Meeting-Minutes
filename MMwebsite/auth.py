#same as views.py but for auth pages
#request to help get the information from the form onto the server
#flash = flask method for message flashing to user on error or success ect...
from hashlib import sha256
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash #hashing for password security
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods =['GET', 'POST']) #by default is get request, this adds post request (HTTP)
def login():
        if request.method == 'POST': #if post request has been made by the website.
        # if email and password match a registered user in the database
            email = request.form.get('email')
            password = request.form.get('password')
        
            user = User.query.filter_by(email=email).first() #User = Location. query.filter_by = looking for data. first() styops at first match
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in succesfully!', category='success')
                    login_user(user, remember=True) #generally remembers the user as logged in for duration
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again', category='error')
            else:
                flash('User does not exist', category='error')
        
        return render_template ("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user() # sets users status to logout
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods =['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #pre-submit error checking
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists, try another.', category='error')
            
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error') #category can be any name, called later

        elif len(first_name) < 2:
            flash('first Name must be greater than 1 characters.', category='error')

        elif password1 != password2:
            flash('Passwords do not match.', category='error')

        elif len(password1) < 7:
            flash('Password must be at least characters.', category='error')
            
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256')) #storing password with a hash. sha= hashing algorithm
            db.session.add(new_user) # adds new_user to the database
            db.session.commit() #update changes made to database
            #After new user is created, login as new user
            login_user(new_user, remember=True) #generally remembers the user as logged in for duration
            flash('Account created!', category='success')
            return redirect(url_for('views.home')) #could use redirect('/'), BUT if I ever change the url for home function, would have to change this
            #return = redirects to the homepage

    return render_template ("sign_up.html", user=current_user)

