from flask import Flask, render_template
import os
import subprocess
import asyncio
import threading
from queue import Queue
import json
import re
from flask import jsonify

# loop = asyncio.get_event_loop()
# db = SQLAlchemy()

app = Flask(__name__)
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

        if not linea_limpia:
            break
        
        ## Quitamos la última coma del último elemento para poder parsear el string a json con json.loads
        linea_limpia = linea_limpia[::-1].replace(",","",1)[::-1]

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


@app.route("/ejecuta/mesa/<id>")
def ejecuta_mesa(id):
        # global process
    command = ['python', '-u', 'C:\\Users\\David\\Desktop\\Github\\PopulationDynamicsModel_AI\\Code\\Simulation\\main.py']
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