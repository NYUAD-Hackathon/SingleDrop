# Import flask dependencies
from flask import Blueprint, request, render_template, \
				  flash, g, session, redirect, url_for, make_response

# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Twilio number = +17313345839

# Find these values at https://twilio.com/user/account


# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_index = Blueprint('index', __name__, url_prefix='')

# Set the route and accepted methods
@mod_index.route('/')
def index():
	return render_template("index/index.html")

@mod_index.route('/api/message/<phone>', methods=['GET'])
def message(phone):
	account_sid = "ACa6519741271e9a4dc8536f2feb388c0f"
	auth_token = "694e428d2de4bb3526eeed5f645a1661"
	client = TwilioRestClient(account_sid, auth_token)

	message = client.messages.create(to=phone, from_="+17313345839", body="Hello there!")

	print message

	return ""

@mod_index.route('/api/call/<phone>', methods=['GET'])
def call(phone):
	account_sid = "ACa6519741271e9a4dc8536f2feb388c0f"
	auth_token = "694e428d2de4bb3526eeed5f645a1661"
	client = TwilioRestClient(account_sid, auth_token)
	
	# Make the call
	call = client.calls.create(to=phone,  # Any phone number
			               from_="+17313345839", # Must be a valid Twilio number
			               url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")

	return ""

@mod_index.route('/about')
def about():
	return render_template("index/about.html")

@mod_index.route('/contacts')
def contacts():
	return render_template("index/contacts.html")