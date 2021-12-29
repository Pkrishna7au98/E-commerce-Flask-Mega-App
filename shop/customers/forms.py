from flask_wtf import FlaskForm, Form
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, FileField
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from .model import Register

class CustomerRegisterForm(Form):
    name  = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo(['confirm', 'Both password must match'])])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    country = StringField('Country',  [validators.DataRequired()])
    state = StringField('State', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    contact = StringField('Contact Number', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])
    zipcode = StringField('Zip Code', [validators.DataRequired()])

    accept_tos = BooleanField('I accept the Terms & Conditions', [validators.DataRequired()]) 
    profile = FileField('Profile')

    submit = SubmitField('Register')

    # def validate_username(self, field):
    #     if Register.query.filter_by(username = field.data).first():
    #         raise ValidationError('This is Username already in use')

    # def validate_email(self, field):
    #     if Register.query.filter_by(email = field.data).first():
    #         raise ValidationError('This Email is already in use')
 
class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])

