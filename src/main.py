from vertex import Vertex

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
