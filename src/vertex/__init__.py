
class Vertex:

    attribute = None
    children = []

    def __init__(self, attribute, children): #Children => {valorAtributo:vertice, valorAtributo:True/False}
        self.attribute = attribute
        self.children = children

    def clasify(self, example): #{atributo:valorAtributo, atributo:valorAtributo}
        value = example[self.attribute]
        child = self.children[value]

        if type(child) is Vertex:
            return child.clasify(example)
        else:
            return child

