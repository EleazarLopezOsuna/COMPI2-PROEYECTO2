from enum import Enum

class Symbol():
    def __init__(self, type, absolutePosition, relativPosition, row, column, root):
        self.type = type
        self.absolutePosition = absolutePosition
        self.relativePosition = relativPosition
        self.row = row
        self.column = column
        self.root = root
        self.rol = 'Variable'
        self.size = 1
        self.heapPosition = -1
        self.limiteInferior = -1
        self.limiteSuperior = -1
        self.parameterType = 0
        self.content = -1
        self.atributes = -1

    def __init__(self, type, absolutePosition, relativePosition, row, column, root, size, content):
        self.type = type
        self.absolutePosition = absolutePosition
        self.relativePosition = relativePosition
        self.row = row
        self.column = column
        self.root = root
        self.rol = 'Variable'
        self.size = size
        self.atributes = -1
        self.heapPosition = -1
        self.limiteInferior = -1
        self.limiteSuperior = -1
        self.parameterType = 0
        self.content = content

    def __init__(self, type, absolutePosition, relativePosition, row, column, root, size, atributes, heapPosition):
        self.type = type
        self.absolutePosition = absolutePosition
        self.relativePosition = relativePosition
        self.row = row
        self.column = column
        self.root = root
        self.rol = 'Variable'
        self.size = size
        self.atributes = atributes
        self.heapPosition = heapPosition
        self.limiteInferior = -1
        self.limiteSuperior = -1
        self.parameterType = 0
        self.content = -1

class EnumType(Enum):
    arreglo = 1
    caracter = 2
    cadena = 3
    entero = 4
    flotante = 5
    boleano = 6
    nulo = 7
    error = 8
    funcion = 9
    mutable = 10
    nomutable = 11