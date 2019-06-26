# Trabajo IA - ID3 + Naive Bayes

## Introducción

El trabajo trata de a partir de un valor llamado quórum y un conjunto de datos, crear arboles de decision mixtos, formados por hojas clasificadas por ID3 y hojas truncadas clasificadas por Naive Bayes. El valor quórum determina, al ir ID3 ramificando el árbol, si el conjunto de entrenamiento restante es suficiente para garantizar fiabilidad de la clasificación o, por el contrario, es mejor trurncar la hoja y realizar una llamada a Naive Bayes.

## Instalación y arranque
### Instalación de Graphviz
En primer lugar es necesario instalar graphviz. La versión utilizada en el proyecto está en la carpeta raiz en un zip (graphviz-2.38.msi.zip).

Tras la instalación, es necesario añadir la ruta de la carpeta bin de la ruta de instalación al PATH (C:\Program Files (x86)\Graphviz2.38\bin por defecto)

### Instalación de librerías utilizadas
Abrir una terminal en el directorio src de el proyecto y correr:
```
pipn3 -r install requirements.txt
``` 
O instalar manualmente las dependencias indicadas en este.

### Arrancar servidor Flask

Entrar a src y correr en el terminal:
```
python3 -m flask run
``` 
Esto arrancará el servidor en 127.0.0.1:5000 por defecto

##Relevant urls:

 * http://flask.pocoo.org/docs/1.0/tutorial/ - Flask tutorial with form examples
 * https://github.com/cgpcsjcmp/flask-cesargp - Flask example
 * https://bulma.io/ - Bulma
 * https://matplotlib.org/ - Matplotlib
 * https://www.graphviz.org/ - Graphviz
 * https://pypi.org/project/pydot/ - Pydot
