from naivebayes import NaiveBayes
from id3 import entropy

class Vertex:

    attribute = None
    children = []

    def __init__(self, children, attribute):   # Children => {valorAtributo:vertice, valorAtributo:True/False}
        self.attribute = attribute
        self.children = children

    def clasify(self, example):                     # {atributo:valorAtributo, atributo:valorAtributo}
        value = example[self.attribute]
        child = self.children[value]

        if type(child) is Vertex:                   # Si es un nodo interior
            return child.clasify(example)
        elif type(child) is NaiveBayes:             # Si es una hoja truncada
            return child.clasify_nb(example)
        else:                                       # Si es una hoja categoría
            return child

