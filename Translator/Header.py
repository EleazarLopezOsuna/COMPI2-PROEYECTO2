# At the moment stack looks like
# absolute | relative | name            | variable
# 0        |    0     | stringConcat    | return
# 1        |    1     | stringConcat    | string 1
# 2        |    2     | stringConcat    | string 2
#-------------------------------------------------------
# 3        |    0     | stringPrint     | string
#-------------------------------------------------------
# 4        |    0     | stringLowerCase | return
# 5        |    1     | stringLowerCase | string
#-------------------------------------------------------
# 6        |    0     | stringUpperCase | return
# 7        |    1     | stringUpperCase | string
#-------------------------------------------------------
# 8        |    0     | stringTimes     | return
# 9        |    1     | stringTimes     | string
# 10       |    2     | stringTimes     | number
#-------------------------------------------------------
# 11       |    0     | numberPower     | return
# 12       |    1     | numberPower     | base
# 13       |    2     | numberPower     | exponent
from .DefaultFunctions import DefaultFunctions

class Header():

    def __init__(self, numeroTemporales):
        self.numeroTemporales = numeroTemporales
        self.codigo = ''
        self.nuevaLinea = '\n'

    def generarCodigo(self):
        self.codigo = 'package main' + self.nuevaLinea
        self.codigo += 'import ("fmt")' + self.nuevaLinea
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
        self.codigo += defaultFunctions.stringLowerCase
        self.codigo += defaultFunctions.stringUpperCase
        self.codigo += defaultFunctions.stringTimes
        self.codigo += defaultFunctions.numberPower
        self.codigo += defaultFunctions.OutOfBounds
        self.codigo += defaultFunctions.DivisionBy0