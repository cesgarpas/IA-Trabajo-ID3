# Trabajo IA - ID3 + Naive Bayes

## Introducción

El trabajo trata de a partir de un valor llamado quórum y un conjunto de datos, crear arboles de decision mixtos, formados por hojas clasificadas por ID3 y hojas truncadas clasificadas por Naive Bayes. El valor quórum determina, al ir ID3 ramificando el árbol, si el conjunto de entrenamiento restante es suficiente para garantizar fiabilidad de la clasificación o, por el contrario, es mejor trurncar la hoja y realizar una llamada a Naive Bayes.


## Librerías utilizadas

El código de los algoritmos es original, pero se han usado varias librerías para varias cosas:
 * Flask - Para la creación del servidor web
 * Bulma - Para el estilo de la web
 * Matplotlib - Para la creación de las gráficas
 * Graphviz - Para el dibujado de los grafos
 * Pydot - Para el dibujado de los grafos
 
La URL a la documentación de estas librerías se puede encontrar en el apartado "URLs relevantes" más abajo.


## Instalación y arranque

### Instalación de Graphviz

En primer lugar es necesario instalar graphviz. La versión utilizada en el proyecto está en la carpeta raiz en un zip (graphviz-2.38.msi.zip).

Tras la instalación, es necesario añadir la ruta de la carpeta bin de la ruta de instalación al PATH (C:\Program Files (x86)\Graphviz2.38\bin por defecto)


### Instalación de librerías utilizadas

Abrir una terminal en el directorio src de el proyecto y correr:
```
pip3 install -r requirements.txt
``` 
O instalar manualmente las dependencias indicadas en este.


### Arrancar servidor Flask

Entrar a src y correr en el terminal:
```
python3 -m flask run
``` 
Esto arrancará el servidor en 127.0.0.1:5000 por defecto


## URLs relevantes:

 * http://flask.pocoo.org/docs/1.0/ - Flask
 * https://bulma.io/ - Bulma
 * https://matplotlib.org/ - Matplotlib
 * https://www.graphviz.org/ - Graphviz
 * https://pypi.org/project/pydot/ - Pydot
 
 
## Autores

 * César García Pascual
 * Julián Carrascosa Cosano
 
 
## Tutor

 * Agustín Riscos Nuñez
