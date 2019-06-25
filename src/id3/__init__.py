from naivebayes import NaiveBayes
from vertex import Vertex
import random

from math import log
import csv


def create_tree(dataset, train_percent, quorum, quorum_type, k, shuffle):

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

    # Calculo del quorum si es porcentual
    if quorum_type == "percent":
        final_quorum = int((len(rows)-1) * (int(quorum)/100))
    else:
        final_quorum = int(quorum)

    output += "Quorum: " + str(final_quorum) + "\n\n"

    # ------ Conjuntos de entrenamiento y pruebas ------
    # Se separan los conjuntos en positivos y negativos
    pos_rows = []
    neg_rows = []
    posvalue = rows[1][-1]  # Uno de los dos valores binarios

    for row in rows[1:]:
        if row[-1] == posvalue:
            pos_rows.append(row)
        else:
            neg_rows.append(row)

    # Obtención del índice de división
    pos_percentile = int((len(pos_rows)) * (int(train_percent)/100))
    neg_percentile = int((len(neg_rows)) * (int(train_percent) / 100))

    # Barajado
    if shuffle:
        random.shuffle(pos_rows)
        random.shuffle(neg_rows)

    # Creación de los conjuntos
    train_rows = pos_rows[:pos_percentile] + neg_rows[:neg_percentile]
    test_rows = pos_rows[pos_percentile:] + neg_rows[neg_percentile:]

    # Inserción de los nombre de los atributos al conjunto de entrenamiento
    train_rows.insert(0, rows[0])

    # Salida de los conjuntos
    output += "Tamaño del conjunto total: " + str(len(rows)-1) + "\n"
    output += "Tamaño del conjunto de entrenamiento: " + str(len(train_rows)-1) + "\n"
    output += "Tamaño del conjunto de pruebas: " + str(len(test_rows)) + "\n\n"

    # ------ Ejecución ------
    # Creación del arbol
    naive_bayes = NaiveBayes(train_rows, int(k))
    tree = recursion_base(train_rows, final_quorum, naive_bayes, [], False)

    # ------ Pruebas ------
    # Salida y contadores para pruebas
    attributes = rows[0][:-1]
    output2 = "\n\n\n================== TODAS LAS PRUEBAS ==================\n\n"
    hits_trunc = 0
    hits_id3 = 0
    miss_trunc = 0
    miss_id3 = 0
    trunc = 0
    id3 = 0

    for row in test_rows:
        # Mapeado a el formato de nuestro clasificador
        row_dict = {}
        for x in range(len(attributes)):
            row_dict[attributes[x]] = row[x]

        # Conteo de aciertos
        expected = str(row[-1])
        classification, result, leaf = classify_helper(tree, row_dict)

        # Conteo de hojas
        if leaf == "trunc":
            trunc += 1
            if expected == result:
                hits_trunc += 1
            else:
                miss_trunc += 1
        else:
            id3 += 1
            if expected == result:
                hits_id3 += 1
            else:
                miss_id3 += 1

        # Generación de la salida
        output2 += str(row_dict) + "\n"
        output2 += "Valor esperado: " + expected + "\n"
        output2 += classification + "\n\n"

    # ------ Salida de los resultados ------
    # Porcentaje de acierto total
    hits = hits_id3 + hits_trunc
    miss = miss_id3 + miss_trunc
    hit_percent = hits / (hits + miss)

    output += "Aciertos: " + str(hits) + "\n"
    output += "Fallos: " + str(miss) + "\n"
    output += "Porcentaje de acierto: " + str(hit_percent) + "\n\n"

    # Porcentaje de acierto por tipo de hoja
    id3_total = hits_id3 + miss_id3
    id3_hit_percent = 0 if id3_total == 0 else hits_id3 / id3_total

    trunc_total = hits_trunc + miss_trunc
    trunc_hit_percent = 0 if trunc_total == 0 else hits_trunc / trunc_total

    output += "No. Resultados hojas categoría: " + str(id3) + "\n"
    output += "Porcentaje de acierto hojas categoría: " + str(id3_hit_percent) + "\n\n"
    output += "No. Resultados hojas truncadas: " + str(trunc) + "\n"
    output += "Porcentaje de acierto hojas truncadas: " + str(trunc_hit_percent) + "\n\n"

    # Concatenación final y output
    output += output2

    return output, {"hits": hits, "miss": miss, "hit_percent": hit_percent,
                    "id3_count": id3, "id3_hit_percent": id3_hit_percent,
                    "trunc_count": trunc, "trunc_hit_percent": trunc_hit_percent}


def classify_helper(tree, example):
    classification = tree.clasify(example)

    if type(classification) is type([]):
        return "Rama truncada por el quorum, se clasificará mediante Naive Bayes: " + str(classification), classification[0], "trunc"
    else:
        return "Clasificación por ID3: " + str(classification), classification, "id3"


def recursion_base(rows, quorum, naive_bayes, used_attributes, is_leaf):
    # Calculamos la entropía del conjunto inicial
    data_entropy = column_entropy(rows)

    # Vemos qué tipo de vértice tenemos que crear
    if (len(rows) - 1) < quorum and not is_leaf:    # Hoja-truncada
        return naive_bayes
    elif data_entropy == 0:                         # Hoja-categoría entropía 0
        return rows[1][-1]
    elif is_leaf:                                   # Hoja-categoría entropia no 0
        return id3_clasify_leafs(rows)
    else:                                           # Nodo interior
        return recursion_continue(rows, quorum, naive_bayes, used_attributes, data_entropy)


def recursion_continue(rows, quorum, naive_bayes, used_attributes, entropy):
    # Buscamos el atributo con mayor ganancia
    best_attr = None
    best_attr_gain = -1.0
    best_attr_values = []
    best_attr_values_data = {}

    # TODO - Añadir condición de que si es el ultimo...
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
                attr_value_data = []        # Obtenemos el subconjunto del valor
                attr_value_data.append(rows[0]) # TODO - Simplificar con la anterior
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
    new_used_attributes = list(used_attributes)
    new_used_attributes.append(best_attr)

    children = {}
    if len(new_used_attributes) == (len(rows[0]) - 1):
        for attr_value in best_attr_values:
            children[attr_value] = recursion_base(best_attr_values_data[attr_value], quorum, naive_bayes, new_used_attributes, True)
    else:
        for attr_value in best_attr_values:
            children[attr_value] = recursion_base(best_attr_values_data[attr_value], quorum, naive_bayes, new_used_attributes, False)
    return Vertex(children, best_attr)


def id3_clasify_leafs(rows):
    count = {}
    for row in rows:
        if row[-1] not in count:
            count[row[-1]] = 1
        else:
            count[row[-1]] = count[row[-1]] + 1
    keys = list(count.keys())

    # Se devuelve el que más aparece, o uno aleatorio en falta
    if count[keys[0]] > count[keys[1]]:
        return keys[0]
    elif count[keys[0]] < count[keys[1]]:
        return keys[1]
    else:
        return random.choice(keys)


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
