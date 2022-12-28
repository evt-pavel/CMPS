from wtforms import StringField, PasswordField, BooleanField, SubmitField, Form
from wtforms.validators import DataRequired, Email, InputRequired


class LoginForm(Form):
    email = StringField('Email Address')  # , [Email(), DataRequired(message='Enter Email!')])
    password = PasswordField('Password')  # , [DataRequired(message='Enter Password!')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

