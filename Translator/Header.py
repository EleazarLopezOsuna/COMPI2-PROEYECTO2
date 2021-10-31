from .DefaultFunctions import DefaultFunctions

class Header():

    def __init__(self, numeroTemporales):
        self.numeroTemporales = numeroTemporales
        self.codigo = ''
        self.nuevaLinea = '\n'

    def generarCodigo(self):
        self.codigo = 'package main' + self.nuevaLinea
        self.codigo += 'import ("fmt")' + self.nuevaLinea
        self.codigo += self.nuevaLinea
        self.codigo += 'var STACK[1000000] float64' + self.nuevaLinea
        self.codigo += 'var HEAP[1000000] float64' + self.nuevaLinea
        self.codigo += 'var SP, HP float64' + self.nuevaLinea
        for i in range(self.numeroTemporales + 1):
            if (i == 0):
                self.codigo += 'var T' + str(i)
            elif (i == self.numeroTemporales):
                self.codigo += ', T' + str(i) + ' float64' + self.nuevaLinea
            else:
                self.codigo += ', T' + str(i)
        defaultFunctions = DefaultFunctions()
        self.codigo += defaultFunctions.stringConcat
        self.codigo += defaultFunctions.stringPrint
        self.codigo += defaultFunctions.OutOfBounds
        self.codigo += defaultFunctions.DivisionBy0