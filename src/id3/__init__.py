from naivebayes import NaiveBayes
from vertex import Vertex

from math import log
import csv


def create_tree():

    print("Dataset: ejercicio.data.csv")
    rows = get_data('../datasets/pruebas.data.csv')
    naive_bayes = NaiveBayes(rows, 0)  # K = 1
    tree = recursion_base(rows, 4, naive_bayes, [])

    classify_helper(tree, naive_bayes,
                    {"continente": "africa", "lugar": "ciudad", "actividad": "opera", "precio": "bajo"})
    classify_helper(tree, naive_bayes,
                    {"continente": "africa", "lugar": "ciudad", "actividad": "opera", "precio": "bajo"})
    classify_helper(tree, naive_bayes,
                    {"continente": "asia", "lugar": "lago", "actividad": "senderismo", "precio": "bajo"})
    classify_helper(tree, naive_bayes,
                    {"continente": "europa", "lugar": "playa", "actividad": "opera", "precio": "bajo"})
    classify_helper(tree, naive_bayes,
                    {"continente": "asia", "lugar": "lago", "actividad": "senderismo", "precio": "bajo"})




    print("Dataset: tic-tac-toe.data.csv")
    rows = get_data('../datasets/tic-tac-toe.data.csv')
    naive_bayes = NaiveBayes(rows, 0)  # K = 1
    tree = recursion_base(rows, 20, naive_bayes, [])

    classify_helper(tree, naive_bayes,
                    {"AA": "x",
                        "AB": "x",
                        "AC": "x",
                        "BA": "b",
                        "BB": "b",
                        "BC": "b",
                        "CA": "b",
                        "CB": "b",
                        "CC": "b"})

    classify_helper(tree, naive_bayes,
                    {"AA": "x",
                        "AB": "x",
                        "AC": "x",
                        "BA": "o",
                        "BB": "o",
                        "BC": "b",
                        "CA": "b",
                        "CB": "b",
                        "CC": "b"})

    classify_helper(tree, naive_bayes,
                    {"AA": "b",
                        "AB": "b",
                        "AC": "b",
                        "BA": "b",
                        "BB": "o",
                        "BC": "o",
                        "CA": "x",
                        "CB": "x",
                        "CC": "x"})

    classify_helper(tree, naive_bayes,
                    {"AA": "x",
                        "AB": "x",
                        "AC": "o",
                        "BA": "x",
                        "BB": "x",
                        "BC": "o",
                        "CA": "o",
                        "CB": "b",
                        "CC": "o"})




    print("Dataset: car.data")
    rows = get_data('../datasets/car.data', "acc", "unacc", "accuracy")
    naive_bayes = NaiveBayes(rows, 0)  # K = 1
    tree = recursion_base(rows, 100, naive_bayes, [])

    classify_helper(tree, naive_bayes,
                    {"buying": "vhigh",
                        "maint": "high",
                        "doors": "4",
                        "persons": "4",
                        "lug_boot": "med",
                        "safety": "med"})

    classify_helper(tree, naive_bayes,
                    {"buying": "high",
                        "maint": "high",
                        "doors": "4",
                        "persons": "4",
                        "lug_boot": "med",
                        "safety": "med"})

    classify_helper(tree, naive_bayes,
                    {"buying": "vhigh",
                        "maint": "high",
                        "doors": "4",
                        "persons": "4",
                        "lug_boot": "med",
                        "safety": "low"})


def classify_helper(tree, naive_bayes, example):
    classification = tree.clasify(example)
    if classification is None:
        classification = naive_bayes.clasify(example)
        print("No se pudo clasificar con ID3, se clasificará con Naive Bayes", classification)
    elif type(classification) is type([]):
        print("Rama truncada por el quorum, se clasificará con Naive Bayes", classification)
    else:
        print("Clasificación por ID3:", classification)


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


def get_entropy(x,y):
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


def get_data(filename, cat1=None, cat2=None, cat_name=None):

    if filename.split(".")[-1] == "csv":
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            row_data = []
            for row in spamreader:
                split = row[0].split(",")
                row_data.append(split)
            return row_data
    elif filename.split(".")[-1] == "data":
        f = open(filename, "r")
        row_data = []
        for row in f:
            split = row.split(",")
            # Eliminamos el salto de linea ala ultimo
            split[-1] = split[-1][:-1]
            # Binarizamos
            if split[-1] == cat1 or split[-1] == cat2 or split[-1] == cat_name:
                row_data.append(split)
        return row_data

