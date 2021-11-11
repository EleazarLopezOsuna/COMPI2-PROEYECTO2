from enum import Enum

class Symbol():
    def __init__(self, type, role, atributes, lower, upper, absolute, relative, size, reference, row, column, root, functionType):
        self.type = type
        self.role = role
        self.atributes = atributes
        self.lower = lower
        self.upper = upper
        self.absolute = absolute
        self.relative = relative
        self.size = size
        self.reference = reference
        self.row = row
        self.column = column
        self.root = root
        self.functionType = functionType

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