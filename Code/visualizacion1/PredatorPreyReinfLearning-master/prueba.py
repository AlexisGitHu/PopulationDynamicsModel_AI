import os
import subprocess
import asyncio
import threading
from queue import Queue
import json

datos = []

def lectura_datos(process, queue):
    global datos
    
    while True:   # Could be more pythonic with := in Python3.8+
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        datos = line.decode()
        queue.put(datos)
        # print(datos, end="")

def run_command():
    command = ['python', '-u', 'Main.py', '--numLearningIterations', '20', '--totalNumIterations', str(50)]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    queue = Queue()
    
    thread = threading.Thread(name='lectura_datos', target=lectura_datos, args=[process, queue])
    thread2 = threading.Thread(name='data', target=data, args=[queue])
    
    thread.start()
    thread2.start()


def data(queue):
    while True:
        # s = '\n'.join(datos)
        datos = queue.get()
        if datos==None:
            break
    
        print("**************************************************")
        print(datos)
        print("**************************************************")

    # return s
run_command()