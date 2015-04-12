# Import flask dependencies
from flask import Blueprint, request, render_template, \
				  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_hospital.forms import LoginForm, SearchForm, RegistrationForm

# Import module models (i.e. User)
from app.mod_hospital.models import Hospital
from app.mod_user.models import User

import math

# Geo-code module
from geopy.geocoders import Nominatim

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_hospital = Blueprint('hospital', __name__, url_prefix='/hospital')

# how many people contact
n = 10

# Set the route and accepted methods
@mod_hospital.route('/manage/', methods=['GET', 'POST'])
def manage():
	if (session.get('hospital_id')):
		form = SearchForm(request.form)
		blood = None
		if form.validate_on_submit():
			blood = form.blood.data
		print form.errors
		hosp = Hospital.query.filter_by(id=session['hospital_id']).first()
		if blood:
			users = User.query.filter_by(blood_type=blood).all()
		else:
			users = User.query.all()
		for u in users:
			u.distance = distance(hosp.lat, hosp.lon, u.lat, u.lon)

		users = sorted(users, key=lambda x: x.distance)[:n]

		return render_template("hospital/manage.html", users=users, blood_type=blood)
	return render_template('403.html')

@mod_hospital.route('/login/', methods=['GET', 'POST'])
def login():

	# If login form is submitted
	form = LoginForm(request.form)

	# Verify the sign in form
	print form
	print form.errors
	if form.validate_on_submit():

		hospital = Hospital.query.filter_by(name=form.name.data).first()
		
		if hospital and hospital.password == form.password.data:

			session['logged_in'] = True
			session['hospital_id'] = hospital.id

			flash('Welcome %s' % hospital.name)
			print hospital
			return redirect("/hospital/manage/")

	flash('Wrong name or password', 'error-message')
	print "wrong form"
	return render_template("hospital/login.html", form=form)

@mod_hospital.route('/logout/', methods=['GET', 'POST'])
def logout():

	session.pop('logged_in', None)
	session.pop('hospital_id', None)
	flash('You were logged out')

	return redirect("/")

# Set the route and accepted methods
@mod_hospital.route('/registration/', methods=['GET', 'POST'])
def registration():
	geolocator = Nominatim()

	form = RegistrationForm(request.form)

	# Verify the sign in form
	print "FORM:", form
	print form.errors
	if form.validate_on_submit():

		name = form.name.data
		password = form.password.data
		city = form.city.data
		neighborhood = form.neighborhood.data

		address = neighborhood + ", " + city
		location = geolocator.geocode(address)
		try:
			lat = location.latitude
			lon = location.longitude
		except:
			lat = 0
			lon = 0
			print "ERROR no location"

		hospital = Hospital(name, password, city, neighborhood, lat, lon)

		db.session.add(hospital)
		db.session.commit()
		print "hospital created"
		print hospital

		return redirect("hospital/login")
	print form.errors
	print "wrong form"
	return render_template("hospital/registration.html", form=form)

def distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    return 6367 * c
