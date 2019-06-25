from naivebayes import NaiveBayes
from vertex import Vertex


# Naive Bayes
probSi = {"Sí": 0.4, "color-red": 0.8, "color-green": 0.2, "size-big": 0.5, "size-small": 0.5}
probNo = {"No": 0.6, "color-red": 0.3, "color-green": 0.7, "size-big": 0.4, "size-small": 0.6}
naivebayesV = NaiveBayes("Sí", "No", probSi, probNo)

# Vertices ID3
sizeV = Vertex({"big": "Yes", "small": naivebayesV}, "size")
colorV = Vertex({"red": "No", "green": sizeV}, "color")

print("Atributo Raiz:", colorV.attribute)
print("Hijos:", colorV.children)
print("Primer Hijo:", colorV.children['red'])
print("Segundo Hijo:", colorV.children['green'])
print("Atributo del segundo hijo:", colorV.children['green'].attribute)
print("Hijos del segundo hijo:", colorV.children['green'].children)


print("Clasificación de {rojo, grande}:", colorV.classify({"color": "red", "size": "big"}))
print("Clasificación de {verde, grande}:", colorV.classify({"color": "green", "size": "big"}))
print("Clasificación de {verde, pequeño}:", colorV.classify({"color": "green", "size": "small"}))
