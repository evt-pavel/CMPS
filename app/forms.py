from wtforms import StringField, PasswordField, BooleanField, SubmitField, Form
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import Session
from app.models import User


class LoginForm(Form):
    email = StringField('Email Address', [Email(), DataRequired(message='Enter Email!')])
    password = PasswordField('Password', [DataRequired(message='Enter Password!')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(Form):
    name = StringField("Name*", [DataRequired(message='Enter your name!')])
    last_name = StringField("Last name*", [DataRequired(message='Enter your last name!')])
    email = StringField("Email*", [DataRequired(message='Enter email!'), Email()])
    password = PasswordField('Password*', [DataRequired(message='Pick a password')])
    repeat_password = PasswordField('Repeat password', [EqualTo('password', message='Pick a password')])
    submit = SubmitField('Register!')

    def validate_email(self, email):
        with Session() as session:
            user = session.query(User).filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')




