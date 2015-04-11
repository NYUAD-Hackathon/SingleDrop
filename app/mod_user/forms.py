# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class EditForm(Form):

    phone    = TextField('Phone number', [
                Required(message='Forgot your phone number?')])
    city = TextField('City', [
                Required(message='Must provide a city')])
    neighborhood = TextField('Neighborhood', [
                Required(message='Must provide a neighborhood')])
