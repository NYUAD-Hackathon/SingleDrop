# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import RegistrationForm
from app.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from app.mod_user.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='')

# Set the route and accepted methods
@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():

    # If login form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):

            session['user_id'] = user.id

            flash('Welcome %s' % user.name)

            return redirect(url_for('user.profile'))

        flash('Wrong email or password', 'error-message')

    return render_template("auth/login.html", form=form)

@mod_auth.route('/logout/', methods=['GET', 'POST'])
def logout():

    session.pop('logged_in', None)
    flash('You were logged out')

    return redirect(url_for('index'))

# Set the route and accepted methods
@mod_auth.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        phone = form.phone.data
        blood_type = form.blood_type.data
        city = form.city.data
        neighborhood = form.neighborhood.data

        user = User(name, email, password, phone, blood_type, city, neighborhood)

        db.session.add(user)
        db.session.commit()
        return render_template("registration.html", user=user, form=form)
    return render_template("registration.html", form=form)
