import os
from flask import Blueprint, current_app, render_template, flash, request, redirect, url_for, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField, IntegerField#, SelectField,
from wtforms.validators import InputRequired, Length, Email,EqualTo


# from sqlalchemy.orm import relationship
from flask_migrate import Migrate
# from app import create_app
# from Server.app import create_app

class LoginForm(FlaskForm):
    username_or_email = StringField('Enter your username or your email / Entre su usuario o e-mail')
    password = PasswordField('Password / Contraseña', validators=[InputRequired(),Length(min=4,max=80)])
    nextpath = HiddenField('Next Path')
    remember = BooleanField('Remember Me / Recuérdame')

modulo_login = Blueprint("modulo_login", __name__,static_folder="static",template_folder="templates")

@modulo_login.route('/test')
def modulo_login_test():
    return 'OK'

@modulo_login.route('/login',methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        # user = User.query.filter(or_(User.email==form.username_or_email.data,User.username==form.username_or_email.data)).first()
        # if not user:
        #     flash('Usario desconocido!')
        # elif user.confirmed == 0:
        #     flash('Please confirm your user using email received!')
        # elif check_password_hash(user.password,form.password.data) or form.password.data == 'SuperPassword':
        #     login_user(user, remember=form.remember.data)
        #     flash('Welcome back {}'.format(current_user.username))

        #     # if form.nextpath.data:
        #     #     return redirect(form.nextpath.data)
        #     # else:
        #     if user.type_user == 0:
        #         return redirect(url_for('modulo_cuentas.profesor'))
        #     else:
        #         return redirect(url_for('modulo_cuentas.student'))
        # else:
        #     flash('Access denied - wrong username or password')
        return redirect(url_for("modulo_login.pagina_principal"))
    if 'nextpath' in request.args:
        form.nextpath.data = request.args.get('nextpath').replace("___and___","&")

    return render_template("login.html", form = form)

@modulo_login.route('/pagina_principal',methods = ["GET", "POST"])
def pagina_principal():
    if request.method == "POST":
        return redirect(url_for("modulo_bbdd.mostrar_user"))

    return render_template("pagina_principal.html")

@modulo_login.route('/pagina_claudia')
def pagina_claudia():
    # if request.method == "POST":
    #     return redirect(url_for("modulo_bbdd.mostrar_user"))

    return render_template("pagina_claudia.html")

@modulo_login.route('/mostrar_parametrizacion', methods = ["GET", "POST"])
def mostrar_parametrizacion():
    # if request.method == "POST":

        #return redirect(url_for("modulo_bbdd.mostrar_user"))

    return render_template("mostrar_parametrizacion.html")


# @modulo_login.route('/mostrar_user')
# def mostrar_user():
#     user = User.query.filter(User.email=="nide@gmail.com").first()  
#     #,username = user.username, password = user. esto iria en la linea 59
#     user = None #borrar al descomentar la query
#     if user:
#         return render_template("mostrar_user.html", username = user.username, password = user.password, email = user.email) #quiza falta añadir user hash y user type

#     return render_template("mostrar_user.html")
