class SintacticNode():

    # Constructor de la clase nodo
    def __init__(self, nombre, valor, linea, columna, numero):
        self.nombre = nombre
        self.valor = valor
        self.hijos = []
        self.linea = linea
        self.columna = columna
        self.numero = numero
    
    # Agrega un hijo
    def addHijo(self, hijo):
        self.hijos.append(hijo)

    def getHijo(self, posicion):
        return self.hijos[posicion]