from flask import flash, render_template
from flask import request
from flask_login import LoginManager, login_required, login_user, logout_user
from wtforms import ValidationError

from modulo_funcionesAux.modulo_funcionesAux import *
from modulo_bbdd.modulo_bbdd import *
from modulo_login.modulo_login import *
from modulo_forms.modulo_forms import *

import datetime

modulo_modelos = Blueprint("modulo_modelos", __name__, static_folder="static", template_folder="templates")


@modulo_modelos.route('/modelos', methods=['GET', 'POST'])
@login_required
def modelos():
    formCrearModelo = CrearModeloForm()
    formAnadirModelo = AnadirModeloForm()
    if request.method == 'POST':
        if formCrearModelo.validate_on_submit():
            modelo = Modelo(nombre=formCrearModelo.nombre.data, url=formCrearModelo.url.data,
                            creador=current_user.username, fecha_creacion=datetime.date.today(),
                            compartir=str(uuid.uuid4()), publico=formCrearModelo.publico.data)

            db.session.add(modelo)
            db.session.commit()

            modelo = Modelo.query.filter_by(compartir=modelo.compartir).first()
            permisos = Permisos(id_usuario=current_user.id, id_modelo=modelo.id)
            db.session.add(permisos)
            db.session.commit()

            flash("Modelo creado correctamente")
            return redirect(url_for('modulo_modelos.modelos'))

        elif formAnadirModelo.validate_on_submit():
            modelo = Modelo.query.filter_by(compartir=formAnadirModelo.codigo.data).first()
            if modelo is None:
                flash("No existe ningún modelo con ese código")
                return redirect(url_for('modulo_modelos.modelos'))

            else:
                print(current_user.id)
                print(modelo.id)
                if Permisos.query.filter_by(id_usuario=current_user.id, id_modelo=modelo.id).first() is not None:
                    flash("Ya tienes acceso a ese modelo")
                    return redirect(url_for('modulo_modelos.modelos'))
                else:
                    permiso = Permisos(id_usuario=current_user.id, id_modelo=modelo.id)
                    db.session.add(permiso)
                    db.session.commit()
                    flash("Modelo añadido correctamente")
                    return redirect(url_for('modulo_modelos.modelos'))

    else:
        listaModelos = Modelo.query.join(Permisos, Permisos.id_modelo == Modelo.id) \
            .filter(Permisos.id_usuario == current_user.id).all()

        modelos = [x.serialize for x in listaModelos]
        for x in modelos:
            x['id'] = "modal" + str(x['id'])
            x['modalId'] = "#" + x['id']

        return render_template('modelos.html', modelos=modelos, formCrearModelo=formCrearModelo,
                               formAnadirModelo=formAnadirModelo)


@modulo_modelos.route('/comunidad')
@login_required
def comunidad():
    listaModelos = Modelo.query.filter_by(publico=True).all()

    modelos = [x.serialize for x in listaModelos]
    return render_template('comunidad.html', modelos=modelos)