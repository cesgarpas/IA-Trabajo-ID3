from naivebayes import NaiveBayes
from vertex import Vertex

from math import log
import csv


def create_tree():
    rows = get_data('../datasets/tic-tac-toe.data.csv')

    naive = NaiveBayes(rows)

    # print(recursion(rows))


def recursion(rows):
    # Calculamos la entropía del conjunto inicial
    initial_entropy = column_entropy(rows)

    # Calculamos las ganancias para cada atributo, parando si se encuentra una ganancia máxima
    for x in range(len(rows[0]) - 1):
        # Ganancia inicial
        gain = initial_entropy

        # Obtenemos para cada valor del atributo, el valor de la última columna
        dict = {}
        for row in rows:
            if row[x] not in dict:
                dict[row[x]] = []
            else:
                dict[row[x]].append(row[-1])

        # Contamos para cada valor del atributo, el numero de positivos y negativos
        for value in dict:
            # Lista de positivos y negativos para el valor del atributo
            posneg = dict[value]
            dict2 = {}
            # Contamos y lo añadimos a un diccionario
            for item in posneg:
                if item not in dict2:
                    dict2[item] = 1
                else:
                    dict2[item] = dict2[item] + 1

            # Obtenemos el numero de positivos y negativos
            posneglist = []
            for item in dict2:
                posneglist.append(dict2[item])

            # Calculamos la ganancia
            gain = gain - (((posneglist[0] + posneglist[1]) / len(rows)) * entropy(posneglist[0], posneglist[1]))

    return initial_entropy


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
    for row in rows:
        if row[-1] not in dict:
            dict[row[-1]] = 1
        else:
            dict[row[-1]] = dict[row[-1]] + 1

    keys = []
    for item in dict:
        keys.append(item)

    return entropy(dict[keys[0]], dict[keys[1]])


def get_data(filename):
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        row_data = []
        for row in spamreader:
            split = row[0].split(",")
            row_data.append(split)
        return row_data

