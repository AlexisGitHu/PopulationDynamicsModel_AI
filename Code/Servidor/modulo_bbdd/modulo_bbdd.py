import os
from flask import Blueprint, current_app, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# from sqlalchemy.orm import relationship
from flask_migrate import Migrate
# from app import create_app
# from Server.app import create_app


modulo_bbdd = Blueprint("modulo_bbdd", __name__,static_folder="static",template_folder="templates")

@modulo_bbdd.route('/modulo_bbdd/test')
def modulo_bbdd_test():
    return 'OK'

# db = create_app()
db = SQLAlchemy(current_app)
db.init_app(current_app)

# migrate = Migrate(current_app, db)


# class Migracion(db.Model):
#     __tablename__='migracion'
#     id = db.Column(db.Integer, primary_key=True)
    
#     def as_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# LOGIN
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    confirmed = db.Column(db.Integer, default=0)
    userhash = db.Column(db.String(50))
    type_user = db.Column(db.Integer, default=1) # 0 es admin, 1 es usuario


    # alumno = db.relationship('User_Group_Class', backref='user')


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


################################################################################
# db.create_all tiene que ir debajo de todas las tablas
db.create_all()
################################################################################

# Para ver cómo se hacían las FK

# class User_Group_Class(db.Model):
#     __tablename__='grupos_clase'
#     id = db.Column(db.Integer, primary_key=True)
#     # ALVARO O JORGE: LA TUPLA DE ESTUDIANTE Y FILENAME DEBE SER ÚNICA
#     # (En la inserción de datos os debeís de asegurar de que esta tupla es única (en el caso de que te vayan a meter algún dato donde esta condición falle, sobreescribir la tupla anterior))
#     encuesta = db.Column(db.String(20), db.ForeignKey('clases.name'))
#     email = db.Column(db.String(50), db.ForeignKey('user.email'))
#     student_group = db.Column(db.String(80))

#     #id_ref_1 = db.relationship('GroupGrading', backref='grupos_clase')
#     #id_ref_2 = db.relationship('PeerGrading', backref='grupos_clase')
#     # clases = db.relationship('Classes', backref='grupos_clase')

#     def as_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}



def create_user():
    try:
        new_user = User (
            # username=form.username.data,
            username="Pedro",
            # email = form.email.data,
            email = "nide@gmail.com",
            # password = password_hashed,
            password = "password_hashed",
            # userhash = userhash,
            userhash = "",
            # type_user = form.type_user.data
            type_user = 1
        )

        db.session.add(new_user)
        db.session.commit()

        return 'Usuario creado con éxito!'

    except:
        db.session.rollback()
        
        return 'Este nombre de usuario o correo ya existe, introduce otro'

@modulo_bbdd.route('/modulo_bbdd/create_user')
def modulo_bbdd_create_user():

    prueba = create_user()

    return prueba
