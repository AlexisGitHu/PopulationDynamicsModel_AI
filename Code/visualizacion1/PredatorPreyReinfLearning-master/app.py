from flask import Flask, render_template
import os
import subprocess
import asyncio
import threading
from queue import Queue
import json
import re
from flask import jsonify
from flask_cors import CORS, cross_origin

loop = asyncio.get_event_loop()

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

datos = {}
# datos2 = {}

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
        try:
            datos[id].append(json.loads(linea_limpia))
            # datos2[id].append(line2)
        except:
            datos[id] = [json.loads(linea_limpia)]
            # datos2[id] = [line2]

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

@app.route("/inicio/<iter>/<id>")
def inicio(iter,id):
    return render_template('index.html', user_id=id,iter=iter)

@app.route('/datos/<id>')
def data(id):
    datos_bien = list(filter(lambda a: a != "", datos[id]))
    # s = '\n'.join(datos)
    
    s = json.dumps(datos_bien)
    return s




@app.route('/prueba/<id>')
@cross_origin()
def prueba_json(id):
    datos_bien = list(filter(lambda a: a != "", datos[id]))
    # datos_bien2 = list(filter(lambda a: a != "", datos2[id]))
    # s = '\n'.join(datos)
    # print(type(datos_bien))
    # print(datos_bien)
    # print(datos_bien2)
    # print(datos[id])
    return jsonify(datos[id])



@app.route("/", defaults={"id":None})
@app.route("/<id>")
def prueba(id):
    return datos
# @app.route('/')
# async def index():
#     run_command(['python', 'Main.py'])
#     # await asyncio.sleep(1)
#     return await render_template('index.html')



@app.route("/devolver")
def devolver():
    fcc_data = [
    {
        "Step": 0, 
        "info": 
        [
          {
            "Alive": "True", 
            "Direction": "N", 
            "id": 1, 
            "Position": [
              4, 
              6
            ], 
            "Sprite": "conejo.png"
          }, 
          {
            "Alive": "True", 
            "Direction": "N", 
            "id": 2, 
            "Position": [
              1, 
              7
            ], 
            "Sprite": "conejo.png"
          }, 
          {
            "Alive": "True", 
            "Direction": "N", 
            "id": 3, 
            "Position": [
              2, 
              2
            ], 
            "Sprite": "conejo.png"
          }, 
          {
            "Alive": "True", 
            "Direction": "N", 
            "id": 4, 
            "Position": [
              7, 
              1
            ], 
            "Sprite": "lobo.png"
          }, 
          {
            "Alive": "True", 
            "Direction": "N", 
            "id": 5, 
            "Position": [
              5, 
              1
            ], 
            "Sprite": "lobo.png"
          }
        ]
    }, 
      {
        "Step": 1, 
        "info": [
          {
            "Alive": "True", 
            "Direction": "N", 
            "id": 1, 
            "Position": [
              7, 
              3
            ], 
            "Sprite": "conejo.png"
          }, 
          {
            "Alive": "True", 
            "Direction": "N", 
            "id": 2, 
            "Position": [
              1, 
              3
            ], 
            "Sprite": "conejo.png"
          }, 
          {
            "Alive": "True", 
            "Direction": "N", 
            "id": 3, 
            "Position": [
              1, 
              7
            ], 
            "Sprite": "conejo.png"
          }, 
          {
            "Alive": "True", 
            "Direction": "N", 
            "id": 4, 
            "Position": [
              3, 
              3
            ], 
            "Sprite": "lobo.png"
          }, 
          {
            "Alive": "True", 
            "Direction": "N", 
            "id": 5, 
            "Position": [
              4, 
              5
            ], 
            "Sprite": "lobo.png"
          }
        ]
    }]

    return jsonify(fcc_data)

if __name__ == "__main__":
    app.run(debug=True)