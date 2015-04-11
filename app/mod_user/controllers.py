# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_user.forms import EditForm

# Import module models (i.e. User)
from app.mod_user.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_user = Blueprint('user', __name__, url_prefix='')

# Set the route and accepted methods
@mod_user.route('/user/', methods=['GET'])
def user_profile():
    # session['user_id'] = 1
    user = User.query.filter_by(id=session['user_id']).first()
    # warning passwords
    return render_template("user_edit.html", user=user)

# Set the route and accepted methods
@mod_user.route('/user/edit', methods=['GET', 'POST'])
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
