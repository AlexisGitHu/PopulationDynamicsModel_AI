from flask import Blueprint

modulo_forms = Blueprint("modulo_forms", __name__, static_folder="static", template_folder="templates")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import EqualTo, DataRequired


class LoginForm(FlaskForm):
    username_or_email = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', id='password')
    show_password = BooleanField('Mostrar Contraseña', id='check')
    submit = SubmitField('Log in')


class SignUpForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    user_agreement = BooleanField('Acepto todos los acuerdos de licencia de usuario')
    submit = SubmitField('Sign up')


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
