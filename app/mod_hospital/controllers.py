# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
#from app.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from app.mod_hospital.models import Hospital

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_hospital = Blueprint('hospital', __name__, url_prefix='/hospital')

# Set the route and accepted methods
@mod_hospital.route('/manage/')
def manage():
    hospital = Hospital.query.filter_by(name="Red Crescent Hospital")

    return render_template("hospital.html")