 # PopulationDynamicsModel_AI
Proyecto para la creación de un modelo de simulación de dinámica de poblaciones mediante aprendizaje por refuerzo
Trophic Terra es un software de simulación online de ecosistemas virtuales. Su principal objetivo es recrear modelos presa-depredador de manera empírica. Esto permite hacer estudios sobre la evolución futura de dos especies a lo largo del tiempo en cuestión de minutos.  Para lograrlo, combina las técnicas de simulación multiagente y aprendizaje por refuerzo para entrenar inteligencias artificiales capaces de adaptarse a su entorno. Este proceso de aprendizaje automático se muestra de manera gráfica continuamente, lo que hace que Trophic Terra sea también una herramienta visual para entender el funcionamiento del aprendizaje por refuerzo.
Algunas de las herramientas que podrás encontrar en la página son:
-	Creación de ecosistemas virtuales y visualización de su evolución en el tiempo.
-	Extensa parametrización para adaptar el comportamiento de los individuos a las características reales de las especies estudiadas.
-	Monitorización de la evolución del ecosistema en el tiempo.
-	Comparación de la evolución de las poblaciones con el comportamiento teórico ofrecido por el modelo Lotka-Volterra.
-	Posibilidad de compartir modelos concretos con otros usuarios.

## Instalación
***
Intrucciones de instalación 

1. Clonar el repositorio PopulationDynamicsModel_AI en el escritorio
```bash
git clone https://github.com/AlexisGitHu/PopulationDynamicsModel_AI.git
```
2. Abrir la consola en Code/Servidor
3. Ejecutar el comando: 
```bash 
    pip install -r "requirements.txt"
```
4. Ejecutar el comando: 
```bash 
    python app.py
```
5. Copiar el link http://127.0.0.1:5000 en el navegador para acceder a la web


## Uso del producto
***
Descripción de un escenario típico de uso del producto


1. Pinchar en sign up a la izquierda y rellenar los campos.
2. Rellenar el log in lo que lleva a la sección "Mi unidad".
3. Pinchar en el "+" para crear un nuevo modelo.
4. Introducir el nombre del modelo y darle a crear (se puede elegir la opción de que el modelo sea público), esto lleva a la simulación.
5. Rellenar los parámetros del modelo.
6. Pinchar en crear modelo en el botón de abajo a la izquierda en el recuadro azul debajo de la representación.
7. Darle al play para ver la simulación representada.
8. Pinchar en mostrar gráficas para ver las gráficas del modelo dándole al botón central del recuadro azul debajo de la representación.
9. Pinchar en guardar modelo dándole al botón derecho del recuadro azul debajo de la representación. El modelo no se guardará hasta que no se hayan terminado de ejecutar los cálculos.
10. Pinchar en "Mi unidad" a la izquierda para volver a los proyectos del usuario. El modelo creado en el paso anterior aparecerá disponible pero no se podrá acceder hasta que no se haya terminado de entrenar.
11. Pinchar en el botón de compartir del modelo creado y copiar el código para compartir con otro usuario.
12. Pinchar en "Añadir modelo compartido" e introducir el código del modelo de otro usuario para tener acceso a él.
13. Pinchar en comunidad para ver los modelos públicos.
14. Pinchar en "logout" a la izquierda para cerrar la sesión y volver a la página de inicio.


