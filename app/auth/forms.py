from wtforms import StringField, PasswordField, BooleanField, SubmitField, Form
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import scoped_session
from app.models import User


class LoginForm(Form):
    email = StringField('Email Address', [Email(), DataRequired(message='Enter Email!')])
    password = PasswordField('Password', [DataRequired(message='Enter Password!')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(Form):
    name = StringField("Name*", [DataRequired(message='Введите ваше имя!')])
    last_name = StringField("Last name*", [DataRequired(message='Введите вашу фамилию!')])
    email = StringField("Email*", [DataRequired(message='Введите адрес эл. почты!'), Email()])
    password = PasswordField('Password*', [DataRequired(message='Введите пароль')])
    repeat_password = PasswordField('Repeat password', [EqualTo('password', message='Повторите пароль!')])
    submit = SubmitField('Register!')

    def validate_email(self, email):
        with scoped_session() as session:
            user = session.query(User).filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')




