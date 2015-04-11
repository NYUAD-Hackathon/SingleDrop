# Import flask dependencies
from flask import Blueprint, request, render_template, \
				  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_hospital.forms import LoginForm

from app.mod_hospital.forms import RegistrationForm

# Import module models (i.e. User)
from app.mod_hospital.models import Hospital

# Geo-code module
from geopy.geocoders import Nominatim

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_hospital = Blueprint('hospital', __name__, url_prefix='/hospital')

# Set the route and accepted methods
@mod_hospital.route('/manage/')
def manage():
	hospital = Hospital.query.filter_by(name="Red Crescent Hospital")
	return render_template("hospital.html")

@mod_hospital.route('/login/', methods=['GET', 'POST'])
def login():

	# If login form is submitted
	form = LoginForm(request.form)

	# Verify the sign in form
	print form
	print form.errors
	if form.validate_on_submit():

		hospital = Hospital.query.filter_by(name=form.name.data).first()
		print "PASSWORD:", form.password.data
		print "USER PASS:", hospital.password
		if hospital and hospital.password == form.password.data:

			session['hospital_id'] = hospital.id

			flash('Welcome %s' % hospital.name)
			print hospital
			return redirect("hospital/manage")

	flash('Wrong name or password', 'error-message')
	print "wrong form"
	return render_template("hospital/login.html", form=form)

@mod_hospital.route('/logout/', methods=['GET', 'POST'])
def logout():

	session.pop('logged_in', None)
	flash('You were logged out')

	return redirect(url_for('index'))

# Set the route and accepted methods
@mod_hospital.route('/registration/', methods=['GET', 'POST'])
def registration():
	geolocator = Nominatim()

	form = RegistrationForm(request.form)

	# Verify the sign in form
	print form
	print form.errors
	if form.validate_on_submit():

		name = form.name.data
		password = form.password.data
		city = form.city.data
		neighborhood = form.neighborhood.data

		address = neighborhood + ", " + city
		location = geolocator.geocode(address)

		lat = location.latitude
		lon = location.longitude

		hospital = Hospital(name, password, city, neighborhood, lat, lon)

		db.session.add(hospital)
		db.session.commit()
		print "hospital created"
		print hospital

		return redirect("hospital/manage")
	print form.errors
	print "wrong form"
	return render_template("hospital/registration.html", form=form)
