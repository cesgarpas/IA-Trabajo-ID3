from naivebayes import NaiveBayes
from vertex import Vertex
import random

from math import log
import csv


def create_tree(dataset, train_percent, quorum, quorum_type, k):

    # Salida
    output = ""

    # Obtencion de la dirección del archivo del dataset
    switcher = {
        "ttt": "datasets/tic-tac-toe.data.csv",
        "car": "datasets/car.data",
        "krkp": "datasets/kr-vs-kp.data.csv",
        "ex": "datasets/ejercicio1.data.csv",
    }
    filename = switcher[dataset]
    output += "Dataset: " + str(filename) + "\n"
    output += "Suavizado (K): " + str(k) + "\n"

    # Obtención conjunto de datos
    rows = get_data(filename)

    # Calculo del quorum si es necesario
    if quorum_type == "percent":
        final_quorum = int((len(rows)-1) * (int(quorum)/100))
    else:
        final_quorum = int(quorum)

    output += "Quorum: " + str(final_quorum) + "\n\n"

    # TODO: Dividir en entrenamiento y prueba homogeneamente
    eighty = int((len(rows)-1) * (int(train_percent)/100))
    shuffled = rows[1:]
    random.shuffle(shuffled)
    train_rows = shuffled[:eighty]
    train_rows.insert(0, rows[0])
    test_rows = shuffled[eighty:]

    output += "Tamaño del conjunto total: " + str(len(rows)) + "\n"
    output += "Tamaño del conjunto de entrenamiento: " + str(len(train_rows)) + "\n"
    output += "Tamaño del conjunto de pruebas: " + str(len(test_rows)) + "\n\n"

    # Creación del arbol
    naive_bayes = NaiveBayes(train_rows, int(k))
    tree = recursion_base(train_rows, final_quorum, naive_bayes, [])

    # Pruebas
    attributes = rows[0][:-1]
    for row in test_rows:
        row_dict = {}
        for x in range(len(attributes)):
            row_dict[attributes[x]] = row[x]

        output += str(row_dict) + "\n"
        output += classify_helper(tree, naive_bayes, row_dict) + "\n\n"

    return output


def classify_helper(tree, naive_bayes, example):
    classification = tree.clasify(example)
    if classification is None:
        classification = naive_bayes.clasify(example)
        return "No se pudo clasificar con ID3, se clasificará con Naive Bayes: " + str(classification)
    elif type(classification) is type([]):
        return "Rama truncada por el quorum, se clasificará mediante Naive Bayes: " + str(classification)
    else:
        return "Clasificación por ID3: " + str(classification)


def recursion_base(rows, quorum, naive_bayes, used_attributes):
    # Calculamos la entropía del conjunto inicial
    data_entropy = column_entropy(rows)

    # Vemos qué tipo de vértice tenemos que crear
    if data_entropy == 0:               # Hoja-categoría
        return rows[1][-1]
    elif (len(rows) - 1) < quorum:      # Hoja-truncada
        return naive_bayes
    else:                               # Nodo interior
        return recursion_continue(rows, quorum, naive_bayes, used_attributes, data_entropy)


def recursion_continue(rows, quorum, naive_bayes, used_attributes, entropy):
    # Buscamos el atributo con mayor ganancia
    best_attr = None
    best_attr_gain = -1.0
    best_attr_values = []
    best_attr_values_data = {}

    # Para cada atributo
    for x in range(len(rows[0])-1):
        # Si el atributo aun no se ha usado para clasificar
        if rows[0][x] not in used_attributes:
            # Extraemos los valores del atributo
            attr_values = []
            for row in rows[1:]:
                attr_values.append(row[x])
            attr_values = list(set(attr_values))

            # Creamos la ganancia inicial a partir de la entropía
            gain = entropy

            # Creamos el map para almacenar los subconjuntos para cada valor para tenerlo en caso de ser mejor atributo
            attr_values_data = {}

            # Iteramos los valores
            for attr_value in attr_values:
                # Extraemos los positivos y negativos para el valor del atributo
                count = {}
                attr_value_data = []    # Obtenemos el subconjunto del valor
                attr_value_data.append(rows[0])
                for row in rows[1:]:
                    if row[x] == attr_value:
                        # Se cuenta
                        if row[-1] not in count:
                            count[row[-1]] = 1
                        else:
                            count[row[-1]] = count[row[-1]] + 1
                        # Se añade la row a los datos
                        attr_value_data.append(row)

                # Añadimos la información del valor del atributo al sub dataset para uso posterior
                attr_values_data[attr_value] = attr_value_data

                # Calculamos su entropía
                posneg_values = list(count.values())
                if len(posneg_values) == 1:
                    posneg_values.append(0)
                attr_value_entropy = get_entropy(posneg_values[0], posneg_values[1])

                # Restamos a la ganancia el número de valores / total de ejemplos * entropía valor
                gain -= ((posneg_values[0] + posneg_values[1]) / (len(rows)-1)) * attr_value_entropy

            # Si la ganancia es mayor a la almacenada, almacenamos esta y el atributo
            if gain > best_attr_gain:
                best_attr_gain = gain
                best_attr = rows[0][x]
                best_attr_values = attr_values
                best_attr_values_data = attr_values_data

    # Se añade el atributo elegido a los usados
    new_used_attributes = used_attributes
    new_used_attributes.append(best_attr)

    children = {}
    for attr_value in best_attr_values:
        children[attr_value] = recursion_base(best_attr_values_data[attr_value], quorum, naive_bayes, new_used_attributes)
    return Vertex(children, best_attr)


def get_entropy(x, y):
    if x == 0 or y == 0:
        return 0.0
    var1 = x/(x+y)
    var2 = log(x/(x+y),2)
    var3 = y/(x+y)
    var4 = log(y/(x+y), 2)
    return -var1*var2-var3*var4


def column_entropy(rows):
    dict = {}
    for row in rows[1:]:
        if row[-1] not in dict:
            dict[row[-1]] = 1
        else:
            dict[row[-1]] = dict[row[-1]] + 1

    values = list(dict.values())
    if len(values) == 1:
        values.append(0)

    return get_entropy(values[0], values[1])


def get_data(filename):

    if filename.split(".")[-1] == "csv":
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            row_data = []
            for row in spamreader:
                split = row[0].split(",")
                row_data.append(split)
            return row_data
    elif filename.split(".")[-1] == "data":     # Para cars que no están correctos los datos
        f = open(filename, "r")
        row_data = []
        for row in f:
            split = row.split(",")
            # Eliminamos el salto de linea ala ultimo
            split[-1] = split[-1][:-1]
            # Binarizamos
            if split[-1] == "acc" or split[-1] == "unacc" or split[-1] == "accuracy":
                row_data.append(split)
        return row_data
