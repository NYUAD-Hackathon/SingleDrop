from geopy.geocoders import Nominatim

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_user.forms import RegistrationForm
from app.mod_user.forms import LoginForm
from app.mod_user.forms import EditForm

# Import module models (i.e. User)
from app.mod_user.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_user = Blueprint('user', __name__, url_prefix='/user')

# Set the route and accepted methods
@mod_user.route('/login/', methods=['GET', 'POST'])
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

@mod_user.route('/logout/', methods=['GET', 'POST'])
def logout():

    session.pop('logged_in', None)
    flash('You were logged out')

    return redirect(url_for('index'))

@mod_user.route('/registration/', methods=['GET', 'POST'])
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

@mod_user.route('/profile/', methods=['GET'])
def user_profile():
    # session['user_id'] = 1
    user = User.query.filter_by(id=session['user_id']).first()
    # warning passwords
    return render_template("user_edit.html", user=user)

@mod_user.route('/edit/', methods=['GET', 'POST'])
def user_edit():
    form = EditForm(request.form)
    user = User.query.filter_by(id=session['user_id']).first()

    # Verify the sign in form
    if form.validate_on_submit():

        user.phone = form.phone.data
        user.city = form.city.data
        user.neighborhood = form.neighborhood.data

        db.session.add(user)
        db.session.commit()

    return render_template("user_edit.html", user=user, form=form)
