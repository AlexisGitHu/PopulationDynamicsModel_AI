from flask import Flask, render_template
import os
import subprocess
import asyncio
import threading
from queue import Queue
import json
import re
import json
from flask_cors import CORS, cross_origin

loop = asyncio.get_event_loop()

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

datos = {}

def lectura_datos(process, id):
    global datos
    # Validar que el id es válido para no meter basura por si acaso

    while True:   # Could be more pythonic with := in Python3.8+
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        
        try:
            datos[id].append(line.decode())
        except:
            datos[id] = [line.decode()]

# def lectura_datos(process):    
#     while True:   # Could be more pythonic with := in Python3.8+
#         line = process.stdout.readline()
#         if not line and process.poll() is not None:
#             break
#         datos.append(line.decode())


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

# @app.route('/')
# def run_command():
#     # global process

#     command = ['python', 'Main.py', '--numLearningIterations', '20', '--totalNumIterations', '50']
#     # """Run a command while printing the live output"""
#     process = subprocess.Popen(
#         command,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT
#     )
    
#     thread = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process])
#     # thread.setDaemon(True)
#     thread.start()

#     return render_template('index.html')

# @app.route('/')
# async def run_command():
#     command = ['python', 'Main.py', '--numLearningIterations', '20', '--totalNumIterations', '20']
#     # """Run a command while printing the live output"""
#     process = subprocess.Popen(
#         command,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT
#     )
#     corrutina = lectura_datos(process)
#     task = asyncio.create_task(corrutina)



#     return render_template('index.html')

@app.route("/inicio/<id>")
def inicio(id):
    return render_template('index.html', user_id=id)

@app.route('/datos/<id>')
def data(id):
    datos_bien = list(filter(lambda a: a != "", datos[id]))
    # s = '\n'.join(datos)
    
    s = json.dumps(datos_bien)
    return s

@app.route('/pruebajson')
@cross_origin()
def pruebajson():
    #with open('ejemplo.json', 'r') as fcc_file:
     #   fcc_data = fcc_file.read()
       # print(fcc_data)
    fcc_data = [{"Iteration": 1, "Pred": 100, "prey": 368, "grass": 1264, "avg. prey death age": 0.62, "avg. pred death age": 0.00, "coord_x":500, "coord_y":218},
                {"Iteration": 2, "Pred": 100, "prey": 368, "grass": 1264, "avg. prey death age": 0.62, "avg. pred death age": 0.00, "coord_x":200, "coord_y":100},
                {"Iteration": 3, "Pred": 100, "prey": 311, "grass": 1379, "avg. prey death age": 2.75, "avg. pred death age": 0.00, "coord_x":826, "coord_y":49},
                {"Iteration": 4, "Pred": 100, "prey": 299, "grass": 1421, "avg. prey death age": 3.89, "avg. pred death age": 0.00, "coord_x":855, "coord_y":154},
                {"Iteration": 5, "Pred": 109, "prey": 315, "grass": 1445, "avg. prey death age": 4.93, "avg. pred death age": 0.00, "coord_x":802, "coord_y":333},
                {"Iteration": 6, "Pred": 111, "prey": 326, "grass": 1465, "avg. prey death age": 5.44, "avg. pred death age": 11.44, "coord_x":658, "coord_y":305},
                {"Iteration": 7, "Pred": 117, "prey": 329, "grass": 1494, "avg. prey death age": 6.53, "avg. pred death age": 12.56, "coord_x":965, "coord_y":228},
                {"Iteration": 8, "Pred": 116, "prey": 344, "grass": 1512, "avg. prey death age": 7.14, "avg. pred death age": 13.54, "coord_x":191, "coord_y":283},
                {"Iteration": 9, "Pred": 121, "prey": 341, "grass": 1537, "avg. prey death age": 7.95, "avg. pred death age": 14.15, "coord_x":356, "coord_y":435},
                {"Iteration": 10, "Pred": 134, "prey": 335, "grass": 1554, "avg. prey death age": 8.45, "avg. pred death age": 15.07, "coord_x":431, "coord_y":461},
                {"Iteration": 11, "Pred": 140, "prey": 335, "grass": 1552, "avg. prey death age": 8.89, "avg. pred death age": 15.79, "coord_x":247, "coord_y":199}]
    return fcc_data

@app.route("/", defaults={"id":None})
@app.route("/<id>")
def prueba(id):
    return datos
# @app.route('/')
# async def index():
#     run_command(['python', 'Main.py'])
#     # await asyncio.sleep(1)
#     return await render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)