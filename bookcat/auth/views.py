from flask import render_template, request, flash, redirect,url_for

from bookcat.auth.forms import RegistrationForm, LoginForm
from bookcat.auth import authentication
from bookcat.auth.models import User
from flask_login import login_user, logout_user, login_required, current_user
from bookcat.api_home import home

@authentication.route('/register/', methods=['Get', 'POST'])
def register_user():
    name = None
    email = None

    form = RegistrationForm()

   # if request.method == 'POST':
   #     name = form.name.data
   #    email = form.emai.data#

    if current_user.is_authenticated:
        flash('You are already registered')
        return redirect(url_for('api_home.display_books'))

    if form.validate_on_submit():  #Checks if POST Request and also validates data
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data)

        flash("Registration Successful")
        return redirect(url_for('authentication.do_the_login'))

    return render_template('registration_old.html', form=form)

@authentication.route('/login', methods=['Get', 'POST'])
def do_the_login():

    form = LoginForm()

    if current_user.is_authenticated:
        flash('You are already logged-in')
        return redirect(url_for('api_home.display_books'))

    if form.validate_on_submit():
            user = User.query.filter_by(user_email=form.email.data).first()
            if not user or not user.check_password(form.password.data):
                flash('Invalid Credentials, Please try Again')
                return redirect(url_for('authentication.do_the_login'))

            login_user(user,form.stay_logged_in.data)
            return redirect(url_for('api_home.display_books'))

    return render_template('login.html', form=form)


@authentication.route('/logout', methods=['Get'])
@login_required
def log_out_user():
    logout_user()
    return redirect(url_for('api_home.display_books'))

@authentication.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
