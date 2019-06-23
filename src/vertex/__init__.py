from naivebayes import NaiveBayes
from id3 import entropy

class Vertex:

    attribute = None
    children = []

    def __init__(self, *args, **kwargs):   # Children => {valorAtributo:vertice, valorAtributo:True/False}
        if type(args[0]) == type(0.0):
            self.initialize_raw(args[0], args[1])
        else:
            self.initialize_processed(args[0], args[1])

    def initialize_processed(self, children, attribute):   # Children => {valorAtributo:vertice, valorAtributo:True/False}
        self.attribute = attribute
        self.children = children

    def initialize_raw(self, rows, quorum, naive_bayes, entropy, used_attributes):
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

        new_used_attributes = used_attributes
        new_used_attributes.append(best_attr)

        children = {}
        for attr_value in best_attr_values:
            children[attr_value] = recursion(rows, quorum, naive_bayes, entropy, new_used_attributes)
        return Vertex(children, best_attr)




    def clasify(self, example):                     # {atributo:valorAtributo, atributo:valorAtributo}
        value = example[self.attribute]
        child = self.children[value]

        if type(child) is Vertex:                   # Si es un nodo interior
            return child.clasify(example)
        elif type(child) is NaiveBayes:             # Si es una hoja truncada
            return child.clasify_nb(example)
        else:                                       # Si es una hoja categoría
            return child

