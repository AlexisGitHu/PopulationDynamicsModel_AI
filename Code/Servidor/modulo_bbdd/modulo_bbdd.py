from flask import Blueprint, current_app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = SQLAlchemy(current_app)

modulo_bbdd = Blueprint("modulo_bbdd", __name__, static_folder="static", template_folder="templates")


class User(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(60), unique=True)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }


db.create_all()


class Modelo(db.Model):
    __tablename__ = 'modelos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    url = db.Column(db.String(100), unique=True)
    creador = db.Column(db.String(100))
    fecha_creacion = db.Column(db.String(100))
    compartir = db.Column(db.String(100), unique=True)
    publico = db.Column(db.Boolean)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'url': self.url,
            'creador': self.creador,
            'fecha_creacion': self.fecha_creacion,
            'compartir': self.compartir,
            'publico': self.publico
        }


db.create_all()


class Permisos(db.Model):
    __tablename__ = 'permisos'
    id_modelo = db.Column(db.Integer, db.ForeignKey('modelos.id'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    modelo = db.relationship("Modelo", backref=backref("modelos", uselist=False))
    usuario = db.relationship("User", backref=backref("usuarios", uselist=False))

    __table_args__ = (
        db.PrimaryKeyConstraint(
            id_modelo, id_usuario,
        ),
    )

    @property
    def serialize(self):
        return {
            'id_modelo': self.id_modelo,
            'id_usuario': self.id_usuario,
        }


db.create_all()


@modulo_bbdd.route('/modulo_bbdd/test')
def modulo_bbdd_test():
    db.create_all()

    '''
    user = User(username="prueba", email="prueba@prueba.es")
    user.set_password("test")
    modelo = Modelo(nombre="prueba", url="prueba", creador="prueba" ,fecha_creacion="prueba", compartir=str(uuid.uuid4()))
    permiso = Permisos(id_modelo=1, id_usuario=1)

    try:
        db.session.add(user)
        db.session.add(modelo)
        db.session.add(permiso)
        db.session.commit()
    except:
        db.session.rollback()
        return 'ERROR'
    '''

    return 'OK'
