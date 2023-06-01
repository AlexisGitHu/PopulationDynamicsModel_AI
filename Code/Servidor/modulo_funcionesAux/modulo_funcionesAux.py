from flask import Blueprint, current_app, url_for, redirect, make_response
from flask_login import current_user

modulo_funcionesAux = Blueprint("modulo_funcionesAux", __name__, static_folder="static", template_folder="templates")

ALLOWED_EXTENSIONS = {'xlsx'}
is_authenticated = False
current_tab = "modelos"


def set_authenticated(value=True):
    global is_authenticated
    is_authenticated = value


def get_authenticated():
    global is_authenticated
    return is_authenticated


def set_current_tab(tab):
    global current_tab
    current_tab = tab


def get_current_tab():
    global current_tab
    return current_tab


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def llamada_login_con_nextpath(nexpath):
    if not current_user.is_authenticated:
        response = make_response(redirect(url_for('modulo_login.login',
                                                  nextpath=nexpath)))
        return response


def generarEnlace(id):
    return "localhost:5000/nuevoProyecto?project_id=" + str(id)


@current_app.context_processor
def utility_processor():
    def get_authenticated():
        global is_authenticated
        return is_authenticated

    def get_current_tab():
        global current_tab
        return current_tab

    return dict(get_authenticated=get_authenticated, get_current_tab=get_current_tab)


