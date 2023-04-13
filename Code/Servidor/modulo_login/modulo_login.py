import os
from flask import Blueprint, current_app, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# from sqlalchemy.orm import relationship
from flask_migrate import Migrate
# from app import create_app
# from Server.app import create_app


modulo_login = Blueprint("modulo_login", __name__,static_folder="static",template_folder="templates")

@modulo_login.route('/test')
def modulo_login_test():
    return 'OK'

@modulo_login.route('/login')
def login():

    return render_template("index.html")
