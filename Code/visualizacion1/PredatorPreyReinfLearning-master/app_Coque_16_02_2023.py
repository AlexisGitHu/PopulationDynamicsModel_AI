from flask import Flask, render_template, redirect, current_app, url_for
import os
import subprocess
import asyncio
import threading
import logging

# loop = asyncio.get_event_loop()

app = Flask(__name__)
current_app.config['SERVER_NAME'] = 'server_name'

#datos = []

def lectura_datos():
    global process
    
    while True:   # Could be more pythonic with := in Python3.8+
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        #datos.append(line.decode())
        #datosdos(line.decode())
        # with app.app_context():
        #     redirect(url_for('data',numero = 1, line = line.decode()))
        with current_app.test_request_context():
            redirect(url_for('data',numero = 1, line = line.decode(), _external=True))
       
def printLinea(linea):
    return linea


# def lectura_datos(process):    
#     while True:   # Could be more pythonic with := in Python3.8+
#         line = process.stdout.readline()
#         if not line and process.poll() is not None:
#             break
#         datos.append(line.decode())




process = None


@app.route('/')
def run_command():
   
    return render_template('index.html')

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

@app.route('/data')
def data(numero = 0, line = None):

    if numero == False:
        global process

        command = ['python', 'Main.py', '--numLearningIterations', '20', '--totalNumIterations', '50']
        # """Run a command while printing the live output"""
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        
        thread = threading.Thread(name='lectura_datos', target=lectura_datos)
        thread.setDaemon(True)
        thread.start()
        return "Se van a imprimir los datos"
    else:
        print("he entrado")
        return line

# @app.route('/datosdos')
# def datosdos(line = "Se van a imprimir los datos\n\n"):

#     print("he entrado")
#     return line



    # s = '\n'.join(datos)
    # return s
    

# @app.route('/')
# async def index():
#     run_command(['python', 'Main.py'])
#     # await asyncio.sleep(1)
#     return await render_template('index.html')