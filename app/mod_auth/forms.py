# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class RegistrationForm(Form):
    name = TextField('Name', [
                Required(message='name')])
    email    = TextField('Email Address', [Email(),
                Required(message='email')])
    password = PasswordField('Password', [
                Required(message='password')])
    phone = TextField('Phone', [
                Required(message='phone')])
    blood_type = TextField('Blood Type', [
                Required(message='blood type')])
    city = TextField('City', [
                Required(message='city')])
    neighborhood = TextField('Neighborhood', [
                Required(message='neighborhood')])

class LoginForm(Form):
    email    = TextField('Email Address', [Email(),
                Required(message='email')])
    password = PasswordField('Password', [
                Required(message='password')])
