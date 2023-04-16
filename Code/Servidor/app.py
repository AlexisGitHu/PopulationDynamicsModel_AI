from flask import Flask, render_template, make_response
import os
import subprocess
import asyncio
import threading
from queue import Queue
import json
import re
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap


import mpld3
# loop = asyncio.get_event_loop()
# db = SQLAlchemy()

app = Flask(__name__)
CORS(app)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/prueba.db"
app.config['SECRET_KEY'] = '37utopisdr jt ñçã3q0r9irjqwasdaADFSADF3q0r9irjqw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    from Servidor.modulo_bbdd.modulo_bbdd import *
    from Servidor.modulo_login.modulo_login import *

app.register_blueprint(modulo_bbdd)
app.register_blueprint(modulo_login)


# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}?auth_plugin=mysql_native_password".format(
#   username=get_configuration()["MYSQL_USERNAME"],
#   password=get_configuration()["MYSQL_PASSWORD"],
#   hostname=get_configuration()["MYSQL_HOSTNAME"],
#   databasename=get_configuration()["MYSQL_DATABASENAME"]
#   )

# with app.app_context():
#     from modulo_bbdd.modulo_bbdd import *
# app.register_blueprint(modulo_bbdd)


# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/prueba.db"

# app.config['SECRET_KEY'] = '37utopisdr jt ñçã3q0r9irjqwasdaADFSADF3q0r9irjqw'




datos = {}
datosMesa = {}

def lectura_datos(process, id):
    global datos
    # Validar que el id es válido para no meter basura por si acaso

    while True:   # Could be more pythonic with := in Python3.8+        
        
        line = process.stdout.readline()
        # line2 = process.stdout.read().splitlines()
        if not line and process.poll() is not None:
            break
        
        linea_sucia = line.decode()
        linea_limpia = linea_sucia.replace("\r\n", "").replace("\\\"", "\'")

        if not linea_limpia:
            break

        try:
            datos[id].append(json.loads(linea_limpia))
        except:
            datos[id] = [json.loads(linea_limpia)]


def lectura_datos_mesa(process, id):
    global datosMesa
    # Validar que el id es válido para no meter basura por si acaso

    while True:   # Could be more pythonic with := in Python3.8+        
        
        line = process.stdout.readline()
        # line2 = process.stdout.read().splitlines()
        if not line and process.poll() is not None:
            break
        
        linea_sucia = line.decode('latin-1')
        linea_limpia = linea_sucia.replace("\r\n", "").replace("\\\"", "\'")

        if "Interface starting at" in linea_limpia:
            continue
        if "WARNING" in linea_limpia:
            continue
        if not linea_limpia:
            continue
        
        ## Quitamos la última coma del último elemento para poder parsear el string a json con json.loads
        linea_limpia = linea_limpia[::-1].replace(",","",1)[::-1]
        # print(linea_limpia)

        try:
            datosMesa[id].append(json.loads(linea_limpia))
        except:
            datosMesa[id] = [json.loads(linea_limpia)]


@app.route('/modelo/<iter>/<id>')
def run_command(iter, id):
    # global process

    command = ['python', '-u', 'Main.py', '--numLearningIterations', '20', '--totalNumIterations', str(iter)]
    # command = ['python', 'Mesa_trial.py']

    # """Run a command while printing the live output"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    thread = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process, id])
    # thread2 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
    # thread3 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
    # thread4 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
    # thread5 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
    # thread6 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
    # thread7 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
    

    # thread.setDaemon(True)
    thread.start()
    # thread2.start()
    # thread3.start()
    # thread4.start()
    # thread5.start()
    # thread6.start()
    # thread7.start()


    return "Entrenando modelo"



@cross_origin()
@app.route("/ejecuta/mesa/<id>")
def ejecuta_mesa(id):
        # global process
    command = ['python', '-u', '..\\Simulation\\main.py']
    # command = ['python', 'Mesa_trial.py']

    # """Run a command while printing the live output"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    thread = threading.Thread(name='lectura_datos', target=lectura_datos_mesa, args=[process, id])
    
    thread.start()


    return "Entrenando modelo"


@app.route("/muestra/mesa/<id>")
def muestra_mesa(id):
    if id in datosMesa:
        datos_nuevos = datosMesa[id]
        datosMesa[id] = []
    else:
        datos_nuevos = []

    return jsonify(datos_nuevos)
    


@app.route("/inicio/<iter>/<id>")
def inicio(iter, id):
    return render_template('index.html', user_id=id, iters=iter)


@app.route('/prueba/<id>')
def prueba_json(id):
    # datos_bien = list(filter(lambda a: a != "", datos[id]))
    # datos_bien2 = list(filter(lambda a: a != "", datos2[id]))
    # s = '\n'.join(datos)
    # print(type(datos_bien))
    # print(datos_bien)
    # print(datos_bien2)
    # print(datos[id])
    # datos_nuevos = datos[id]
    # for i in datos_nuevos:
    #     datos[id].remove(i)

    # return datos_nuevos
    if id in datos:
        return jsonify(datos[id])
    else:
        return jsonify([])


# Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

periodicity = 0
sol_lv = None
lim_theoretical_step = 200


def lotkavolterra(t, x, rl, alpha, rz, beta):
    return np.array([rl*x[0] - alpha*x[0]*x[1], -rz*x[1] + beta*x[0]*x[1]])

def data_loktavolterra(x_init):
    # from scipy.signal import argrelextrema
    global periodicity
    global sol_lv

    t_span = (lim_theoretical_step-200, lim_theoretical_step)
    t_eval = np.linspace(t_span[0], t_span[1], 1000)
    # x_init = (5, 5)
    # rl = 0.1
    # alpha = 0.0015
    # rz = 2
    # beta = 0.015
    rl = 1.2/8
    alpha = 0.25/8
    rz = 2/8
    beta = 0.5/8

    sol_lv = solve_ivp(lotkavolterra, t_span, x_init, args=(rl, alpha, rz, beta), t_eval=t_eval)


    # # Find the indices of all maxima in the 'liebres' component
    # maxima_idx = argrelextrema(sol_lv.y[0], np.greater)[0]
    # t_maxima_conejos = sol_lv.t[maxima_idx]
    # # Find the indices of all minima in the 'liebres' component
    # minima_idx = argrelextrema(sol_lv.y[0], np.less)[0]
    # t_minima_conejos = sol_lv.t[minima_idx]

    # print(f"The 'liebres' component reaches its maxima at t = {t_maxima_conejos} and its minima at t = {t_minima_conejos}.")

    # # Find the indices of all maxima in the 'zorros' component
    # maxima_idx = argrelextrema(sol_lv.y[1], np.greater)[0]
    # t_maxima_lobos = sol_lv.t[maxima_idx]
    # # Find the indices of all minima in the 'zorros' component
    # minima_idx = argrelextrema(sol_lv.y[1], np.less)[0]
    # t_minima_lobos = sol_lv.t[minima_idx]

    # print(f"The 'zorros' component reaches its maxima at t = {t_maxima_lobos} and its minima at t = {t_minima_lobos}.")

    # periodic_maxima_conejos = t_maxima_conejos[1]-t_maxima_conejos[0]
    # # print(periodic_maxima_conejos)
    # periodic_minima_conejos = t_minima_conejos[1]-t_minima_conejos[0]
    # # print(periodic_minima_conejos)

    # periodic_maxima_lobos = t_maxima_lobos[1]-t_maxima_lobos[0]
    # # print(periodic_maxima_lobos)
    # periodic_minima_lobos = t_minima_lobos[1]-t_minima_lobos[0]
    # # print(periodic_minima_lobos)

    # conditions = [abs(periodic_maxima_conejos - periodic_maxima_lobos) < 0.001, 
    #               abs(periodic_maxima_conejos - periodic_minima_lobos) < 0.001,
    #               abs(periodic_minima_conejos - periodic_minima_lobos) < 0.001,
    #               abs(periodic_minima_conejos - periodic_maxima_lobos) < 0.001]
    
    # if conditions.index(True) < 2:
    #     periodicity = round(periodic_maxima_conejos,4)
    # else:
    #     periodicity = round(periodic_minima_conejos,4)
    


###################### https://stackoverflow.com/questions/15457786/ctrl-c-crashes-python-after-importing-scipy-stats ##########################


# Initialize the data of loktavolterra equations
x_init = (5,5)
data_loktavolterra(x_init)

import math
def get_loktavolterra_data(steps):
    global lim_theoretical_step

    # steps = []
    contadores = []

    for step in steps:
        # Get the indices of the element in 't_eval' closest to t=step
        if step >= lim_theoretical_step:
            lim_theoretical_step += 200
            x_init_nuevo = (sol_lv.y[0][-1], sol_lv.y[1][-1])
            data_loktavolterra(x_init_nuevo)
            # step -= periodicity

        t_idx = np.argmin(np.abs(sol_lv.t - step))

        # Get the values of 'conejos' and 'lobos' at t=step
        conejos = sol_lv.y[0][t_idx]
        lobos = sol_lv.y[1][t_idx]
        
        contadores.append((math.ceil(lobos), math.ceil(conejos)))

    return contadores

@app.route("/get_graph_data")
def get_graph_data():
    datos_nuevos = None
    datos_validos = []
    # print(datosMesa)
    if "1" in datosMesa:
        datos_nuevos = datosMesa["1"]
        datosMesa["1"] = []
    else:
        datos_nuevos = []
    

    step = 0
    cont_lobos = 0
    cont_conejos = 0
    steps = []
    contadores = []

    for i in datos_nuevos:
        step = i["Step"]
        info = i["info"]

        steps.append(step)

        for j in info:
            if "lobo.png" in j.values():
                cont_lobos += 1
            elif "conejo.png" in j.values():
                cont_conejos += 1
        
        contadores.append((cont_lobos, cont_conejos))
        cont_lobos = 0
        cont_conejos = 0
    

    if len(steps) > 0:
        theorical_data = get_loktavolterra_data(steps)
        datos_validos = [steps, contadores, theorical_data]




    response = make_response(json.dumps(datos_validos))

    response.content_type = "application/json"
    print(datos_validos)

    return response


import numpy as np
import matplotlib.pyplot as plt
from mpld3 import plugins
import pandas as pd

@app.route("/graph_data")
def graph_data():
    # np.random.seed(9615)

    # # generate df
    # N = 100
    # df = pd.DataFrame((.1 * (np.random.random((N, 5)) - .5)).cumsum(0),
    #                 columns=['a', 'b', 'c', 'd', 'e'],)

    # # plot line + confidence interval
    # fig, ax = plt.subplots()
    # ax.grid(True, alpha=0.3)

    # for key, val in df.iteritems():
    #     l, = ax.plot(val.index, val.values, label=key)
    #     ax.fill_between(val.index,
    #                     val.values, val.values,
    #                     color=l.get_color(), alpha=.4)

    # # define interactive legend

    # handles, labels = ax.get_legend_handles_labels() # return lines and labels
    # interactive_legend = plugins.InteractiveLegendPlugin(zip(handles,
    #                                                         ax.collections),
    #                                                     labels,
    #                                                     start_visible=True)
    # plugins.connect(fig, interactive_legend)

    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_title('Interactive legend', size=20)


    # # json01 = json.dumps(mpld3.fig_to_dict(fig))
    # html_graph = mpld3.fig_to_html(fig)
    # return render_template('grafica.html', json1=html_graph, graph= [html_graph])
    return render_template('grafica.html')

@app.route("/datos_nuevos/<id>")
def f_datos_nuevos(id):
    if id in datos:
        datos_nuevos = datos[id]
        datos[id] = []
    else:
        datos_nuevos = []

    return jsonify(datos_nuevos)
    

@app.route("/", defaults={"id":None})
@app.route("/<id>")
def prueba(id):
    return datos

if __name__ == "__main__":
    app.run(debug=True)