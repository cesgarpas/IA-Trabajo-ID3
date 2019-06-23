from naivebayes import NaiveBayes
from vertex import Vertex

from math import log
import csv


def create_tree():
    # rows = get_data('../datasets/tic-tac-toe.data.csv')
    rows = get_data('../datasets/pruebas.data.csv')

    naive_bayes = NaiveBayes(rows, 1)  # K = 1

    print(naive.clasify_nb({"continente": "asia", "lugar": "ciudad", "actividad": "opera", "precio": "alto"}))

    print(recursion_base(rows, 10, naive_bayes, []))


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
    best_attr_gain = 0.0
    best_attr_values = []

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

            # Iteramos los valores
            for attr_value in attr_values:
                # Extraemos los positivos y negativos para el valor del atributo
                count = {}
                for row in rows[1:]:
                    if row[x] == attr_value:
                        if row[-1] not in count:
                            count[row[-1]] = 1
                        else:
                            count[row[-1]] = count[row[-1]] + 1
                # Calculamos su entropía
                posneg_values = list(count.values())
                attr_value_entropy = entropy(posneg_values[0], posneg_values[1])
                # Restamos a la ganancia el número de valores / total de ejemplos * entropía valor
                gain -= ((posneg_values[0] + posneg_values[1]) / (len(rows)-1)) * attr_value_entropy

            # Si la ganancia es mayor a la almacenada, almacenamos esta y el atributo
            if gain > best_attr_gain:
                best_attr_gain = gain
                best_attr = rows[0][x]
                best_attr_values = attr_values

    # Se añade el atributo elegido a los usados
    new_used_attributes = used_attributes
    new_used_attributes.append(best_attr)

    children = {}
    for attr_value in best_attr_values:
        children[attr_value] = recursion_base(rows, quorum, naive_bayes, new_used_attributes)
    return Vertex(children, best_attr)


def entropy(x,y):
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

    return entropy(values[0], values[1])


def get_data(filename):
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        row_data = []
        for row in spamreader:
            split = row[0].split(",")
            row_data.append(split)
        return row_data

