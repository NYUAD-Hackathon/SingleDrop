from geopy.geocoders import Nominatim

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
    print form
    print form.errors
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        print "PASSWORD:", form.password.data
        print "USER PASS:", user.password
        if user and user.password == form.password.data:

            session['user_id'] = user.id

            flash('Welcome %s' % user.name)
            print user
            return redirect("user")

        flash('Wrong email or password', 'error-message')
    print "wrong form"
    return render_template("auth/login.html", form=form)

@mod_auth.route('/logout/', methods=['GET', 'POST'])
def logout():

    session.pop('logged_in', None)
    flash('You were logged out')

    return redirect(url_for('index'))

# Set the route and accepted methods
@mod_auth.route('/registration/', methods=['GET', 'POST'])
def registration():
    geolocator = Nominatim()

    form = RegistrationForm(request.form)

    # Verify the sign in form
    print form
    print form.errors
    if form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        password = form.password.data
        phone = form.phone.data
        blood_type = form.blood_type.data
        city = form.city.data
        neighborhood = form.neighborhood.data

        address = neighborhood + ", " + city
        location = geolocator.geocode(address)

        lat = location.latitude
        lon = location.longitude

        user = User(name, email, password, phone, blood_type, city, neighborhood, lat, lon)

        db.session.add(user)
        db.session.commit()
        print "user created"
        print user

        return redirect("login")
    print form.errors
    print "wrong form"
    return render_template("registration.html", form=form)
