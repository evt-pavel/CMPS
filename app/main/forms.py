from wtforms import StringField, SubmitField, Form
from wtforms.validators import DataRequired


class RegistrationOrder(Form):
    address = StringField("Address", [DataRequired(message='Введите адрес доставки!')])
    submit = SubmitField('Заказать!')