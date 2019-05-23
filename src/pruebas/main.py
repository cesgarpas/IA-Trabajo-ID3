from house import House

casa = House(4, 120)
casa2 = House()

print("Metros cuadrados casa",casa.get_square_meters())
print("Numero ventanas casa", casa.get_num_vents())
print("Metros cuadrados casa2",casa2.get_square_meters())
print("Numero ventanas casa", casa2.get_num_vents())



from moto import Moto


moto = Moto(3,120)

print("Ruedas Moto", moto.get_wheels())
print("Velocidad Moto", moto.speed)