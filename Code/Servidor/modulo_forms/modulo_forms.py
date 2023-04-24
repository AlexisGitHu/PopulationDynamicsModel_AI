from flask import Blueprint

modulo_forms = Blueprint("modulo_forms", __name__, static_folder="static", template_folder="templates")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import EqualTo, DataRequired


class LoginForm(FlaskForm):
    username_or_email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', id='password')
    show_password = BooleanField('Show password', id='check')
    submit = SubmitField('Submit')
    remember = BooleanField('Remember Me / Recuérdame')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    user_agreement = BooleanField('I accept all user license agreements')
    submit = SubmitField('Submit')


class CrearModeloForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    publico = BooleanField('Hacer Público el Modelo')
    submit = SubmitField('Crear')


class AnadirModeloForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired()])
    submit = SubmitField('Añadir')


@modulo_forms.route('/modulo_forms/test')
def modulo_forms_test():
    return 'OK'
