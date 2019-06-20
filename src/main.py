
from naivebayes import NaiveBayes

print("NAIVEBAYES")
print("NAIVEBAYES")

probSi = {"color-red": 0.8, "color-blue": 0.2, "size-big": 0.5, "size-small": 0.5}
probNo = {"color-red": 0.3, "color-blue": 0.7, "size-big": 0.4, "size-small": 0.6}
naiveBayes = NaiveBayes("si","no",probSi, probNo)
print(naiveBayes.cat1)
print(naiveBayes.cat2)
print(naiveBayes.cat1_prob)
print(naiveBayes.cat2_prob)
print(naiveBayes.clasify_nb({"color": "red", "size": "big"}))


from vertex import Vertex

print("ID3")
print("ID3")

sizeV = Vertex("size", {"big": "Yes", "small": "No"})
colorV = Vertex("color", {"red": "Yes", "green": sizeV})

print("Atributo Raiz:", colorV.attribute)
print("Hijos:", colorV.children)
print("Primer Hijo:", colorV.children['red'])
print("Segundo Hijo:", colorV.children['green'])
print("Atributo del segundo hijo:", colorV.children['green'].attribute)
print("Hijos del segundo hijo:", colorV.children['green'].children)


print("Clasificación de {rojo, grande}:", colorV.clasify({"color": "red", "size": "big"}))
print("Clasificación de {verde, grande}:", colorV.clasify({"color": "green", "size": "big"}))
print("Clasificación de {verde, pequeño}:", colorV.clasify({"color": "green", "size": "small"}))

import random

print("RANDOM")
print("RANDOM")

array = [1,2,3,4,5,6]
print(array)
random.shuffle(array)
print(array)

