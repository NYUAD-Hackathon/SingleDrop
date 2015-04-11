# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')


# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_hospital.controllers import mod_hospital as hospital_module
from app.mod_user.controllers import mod_user as user_module
from app.mod_index.controllers import mod_index as index_module

# Register blueprint(s)
app.register_blueprint(hospital_module)
app.register_blueprint(user_module)
app.register_blueprint(index_module)

# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
#db.drop_all()
db.create_all()
