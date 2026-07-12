#Polimorfismo
#Mismo metodo, diferente comportamiento

class Animal:
    def sonido(self):
        pass # Sin codigo y sin error

class Perro(Animal):
    def sonido(self):
        return "Guau"

class Gato(Animal):
    def sonido(self):
        return "Miau"


animales =[Perro(), Gato()] #Lista de objetos
for animal in animales: #Recorriendo la lista
    print(animal.sonido()) #se imprimi el metodo en cada clase


    