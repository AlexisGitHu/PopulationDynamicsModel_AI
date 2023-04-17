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

# Iniciamos la app y distintas aplicaciones
app = Flask(__name__)
CORS(app)
bootstrap = Bootstrap(app)

# Configuramos la aplicacion con la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/prueba.db"
app.config['SECRET_KEY'] = '37utopisdr jt ñçã3q0r9irjqwasdaADFSADF3q0r9irjqw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Imports para registrar los modulos
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



# datos = {}
datosMesa = {}


#################################################### PODEMOS ELIMINARLO ########################################################
# def lectura_datos(process, id):
#     global datos
#     # Validar que el id es válido para no meter basura por si acaso

#     while True:   # Could be more pythonic with := in Python3.8+        
        
#         line = process.stdout.readline()
#         # line2 = process.stdout.read().splitlines()
#         if not line and process.poll() is not None:
#             break
        
#         linea_sucia = line.decode()
#         linea_limpia = linea_sucia.replace("\r\n", "").replace("\\\"", "\'")

#         if not linea_limpia:
#             break

#         try:
#             datos[id].append(json.loads(linea_limpia))
#         except:
#             datos[id] = [json.loads(linea_limpia)]
################################################################################################################################


# Función que lee de un stdout los logs del modelo de entrenamiento
def lectura_datos_mesa(process, id):
    global datosMesa
    #### IMPORTANTE!! Validar que el id es válido para no meter basura por si acaso

    while True:      
        
        line = process.stdout.readline()

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

        # Insertar en la lista si no está vacía y si no existen datos meterlos
        try:
            datosMesa[id].append(json.loads(linea_limpia))
        except:
            datosMesa[id] = [json.loads(linea_limpia)]


#################################################### PODEMOS ELIMINARLO ########################################################
# @app.route('/modelo/<iter>/<id>')
# def run_command(iter, id):
#     # global process

#     command = ['python', '-u', 'Main.py', '--numLearningIterations', '20', '--totalNumIterations', str(iter)]
#     # command = ['python', 'Mesa_trial.py']

#     # """Run a command while printing the live output"""
#     process = subprocess.Popen(
#         command,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT
#     )
    
#     thread = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process, id])
#     # thread2 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
#     # thread3 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
#     # thread4 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
#     # thread5 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
#     # thread6 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
#     # thread7 = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
    

#     # thread.setDaemon(True)
#     thread.start()
#     # thread2.start()
#     # thread3.start()
#     # thread4.start()
#     # thread5.start()
#     # thread6.start()
#     # thread7.start()


#     return "Entrenando modelo"
################################################################################################################################


# Ruta para ejecutar un modelo
@cross_origin()
@app.route("/ejecuta/mesa/<id>")
def ejecuta_mesa(id):
        # global process

    ### IMPORTANTE !!! Decidir cómo hacer que seleccione un modelo para q pueda seguir entrenandolo o simplemente ejecutarlo
    ### Es decir, ver si pasar como parametros un posible modelo tras haber rellenado un formulario
    command = ['python', '-u', '..\\Simulation\\main.py']

    # """Run a command while printing the live output"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    thread = threading.Thread(name='lectura_datos', target=lectura_datos_mesa, args=[process, id])
    
    thread.start()


    return "Entrenando modelo"


################################### POSIBLE FUNCION CONJUNTA PARA LA GRAFICA Y VISUALIZACIÓN ###################################
# @app.route("/get_data/<id>")
# def get_data(id):
#     if id in datosMesa:
#         datos_nuevos = datosMesa[id]
#         datosMesa[id] = []
#     else:
#         datos_nuevos = []

#     ret_datos = []

#     if len(datos_nuevos) > 0:
#         datos_visualizar = datos_nuevos
#         datos_grafica = get_graph_data(datos_nuevos) <- Tratar los datos con esta funcion en base a los datos pasados y que me devuelva los steps y los contadores

#         ret_datos = [datos_visualizar, datos_grafica]
    
#     return ret_datos
################################################################################################################################


# Ruta para ver datos nuevos del modelo
@app.route("/muestra/mesa/<id>")
def muestra_mesa(id):
    if id in datosMesa:
        datos_nuevos = datosMesa[id]
        datosMesa[id] = []
    else:
        datos_nuevos = []

    return jsonify(datos_nuevos)
    


#################################################### PODEMOS ELIMINARLO ########################################################
# @app.route("/inicio/<iter>/<id>")
# def inicio(iter, id):
#     return render_template('index.html', user_id=id, iters=iter)
################################################################################################################################


#################################################### PODEMOS ELIMINARLO ########################################################
# @app.route('/prueba/<id>')
# def prueba_json(id):
#     # datos_bien = list(filter(lambda a: a != "", datos[id]))
#     # datos_bien2 = list(filter(lambda a: a != "", datos2[id]))
#     # s = '\n'.join(datos)
#     # print(type(datos_bien))
#     # print(datos_bien)
#     # print(datos_bien2)
#     # print(datos[id])
#     # datos_nuevos = datos[id]
#     # for i in datos_nuevos:
#     #     datos[id].remove(i)

#     # return datos_nuevos
#     if id in datos:
#         return jsonify(datos[id])
#     else:
#         return jsonify([])
################################################################################################################################




# Imports necesarios para calcular las ecuaciones teoricas para el modelo de poblaciones
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

sol_lv = None
lim_theoretical_step = 200

# Definición de la funcion de lotka volterra
def lotkavolterra(t, x, rl, alpha, rz, beta):
    return np.array([rl*x[0] - alpha*x[0]*x[1], -rz*x[1] + beta*x[0]*x[1]])

# Funcion para actualizar datos de la funcion de lotka volterra teorica (dependientes del numero de especies que haya en un momento)
def data_loktavolterra(x_init):
    # Linea para poder actualizar el valor de la variable global sol_lv
    global sol_lv

    t_span = (lim_theoretical_step-200, lim_theoretical_step)
    t_eval = np.linspace(t_span[0], t_span[1], 1000)


    # Si se quiere ampliar el periodo (la frecuencia de las puntas del teorico) dividir entre numeros más grandes, si se quiere más frecuencia multiplicar o dividir entre menos (/2, /3)
    # Parametros para indicar tasa de crecimiento de los conejos, zorros y tasa de muertes de conejos por zorros
    rl = 1.2/8
    alpha = 0.25/8
    rz = 2/8
    beta = 0.5/8

    sol_lv = solve_ivp(lotkavolterra, t_span, x_init, args=(rl, alpha, rz, beta), t_eval=t_eval)

### Hay un error que salta al final de la ejecución cuando tiramos el servidor con crtl + c que scipy da un error en esta url está la solución pero no sé si merece la pena
# forrtl: error (200): program aborting due to control-C event
# Image              PC                Routine            Line        Source
# libifcoremd.dll    00007FFE6FFA3B58  Unknown               Unknown  Unknown
# KERNELBASE.dll     00007FFF06F52603  Unknown               Unknown  Unknown
# KERNEL32.DLL       00007FFF08E37604  Unknown               Unknown  Unknown
# ntdll.dll          00007FFF092426A1  Unknown               Unknown  Unknown
###################### https://stackoverflow.com/questions/15457786/ctrl-c-crashes-python-after-importing-scipy-stats ##########################




# Initialize the data of loktavolterra equations
x_init = (5,5)
data_loktavolterra(x_init)

import math
# Funcion para recoger datos de la solucion numerica de lotka volterra dados unos steps
def get_loktavolterra_data(steps):
    global lim_theoretical_step

    # Contadores para contar el numero de animales por cada especie
    contadores = []

    # Recorremos todos los steps
    for step in steps:
        # En el caso de que se haya pasado el limite hasta el que se había resuelto numericamente las ecuaciones de lotka volterra, actualizamos los datos
        if step >= lim_theoretical_step:
            lim_theoretical_step += 200
            # Cogemos el actual numero de animales de cada especie y resolvemos de nuevo
            x_init_nuevo = (sol_lv.y[0][-1], sol_lv.y[1][-1])
            data_loktavolterra(x_init_nuevo)

        # Cojemos el indice tal que se aproxime más a nuestro step, ya que en la resolucion se va de 0.0X en 0.0X
        t_idx = np.argmin(np.abs(sol_lv.t - step))

        # Cojemos los valores de 'conejos' y 'lobos' en t=step
        conejos = sol_lv.y[0][t_idx]
        lobos = sol_lv.y[1][t_idx]
        
        contadores.append((math.ceil(lobos), math.ceil(conejos)))

    # Devolvemos esos contadores
    return contadores

# Ruta para devolver datos de cuantos animales de cada tipo hay
@app.route("/get_graph_data")
def get_graph_data():

    ### IMPORTANTE!!! Hacer que esto de datos nuevos sean temporales para que distintas rutas puedan devolver distinta informacion de esos mismos datos


    datos_nuevos = None
    datos_validos = []
    # print(datosMesa)

    ### IMPORTANTE!!! En vez de mirar "1" in datosMesa, mirar si el id de la persona loggeada está en datosMesa (por si ha entrenado un modelo)
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
    
    # En el caso de que se hayan recogido datos, poner los steps, los contadores actuales y los contadores teoricos
    if len(steps) > 0:
        theorical_data = get_loktavolterra_data(steps)
        datos_validos = [steps, contadores, theorical_data]


    response = make_response(json.dumps(datos_validos))

    response.content_type = "application/json"
    # print(datos_validos)

    return response

@app.route("/graph_data")
def graph_data():
    return render_template('grafica.html')

#################################################### PODEMOS ELIMINARLO ########################################################
# @app.route("/datos_nuevos/<id>")
# def f_datos_nuevos(id):
#     if id in datos:
#         datos_nuevos = datos[id]
#         datos[id] = []
#     else:
#         datos_nuevos = []

#     return jsonify(datos_nuevos)
################################################################################################################################

    
####################################### PODEMOS ELIMINARLO O CAMBIAR LO QUE SE DEVUELVE ########################################
# @app.route("/", defaults={"id":None})
# @app.route("/<id>")
# def prueba(id):
#     return datos
################################################################################################################################

if __name__ == "__main__":
    app.run(debug=True)